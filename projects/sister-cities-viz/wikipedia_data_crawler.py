from typing import List, Tuple

import click
import pyarrow as pa
from requests_html import AsyncHTMLSession, Element, HTMLSession

BASE_URL = "https://en.wikipedia.org"
HEAD_BASE_URL = "https://en.wikipedia.org/wiki/Lists_of_twin_towns_and_sister_cities"


asession = AsyncHTMLSession()
session = HTMLSession()

sites_visited = set()


def fetch_url(url: str):
    async def _fetch_url():
        if url in sites_visited:
            return None
        r = await asession.get(url)
        sites_visited.add(url)
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

    # for city_tag, cities_sister_cities in zip(cities_tag, sister_city_list_tag):
    #     country: str
    #     lon: str
    #     lat: str
    #     main_city_id: int
    #     try:
    #         country = fetch_country(city_tag)
    #         lat, lon = fetch_geo_location(city_tag)
    #     except:
    #         continue

    #     full_name = f"{city_tag.text}, {country}"

    #     if full_name not in city_id_map:
    #         with database.atomic():
    #             city = Cities.create(
    #                 name=city_tag.text, country=country, lat=lat, lon=lon
    #             )

    #         city_id_map[full_name] = city.cid
    #         main_city_id = city.cid
    #     else:
    #         main_city_id = city_id_map[full_name]

    #     # TODO: Correct missing country issue with going for the a tag directly
    #     for sister_city_tag in cities_sister_cities.find("li > span ~ a"):
    #         print(sister_city_tag.text)

    #         if sister_city_tag.text in city_id_map:
    #             with database.atomic():
    #                 twin_relation = Twinning.create(
    #                     cid1=main_city_id,
    #                     cid2=city_id_map[sister_city_tag.text],
    #                 )
    #         else:
    #             name, *country = sister_city_tag.text.split(", ")
    #             country = ", ".join(country)
    #             lat, lon = fetch_geo_location(sister_city_tag)

    #             with database.atomic():
    #                 city = Cities.create(
    #                     name=sister_city_tag.text, country=country, lat=lat, lon=lon
    #                 )

    #             with database.atomic():
    #                 twin_relation = Twinning.create(
    #                     cid1=main_city_id,
    #                     cid2=city.cid,
    #                 )

    #             city_id_map[sister_city_tag.text] = city.cid


def crawl_webpage(continent_url: str, resp: Element) -> pa.RecordBatch:
    if resp is None:
        return None

    cities_tag = resp.html.find("div.mw-parser-output > p > b")
    sister_city_list_tag = resp.html.find("div.mw-parser-output > p ~ ul, p ~ div > ul")

    next_layer_urls = [
        fetch_url(BASE_URL + tag.attrs["href"])
        for tag in resp.html.find("div.hatnote > a")
    ]
    data = [[], [], []]
    if next_layer_urls:
        for resp in asession.run(*next_layer_urls):
            if resp:
                data[0].append(continent_url)
                data[1].append(resp.url)
                data[2].append(resp.text)

    return pa.RecordBatch.from_arrays(
        data, ["continent_url", "next_layer_url", "page_html"]
    )


def collect_raw_wikipedia_pages() -> List[pa.RecordBatch]:
    resp = session.get(HEAD_BASE_URL)
    continent_urls = [
        fetch_url(BASE_URL + continent_tag.attrs["href"])
        for continent_tag in resp.html.find("div.mw-parser-output > ul > li > a")
    ]
    batches = []
    for resp in asession.run(*continent_urls):
        batches.append(crawl_webpage(resp.url, resp))

    return batches


@click.command()
# @click.option("--")
def main():
    batches = collect_raw_wikipedia_pages()
    table = pa.Table.from_batches(batches)
    print(table)


if __name__ == "__main__":
    main()
