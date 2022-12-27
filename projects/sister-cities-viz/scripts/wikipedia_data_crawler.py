import logging
from logging import info
from pathlib import Path
from typing import Dict, Tuple

from peewee import (AutoField, CharField, Check, FloatField, ForeignKeyField,
                    Model, SqliteDatabase)
from requests_html import AsyncHTMLSession, Element, HTMLSession

BASE_URL = "https://en.wikipedia.org"
HEAD_BASE_URL = "https://en.wikipedia.org/wiki/Lists_of_twin_towns_and_sister_cities"

database = SqliteDatabase("data.sqlite")
logging.basicConfig(filename="example.log", level=logging.DEBUG)


class BaseModel(Model):
    class Meta:
        database = database


class Cities(BaseModel):
    cid = AutoField()
    name = CharField()
    country = CharField()
    lat = FloatField()
    lon = FloatField()


# TODO: Add unique clause for name and country


class Twinning(BaseModel):
    fid = AutoField()
    cid1 = ForeignKeyField(
        Cities, backref="city"
    )  # , constraints=[Check("cid1 < cid2")]
    cid2 = ForeignKeyField(Cities, backref="city")


with database:
    database.create_tables([Cities, Twinning])

city_id_map: Dict[str, int] = {}

asession = AsyncHTMLSession()
session = HTMLSession()


def fetch_url(url: str):
    async def _fetch_url():
        r = await asession.get(url)
        return r

    return _fetch_url


def fetch_geo_location(tag) -> Tuple[str, str]:
    url = list(tag.absolute_links)[0]
    resp = session.get(url)
    print(url)
    resp_x = session.get(
        "http:" + resp.html.find("#coordinates > span > a", first=True).attrs["href"]
    )
    lat, lon = resp_x.html.find("td > span.geo", first=True).text.split(", ")
    return lat, lon


def fetch_country(tag) -> str:
    url = list(tag.absolute_links)[0]
    resp = session.get(url)
    return resp.html.find("tr > th.infobox-label ~ td", first=True).text


def crawl_webpage(resp: Element) -> None:
    cities_tag = resp.html.find("div.mw-parser-output > p > b")
    sister_city_list_tag = resp.html.find("div.mw-parser-output > p ~ ul, p ~ div > ul")

    next_layer_urls = [
        fetch_url(BASE_URL + tag.attrs["href"])
        for tag in resp.html.find("div.hatnote > a")
    ]
    if next_layer_urls:
        for resp in asession.run(*next_layer_urls):
            crawl_webpage(resp)

    for city_tag, cities_sister_cities in zip(cities_tag, sister_city_list_tag):
        country: str
        lon: str
        lat: str
        main_city_id: int
        try:
            country = fetch_country(city_tag)
            lat, lon = fetch_geo_location(city_tag)
        except:
            continue

        full_name = f"{city_tag.text}, {country}"

        if full_name not in city_id_map:
            with database.atomic():
                city = Cities.create(
                    name=city_tag.text, country=country, lat=lat, lon=lon
                )

            city_id_map[full_name] = city.cid
            main_city_id = city.cid
        else:
            main_city_id = city_id_map[full_name]

        # TODO: Correct missing country issue with going for the a tag directly
        for sister_city_tag in cities_sister_cities.find("li > span ~ a"):
            print(sister_city_tag.text)

            if sister_city_tag.text in city_id_map:
                with database.atomic():
                    twin_relation = Twinning.create(
                        cid1=main_city_id,
                        cid2=city_id_map[sister_city_tag.text],
                    )
            else:
                name, *country = sister_city_tag.text.split(", ")
                country = ", ".join(country)
                lat, lon = fetch_geo_location(sister_city_tag)

                with database.atomic():
                    city = Cities.create(
                        name=sister_city_tag.text, country=country, lat=lat, lon=lon
                    )

                with database.atomic():
                    twin_relation = Twinning.create(
                        cid1=main_city_id,
                        cid2=city.cid,
                    )

                city_id_map[sister_city_tag.text] = city.cid


def create_sister_cities_dataset() -> None:
    resp = session.get(HEAD_BASE_URL)
    continent_urls = [
        fetch_url(BASE_URL + continent_tag.attrs["href"])
        for continent_tag in resp.html.find("div.mw-parser-output > ul > li > a")
    ][2:3]
    print(continent_urls)
    for resp in asession.run(*continent_urls):
        crawl_webpage(resp)


if __name__ == "__main__":
    create_sister_cities_dataset()
