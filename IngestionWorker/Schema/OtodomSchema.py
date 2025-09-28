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
            "name":"description",
            "selector":'div[data-cy="adPageAdDescription"]',
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