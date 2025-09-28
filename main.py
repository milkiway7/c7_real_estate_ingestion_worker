from dotenv import load_dotenv
load_dotenv()
import asyncio, json
from IngestionWorker.Services.OtoDomScrapper import OtoDomScrapper

from crawl4ai import (AsyncWebCrawler, BrowserConfig, 
                      JsonCssExtractionStrategy, CrawlerRunConfig, 
                      CacheMode, CrawlResult, DefaultMarkdownGenerator, PruningContentFilter)

URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow"

OFFERS_SCHEMA = {
    "name": "offersPage",
    "baseSelector": "[data-sentry-element='ContentContainer']",
    "fields": [
        {
            "name": "offerUrl",
            "selector": "a[data-cy='listing-item-link']",
            "type": "attribute",
            "attribute": "href"
        }
    ]
}

TOTAL_PAGES_SCHEMA = {
    "name": "numberOfPages",
    "baseSelector": "ul[data-cy='nexus-pagination-component']",
    "fields": [
        {
            "name": "numberOfPages",
            "selector": "li:nth-last-child(2)",
            "type": "text"
        }
    ]
}

OFFER_SCHEMA = {
    "name": "offerDetails",
    "baseSelector":"main",
    "fields": [
        {
            "name":"price",
            "selector":'strong[data-cy="adPageHeaderPrice"]',
            "type":"text"
        },
        {
            "name":"price_m2",
            "selector":'div[aria-label="Cena za metr kwadratowy"]',
            "type":"text"
        },
        {
            "name":"address",
            "selector": 'a[data-sentry-source-file="MapLink.tsx"]',
            "type":"text"
        },
        {
            "name":"offerType",
            "selector":'div[data-sentry-element="CompanyInfoContainer"] :is(a,p):nth-child(2)',
            "type":"text"
        },
        {
            "name":"details",
            "selector":'div[data-sentry-component="AdDetailsBase"] div[data-sentry-element="ItemGridContainer"]',
            "type": "list",
            "fields": [
                {
                    "name":"offerDetailsKey",
                    "selector":"div:nth-child(1)",
                    "type":"text"
                },
                {
                    "name":"offerDetailsValue",
                    "selector":"div:nth-child(2)",
                    "type":"text"
                }
            ]
        }
    ]
}

async def offers_url_list():
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_for="css:a[data-cy='listing-item-link']",
        scan_full_page=True,          # przewiń, by dociągnąć oferty
        remove_overlay_elements=True, # zamknij pop-upy/cookies
        magic=True,                   # udaj, że jesteś człowiekiem
        extraction_strategy=JsonCssExtractionStrategy(OFFERS_SCHEMA),
        verbose=True,
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(URL, config=run_cfg)
        data = json.loads(result.extracted_content or "[]")
        # Linki zapieszę do self.urls
        links = [row["offerUrl"] for row in data if row["offerUrl"]]
        return links
    
async def total_pages():
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_for="css:ul[data-cy='nexus-pagination-component']",
        scan_full_page=True,          # przewiń, by dociągnąć oferty
        remove_overlay_elements=True, # zamknij pop-upy/cookies
        magic=True,                   # udaj, że jesteś człowiekiem
        extraction_strategy=JsonCssExtractionStrategy(TOTAL_PAGES_SCHEMA),
        verbose=True,
    )
    async with AsyncWebCrawler() as crawler:
        result : CrawlResult = await crawler.arun(URL, config=run_cfg)
        data = json.loads(result.extracted_content or "[]")
        # Linki zapieszę do self.urls
        total_pages = int(data[0]["numberOfPages"]) if data and data[0].get("numberOfPages") else 1
        print(f"Liczba stron: {total_pages}")

async def offer_details():
    url_suffix_list = await offers_url_list()
    urls = ['https://www.otodom.pl/pl/oferta/nowe-mieszkanie-garaz-gratis-ID4yehq', 'https://www.otodom.pl/pl/oferta/unikatowe-mieszkanie-widok-na-wawel-i-zielen-mateczny-3-pokoje-ID4y3N5', 'https://www.otodom.pl/pl/oferta/przestronne-2-pokoje-z-wyjatkowym-salonem-klucze-od-reki-ID4vfwb', 'https://www.otodom.pl/pl/oferta/2pok-pld-0-promocja-gotowe-wejscie-ID4yhTE', 'https://www.otodom.pl/pl/oferta/zamieszkaj-w-sasiedztwie-krakowskiej-winnicy-ID4yhTc', 'https://www.otodom.pl/pl/oferta/os-bohaterow-wrzesnia-3-pokoje-1-minuta-do-tramwaju-ID4xEz0', 'https://www.otodom.pl/pl/oferta/twoj-dom-dla-ciebie-i-twojego-pupila-ID4yhTb', 'https://www.otodom.pl/pl/oferta/apartament-4-pokoje-ul-emaus-wola-justowska-ID4m8fX', 'https://www.otodom.pl/pl/oferta/2-pokoje-w-nowej-inwestycji-na-pradniku-bialym-ID4vzxa', 'https://www.otodom.pl/pl/oferta/nowa-oferta-3-pokojowe-mieszkanie-przy-parku-ID4yhSK', 'https://www.otodom.pl/pl/oferta/zabiniec-vita-ID4veh6', 'https://www.otodom.pl/pl/oferta/mieszkanie-3pokoje-zielono-komunikacja-ID4tXz0', 'https://www.otodom.pl/pl/oferta/2-pokoje-balkon-piwnica-ul-obozowa-ruczaj-zielona-czesc-krakowa-ID4xlmj', 'https://www.otodom.pl/pl/oferta/mieszkanie-jasne-balkon-komunikacja-ID4wr5k', 'https://www.otodom.pl/pl/oferta/kawalerka-5-minut-od-kazimierza-15min-rynek-ID4vCjt', 'https://www.otodom.pl/pl/oferta/kazimierz-mieszkanie-w-odnowionej-kamienicy-22-5m2-do-remontu-ID4yhS8', 'https://www.otodom.pl/pl/oferta/2-pokojowe-mieszkanie-36m2-balkon-bezposrednio-ID4yhS3', 'https://www.otodom.pl/pl/oferta/wyjatkowe-m3-w-harmonogramie-ID4yhRH', 'https://www.otodom.pl/pl/oferta/mieszkanie-z-widokiem-na-park-wielicka-ID4yhRE', 'https://www.otodom.pl/pl/oferta/osiedle-ozon-ID4uKL1', 'https://www.otodom.pl/pl/oferta/atrakcyjna-cena-lokalizacja-parking-pradnik-czerwony-ID4yhRx', 'https://www.otodom.pl/pl/oferta/bialopradnicka-park-ID4uarz', 'https://www.otodom.pl/pl/oferta/ogrodek-177m2-balkon-dwustronna-ekspozycja-ID4yhRz', 'https://www.otodom.pl/pl/oferta/4-pokojowe-z-duzym-balkonem-i-garazem-ID4yhQU', 'https://www.otodom.pl/pl/oferta/balkon-piwnica-2-lub-3-pokoje-park-ID4yhQJ', 'https://www.otodom.pl/pl/oferta/krakow-ul-lea-kawalerka-na-sprzedaz-blisko-uczelni-agh-ID4xElz', 'https://www.otodom.pl/pl/oferta/krowodrza-ul-skarbinskiego-3-pokoje-41m2-w-nowym-budownictwie-ID4xMu7', 'https://www.otodom.pl/pl/oferta/86-37-m2-4-pokoje-ul-kazimierza-wielkiego-ID4wJC6', 'https://www.otodom.pl/pl/oferta/1-pokojowe-mieszkanie-30m2-balkon-ID4y5Vu', 'https://www.otodom.pl/pl/oferta/mieszkaj-w-miescie-etap-poetow-bud-k-ID4ul4O', 'https://www.otodom.pl/pl/oferta/piasta-park-vi-mieszkanie-2-pok-g1-80-ID4x6DB', 'https://www.otodom.pl/pl/oferta/lepkowskiego-11-mieszkanie-3-pok-11-m37-ID4x6EC', 'https://www.otodom.pl/hpr/pl/oferta/2pok-pld-0-promocja-gotowe-wejscie-ID4yhTE']
    # urls = [f"https://www.otodom.pl" + suffix for suffix in url_suffix_list]
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_for="css:main",
        # scan_full_page=True,          # przewiśnij, by dociągnąć oferty
        remove_overlay_elements=True, # zamknij pop-upy/cookies
        magic=True,                   # udaj, że jesteś człowiekiem
        extraction_strategy=JsonCssExtractionStrategy(OFFER_SCHEMA),
        verbose=True,
    )
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        results = await crawler.arun_many(
            urls = urls,
            config= run_cfg
            )
        for result in results:
            data = json.loads(result.extracted_content or "[]")
            print(data)

async def main():
    scrapper = OtoDomScrapper()
    await scrapper.start()
    scrapper.prepare_offers_page_url()

    
if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(offers_url_list())
    # # asyncio.run(total_pages())
    # asyncio.run(offer_details())



