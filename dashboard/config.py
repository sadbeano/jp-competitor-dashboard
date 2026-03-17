from __future__ import annotations

BRANDS = [
    {
        "name": "Beyond The Vines",
        "slug": "beyond-the-vines",
        "official_domains": ["beyondthevines.jp", "beyondthevines.com"],
        "market_focus": "Japan + international",
        "is_own_brand": True,
        "category_queries": {
            "Bags": ["bags", "backpack", "tote", "crossbody", "functional bag"],
            "Fashion": ["ready to wear", "womenswear", "menswear", "apparel"],
            "Lifestyle": ["lifestyle", "homeware", "stationery", "accessories"],
        },
        "collections": {
            "bags": [
                "https://www.beyondthevines.jp/collections/bags",
            ],
            "fashion": [
                "https://www.beyondthevines.jp/collections/womens-all",
                "https://www.beyondthevines.jp/collections/mens-all",
            ],
            "lifestyle": [
                "https://www.beyondthevines.jp/collections/lifestyle-all",
            ],
            "new_in": [
                "https://www.beyondthevines.jp/collections/new-in",
                "https://www.beyondthevines.jp/collections/lifestyle-new-in",
                "https://www.beyondthevines.jp/collections/mens-new-in",
            ],
        },
        "stores_page": "https://www.beyondthevines.jp/pages/the-btv-stores",
        "content_pages": {
            "events": "https://www.beyondthevines.jp/blogs/events",
            "collaborations": "https://www.beyondthevines.jp/blogs/collaborations",
            "press": "https://www.beyondthevines.jp/blogs/media-stories",
            "express": "https://www.beyondthevines.jp/blogs/travelling-btv-express",
        },
    },
    {
        "name": "Porter Yoshida & Co.",
        "slug": "porter-yoshida",
        "official_domains": ["yoshidakaban.com", "shop-porter.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["porter bags", "porter backpack", "porter tote"],
            "Fashion": ["porter apparel", "porter wear"],
            "Lifestyle": ["porter accessories", "porter lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "Cotopaxi",
        "slug": "cotopaxi",
        "official_domains": ["cotopaxi.jp", "cotopaxi.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["packs", "bags", "travel pack"],
            "Fashion": ["apparel", "outerwear", "ready to wear"],
            "Lifestyle": ["accessories", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "HAY",
        "slug": "hay",
        "official_domains": ["hay-japan.com", "hay.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bag", "shopper tote"],
            "Fashion": ["apparel", "wear"],
            "Lifestyle": ["homeware", "furniture", "stationery", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "Topologie",
        "slug": "topologie",
        "official_domains": ["topologie.jp", "topologie.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bags", "bottle sacoche", "backpack"],
            "Fashion": ["apparel", "ready to wear"],
            "Lifestyle": ["accessories", "gear", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "Baggu",
        "slug": "baggu",
        "official_domains": ["baggu.com"],
        "market_focus": "International with Japan demand",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bags", "tote", "reusable bag"],
            "Fashion": ["apparel", "ready to wear"],
            "Lifestyle": ["home", "accessories", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "Anello",
        "slug": "anello",
        "official_domains": ["anello.jp"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["backpack", "tote", "bag"],
            "Fashion": ["apparel", "ready to wear"],
            "Lifestyle": ["accessories", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "The Paper Bunny",
        "slug": "the-paper-bunny",
        "official_domains": ["thepaperbunny.com"],
        "market_focus": "Singapore + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["puffer bag", "bag", "backpack"],
            "Fashion": ["apparel", "ready to wear"],
            "Lifestyle": ["bottle", "stationery", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "Standard Supply",
        "slug": "standard-supply",
        "official_domains": ["standardsupply.net"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["backpack", "tote", "pouch"],
            "Fashion": ["wear", "apparel"],
            "Lifestyle": ["lifestyle", "everyday goods"],
        },
        "collections": {},
    },
    {
        "name": "CASETiFY",
        "slug": "casetify",
        "official_domains": ["casetify.com", "casetify.com.jp"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["travel", "bags"],
            "Fashion": ["apparel", "wear"],
            "Lifestyle": ["phone cases", "tech accessories", "collaboration"],
        },
        "collections": {},
    },
    {
        "name": "BEAMS",
        "slug": "beams",
        "official_domains": ["beams.co.jp"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bag", "porter collaboration", "luggage"],
            "Fashion": ["ready to wear", "fashion", "beams collection"],
            "Lifestyle": ["home goods", "lifestyle"],
        },
        "collections": {},
    },
    {
        "name": "MUJI",
        "slug": "muji",
        "official_domains": ["muji.com", "muji.com/jp/ja/store"],
        "market_focus": "Japan + global",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bags", "backpack", "travel"],
            "Fashion": ["wear", "apparel"],
            "Lifestyle": ["household", "stationery", "homeware"],
        },
        "collections": {},
    },
    {
        "name": "and wander",
        "slug": "and-wander",
        "official_domains": ["andwander.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["backpack", "bag", "outdoor pack"],
            "Fashion": ["ready to wear", "outdoor apparel"],
            "Lifestyle": ["accessories", "gear"],
        },
        "collections": {},
    },
    {
        "name": "nanamica",
        "slug": "nanamica",
        "official_domains": ["nanamica.com"],
        "market_focus": "Japan + international",
        "is_own_brand": False,
        "category_queries": {
            "Bags": ["bags", "tote", "backpack"],
            "Fashion": ["ready to wear", "outerwear", "fashion"],
            "Lifestyle": ["accessories", "lifestyle"],
        },
        "collections": {},
    },
]

DEFAULT_CATEGORIES = ["Bags", "Fashion", "Lifestyle"]
EVENT_TYPES = ["pricing", "drop", "collaboration", "strategy", "store_opening", "performance"]
PRICE_CURRENCIES = ["JPY", "¥", "USD", "$", "SGD", "S$", "EUR", "€"]
