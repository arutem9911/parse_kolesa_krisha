import asyncio
from datetime import datetime

from app.parser.house_parser import HouseParser
from app.parser.kolesa_parse import WheelsParser
from app.parser.krisha_parser import FlatsParser
from app.parser.land_plot_parser import LandPlotParser


async def base_service():
    current_year = datetime.now().year
    parser_kolesa_3 = WheelsParser(
        base_url=f"https://kolesa.kz/cars/avtomobili-s-probegom/?_sys-hasphoto=2&"
        f"auto-custom=2&auto-car-transm=2345&auto-sweel=1&auto-car-order=1&"
        f"year%5Bfrom%5D={str(current_year - 20)}&car-dwheel=3",
        drive_well="задний привод",
        pages=200,
    )
    parser_kolesa_2 = WheelsParser(
        base_url=f"https://kolesa.kz/cars/avtomobili-s-probegom/?_sys-hasphoto=2&"
        f"auto-custom=2&auto-car-transm=2345&auto-sweel=1&auto-car-order=1&"
        f"year%5Bfrom%5D={str(current_year - 20)}&car-dwheel=2",
        drive_well="полный привод",
    )
    parser_kolesa_1 = WheelsParser(
        base_url=f"https://kolesa.kz/cars/avtomobili-s-probegom/?_sys-hasphoto=2&"
        f"auto-custom=2&auto-car-transm=2345&auto-sweel=1&auto-car-order=1&"
        f"year%5Bfrom%5D={str(current_year - 20)}&car-dwheel=1",
        drive_well="передний привод",
    )
    parser_krisha = FlatsParser(
        base_url=f"https://krisha.kz/prodazha/kvartiry/"
        f"?das[house.year][from]={str(current_year - 60)}&das[house.year][to]={str(current_year)}&"
        f"das[live.square][from]=30&das[live.square][to]=250"
    )

    parser_land_plot = LandPlotParser(base_url="https://krisha.kz/prodazha/uchastkov/")
    await asyncio.gather(parser_kolesa_1.run(), parser_kolesa_2.run(), parser_kolesa_3.run(), parser_krisha.run())
    for building_material in range(1, 15):
        for condition in range(1, 7):
            parser_house = HouseParser(
                base_url="https://krisha.kz/prodazha/doma-dachi/?das[house.type_object]=1"
                "&das[house.year][from]={str(current_year - 80)}&das[house.year][to]="
                "{str(current_year)}&das[land.square][from]=3&das[live.square][from]=50"
                f"&das[live.square][to]=500&das[house.renewal]={str(condition)}&"
                f"das[house.building_opts]={str(building_material)}",
                condition=condition,
                building_material=building_material,
            )
            await asyncio.gather(parser_house.run())
    try:
        await asyncio.gather(parser_land_plot.run())
    except Exception as err:
        print("Something went wrong: " + str(err))
