import re

import pandas as pd
from bs4 import BeautifulSoup
from starlette import status

from app.database.connection import DatabaseConnection
from app.error_handler.error_handler import RequestErrorBadRequest
from app.parser.base_parser import BaseParser
from app.schemas.error_message import RequestErrorMessages


class LandPlotParser(BaseParser):
    def __init__(self, base_url, session=None, pages=5):
        super().__init__(base_url, session=session, pages=pages)
        self.get_views_count_url = "https://krisha.kz/ms/views/krisha/live/"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "connection": "keep-alive",
            "cookie": "krishauid=fda52c8934d89f6fc38c8f8e65f702c628ad4aff; _ym_uid=1715768562344476921; "
            "ssaid=1031aed0-12a5-11ef-8c19-4fa28bd25878; _fbp=fb.1.1715768567060.1008940827; "
            "_tt_enable_cookie=1; "
            "__gsas=ID=f1997cb75e80bd0f:T=1715768845:RT=1715768845:S=ALNI_MbQhs4p4eAi68D6303pSNuLbQ6q_Q; "
            "_ym_d=1731914859; _ttp=smdJWQ6orQfRSKp7Rk-QzFABDGW.tt.1; _gcl_au=1.1.991151796.1733829294; "
            "_gid=GA1.2.39684904.1734416586; krssid=1pa9j5ttjoeodaddtu5e8roup9; _ym_visorc=b; "
            "kr_cdn_host=//alakcell-kz.kcdn.online; _ym_isad=2; "
            "tutorial=%7B%22add-note%22%3A%22viewed%22%2C%22advPage%22%3A%22viewed%22%7D; _gat=1; "
            "__gads=ID=4d70e739d55ca914:T=1715768563:RT=1734499248:S=ALNI_MZjZ4kulxsxGIUNpWOAvd1kbM792Q; "
            "__gpi=UID=00000e1e01efb5c6:T=1715768563:RT=1734499248:S=ALNI_MaRu5YlbDPQWW15tMbvK-RwGhpIpQ; "
            "__eoi=ID=4ca403ad5ae9be6e:T=1731485915:RT=1734499248:S=AA-AfjZxIFnpza8raSzr0gP0q4rz; "
            "_ga_1FR6YEC4BS=GS1.1.1734498704.18.1.1734499256.49.0.0; "
            "_ga_6YZLS7YDS7=GS1.1.1734498702.93.1.1734499257.48.0.0; _ga=GA1.1.685218053.1715768561; "
            "__tld__=null",
            "host": "krisha.kz",
            # "referer": "https://krisha.kz/prodazha/kvartiry/?page=900"
            "sec-ch-ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

    async def save_data_database(self, connection, advert_df):
        await connection.insert_data_land(advert_df)

    def parse_title(self, title_info):
        splited_data = title_info.split(" · ")
        total_area = splited_data[1].split(" ")[0]
        area_unit = splited_data[1].split(" ")[1]
        return total_area, area_unit

    def parse_detail_info(self, detail_info_str):
        divisibility = None
        splited_data = detail_info_str.split(", ")
        if splited_data[0] in ["делимый", "неделимый"]:
            divisibility = splited_data[0]
        return divisibility

    def calculate_price100m2(self, total_area, area_unit, price):
        total_area = float(total_area)
        price = int(price)
        if area_unit == ["га"]:
            total_area = total_area * 100
        calc_price = price / total_area
        return round(calc_price, 1)

    async def parse_page(self, html, connection):
        soup = BeautifulSoup(html, "html.parser")
        lands: list = []
        products = soup.find_all("div", class_=re.compile(r"^a-card a-storage-live ddl_product ddl_product_link.*$"))
        print("products: ", len(products))
        for product in products:
            try:
                link = product.find("a", class_="a-card__image")["href"]
                land: dict = {
                    "price": product.find("div", class_="a-card__price")
                    .text.replace("\xa0", "")
                    .replace("〒", "")
                    .replace("от ", "")
                    .strip(),
                    "link": link,
                    "advert_id": link.split("/")[-1],
                    "city": product.find("div", class_="a-card__stats-item").text.strip(),
                    "views": (
                        product.find("span", class_="a-view-count status-item").text.strip()
                        if product.find("span", class_="a-view-count status-item").text.strip()
                        else 0
                    ),
                    "title": product.find("a", class_="a-card__title").text.strip(),
                    "detail_info": product.find("div", class_="a-card__text-preview").text.strip(),
                    "ad_publication_date": product.find_all("div", class_="a-card__stats-item")[1].text.strip(),
                    "region": product.find("div", class_="a-card__stats-item").text.strip(),
                }
                lands.append(land)
            except Exception:
                print(product)
        parsed_data = pd.DataFrame(lands)
        parsed_data["divisibility"] = parsed_data["detail_info"].apply(lambda x: pd.Series(self.parse_detail_info(x)))
        parsed_data[["total_area", "area_unit"]] = parsed_data["title"].apply(lambda x: pd.Series(self.parse_title(x)))
        parsed_data["cost_per_100m2"] = parsed_data[["total_area", "area_unit", "price"]].apply(
            lambda row: self.calculate_price100m2(row["total_area"], row["area_unit"], row["price"]), axis=1
        )
        links = parsed_data["link"].tolist()
        #
        advert_views = await self.get_views_count(links)
        if advert_views:
            parsed_data["views"] = parsed_data["advert_id"].map(advert_views).fillna(parsed_data["views"])
        print(parsed_data)

        await self.save_data_database(connection, parsed_data)
        # return parsed_data

    async def parse_pages(self):
        connection = DatabaseConnection()
        if not connection.check_connection():
            raise RequestErrorBadRequest(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error connecting to the database"
            )
        for i in range(1, self.pages_count + 1):
            if i > 1:
                url = self.base_url + "?page=" + str(i)
            else:
                url = self.base_url
            try:
                html = await self.parsing_retries(url, i)
                print("page " + str(i))
                await self.parse_page(html, connection)
            except Exception as e:
                print(RequestErrorMessages.ParsePageError + url + ": " + str(e))
                continue
