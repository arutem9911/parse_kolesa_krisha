import json
import re

import pandas as pd
from bs4 import BeautifulSoup

from app.parser.base_parser import BaseParser


class WheelsParser(BaseParser):
    def __init__(self, base_url, session=None, pages=800, drive_well=None):
        super().__init__(base_url, session=session, pages=pages)
        self.drive_well = drive_well
        self.get_views_count_url = "https://kolesa.kz/ms/views/kolesa/live/"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "connection": "keep-alive",
            "cookie": "_ym_uid=1715772605479301488; ssaid=7b757740-12ae-11ef-825d-536c7ddb71bd; _tt_enable_cookie=1; "
            "_fbp=fb.1.1715772607889.1596671643; _gcl_au=1.1.671211688.1731390709; "
            "_ga_K5X92C5C5C=GS1.1.1731393737.2.0.1731393737.0.0.0; _ym_d=1731914867; "
            "_ttp=VX7VuYkgETfwFD8o-Le6VrrugGF.tt.1; _gcl_gs=2.1.k1$i1732885518$u85307779; "
            "_gac_UA-20095517-1=1.1732885519.EAIaIQobChMIjfm324mBigMVnlGRBR2Lri5gEAAYASAAEgIlSPD_BwE; "
            "_gcl_aw=GCL.1732885520.EAIaIQobChMIjfm324mBigMVnlGRBR2Lri5gEAAYASAAEgIlSPD_BwE; nps=viewed; "
            "klssid=nfk7gl8kad3s70u719bm9oohs6; _gid=GA1.2.582543627.1734513683; _ym_isad=2; "
            "kl_cdn_host=//alaps-kz.kcdn.online; "
            "__gads=ID=98a55605eedea13d:T=1715772607:RT=1734513683:S=ALNI_MbaZXzHhVv2qh999n1kugk0szoitg; "
            "__gpi=UID=00000e1e093d0acd:T=1715772607:RT=1734513683:S=ALNI_MYwnBzYlyMq6sWjU7caX70WyCPZsA; "
            "__eoi=ID=676d6e48b562e5b9:T=1731485905:RT=1734513683:S=AA-AfjYYDXFWuzWwWiKx5d90NVwQ; "
            "_ym_visorc=b; gh_show=1; _ga_K434WRXPFF=GS1.1.1734513684.64.1.1734513848.60.0.86506404; "
            "_ga_J2EHNEPMTC=GS1.1.1734513683.42.1.1734513849.60.0.405143668; "
            "_ga=GA1.2.183927607.1715772605; _gat=1; __tld__=null",
            "host": "kolesa.kz",
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

    def parse_detail_info(self, detail_info_str):
        """
        Асинхронно парсит строку, разделяя её по ', '.
        """
        splitted_data = detail_info_str.split(", ")
        year = None
        body = None
        engine_volume = None
        engine = None
        mileage = None
        transmission = None
        for item_data in splitted_data:
            if " г." in item_data:
                year = item_data.replace(" г.", "").strip()
            elif "Б/у " in item_data:
                body = item_data.replace("Б/у ", "").strip()
            elif " л" == item_data[-2:]:
                engine_volume = item_data.replace(" л", "").strip()
            elif item_data in ["бензин", "дизель", "газ-бензин", "газ", "гибрид", "электричество"]:
                engine = item_data.strip()
            elif "с пробегом " in item_data:
                mileage = item_data.replace("с пробегом ", "").replace(" км", "").replace(" ", "").strip()
            elif any(keyword in item_data for keyword in ["автомат", "типтроник", "вариатор", "робот"]):
                if not transmission:
                    transmission = item_data.strip()

        return splitted_data, year, body, engine_volume, engine, mileage, transmission

    async def save_data_database(self, connection, advert_df):
        await connection.insert_data_car(advert_df)

    async def parse_page(self, html, connection):
        """
        Парсит HTML страницу с данными о колесах.
        """
        soup = BeautifulSoup(html, "html.parser")
        wheels: list = []
        products = soup.find_all("div", class_="a-card js__a-card")
        print("products: ", len(products))
        for product in products:
            try:
                script = product.find("script", type="text/javascript")
                json_data = re.search(r"listing.items.push\((\{.*\})\);", script.string).group(1)  # type: ignore
                data = json.loads(json_data)
                brand = data["attributes"]["brand"]
                model = data["attributes"]["model"]
                ad_publication_date = data["publicationDate"]
                link = product.find("a", class_="a-card__link")["href"]
                wheel: dict = {
                    "drive_well": self.drive_well,
                    "price": product.find("span", class_="a-card__price")
                    .text.replace("\xa0", "")
                    .replace("₸", "")
                    .strip(),
                    "link": link,
                    "advert_id": link.split("/")[-1],
                    "city": product.find("span", {"data-test": "region"}).text.strip(),
                    "ad_publication_date": ad_publication_date,
                    "views": product.find("span", class_="a-card__views nb-views").text.strip(),
                    "brand": brand,
                    "model": model,
                    "detail_info": product.find("p", class_="a-card__description").text.strip(),
                }
                wheels.append(wheel)
            except Exception:
                pass
        parsed_data = pd.DataFrame(wheels)

        parsed_data[
            ["detail_info", "year", "body", "engine_volume", "engine", "mileage", "transmission"]
        ] = parsed_data["detail_info"].apply(lambda x: pd.Series(self.parse_detail_info(x)))
        links = parsed_data["link"].tolist()
        advert_views = await self.get_views_count(links)
        if advert_views:
            parsed_data["views"] = parsed_data["advert_id"].map(advert_views).fillna(parsed_data["views"])
        await self.save_data_database(connection, parsed_data)
        return parsed_data
