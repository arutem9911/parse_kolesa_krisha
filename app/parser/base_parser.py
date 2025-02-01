import asyncio
import random
from abc import ABC, abstractmethod

import aiohttp
from starlette import status

from app.database.connection import DatabaseConnection
from app.error_handler.error_handler import RequestErrorBadRequest
from app.schemas.error_message import RequestErrorMessages
from proxies import proxies


class BaseParser(ABC):
    def __init__(self, base_url, session=None, pages=10):
        self.base_url = base_url
        self.session = session
        self.pages_count = pages
        self.__proxies = proxies
        self.get_views_count_url = ""
        self.headers = {}

    async def get_views_count(self, links: list):
        advert_ids = [i.split("/")[-1] for i in links]
        adverts_list = ",".join(advert_ids)
        url = self.get_views_count_url + adverts_list + "/"
        async with self.session.get(url, proxy=self.gef_random_proxy(), headers=self.headers) as response:
            views_resp = await response.json()
        advert_views = [(advert_id, views["nb_views"]) for advert_id, views in views_resp.get("data").items()]
        return dict(advert_views)

    def gef_random_proxy(self):
        return random.choice(self.__proxies)

    @abstractmethod
    def parse_page(self, html, connection):
        raise RequestErrorBadRequest(code=status.HTTP_400_BAD_REQUEST, message=RequestErrorMessages.AbstractMethod)

    @abstractmethod
    async def save_data_database(self, connection, advert_df):
        raise RequestErrorBadRequest(code=status.HTTP_400_BAD_REQUEST, message=RequestErrorMessages.AbstractMethod)

    async def parsing_retries(self, url, i):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                proxy = random.choice(self.__proxies)
                async with self.session.get(url, proxy=proxy, timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        retries += 1
                        await asyncio.sleep(2)
            except asyncio.TimeoutError:
                retries += 1
                await asyncio.sleep(2)
                print(f"failed {i}")
                print(url)
            except Exception:
                retries += 1
                print(f"failed {i}")
        await asyncio.sleep(2)

    async def parse_pages(self):
        connection = DatabaseConnection()
        if not connection.check_connection():
            raise RequestErrorBadRequest(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error connecting to the database"
            )
        for i in range(1, self.pages_count + 1):
            if i > 1:
                url = self.base_url + "&page=" + str(i)
            else:
                url = self.base_url
            try:
                html = await self.parsing_retries(url, i)
                print("page " + str(i))
                await self.parse_page(html, connection)
            except Exception as e:
                print(RequestErrorMessages.ParsePageError + url + ": " + str(e))
                continue

    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            await self.parse_pages()
