from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from typing import Any, Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup

try:
    from ddgs import DDGS
except Exception:  # pragma: no cover
    DDGS = None

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

EVENT_PATTERNS = {
    "collaboration": [
        r"\bcollab\b",
        r"collaboration",
        r"partnership",
        r"capsule",
        r"co-created",
        r"with\s+[A-Z]",
    ],
    "store_opening": [
        r"store opening",
        r"opens? (a )?(new )?store",
        r"opens? in",
        r"flagship",
        r"popup",
        r"pop-up",
        r"retail location",
        r"grand opening",
    ],
    "drop": [
        r"new in",
        r"new drop",
        r"launch",
        r"launched",
        r"launches",
        r"collection",
        r"released",
        r"release",
        r"restock",
    ],
    "pricing": [
        r"¥\s?\d",
        r"\$\s?\d",
        r"price",
        r"priced at",
        r"sale",
        r"discount",
        r"promotion",
    ],
    "strategy": [
        r"strategy",
        r"expansion",
        r"global",
        r"market",
        r"focus",
        r"growth",
        r"rebrand",
        r"positioning",
    ],
    "performance": [
        r"report",
        r"results",
        r"performance",
        r"revenue",
        r"earnings",
        r"growth",
        r"traffic",
    ],
}

PRICE_PATTERN = re.compile(
    r"(?:¥|JPY|\$|USD|S\$|SGD|€|EUR)\s?([0-9]{1,3}(?:[,\.][0-9]{3})*(?:\.[0-9]{2})?|[0-9]{2,})"
)
DATE_PATTERNS = [
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d %b %Y",
    "%b %d, %Y",
]


@dataclass
class SearchRecord:
    brand: str
    category: str
    query: str
    source_type: str
    title: str
    snippet: str
    url: str
    domain: str
    published_at: dt.datetime | None
    event_type: str
    price_points: list[float]
    is_official: bool


def _domain_from_url(url: str) -> str:
    url = url.lower().replace("https://", "").replace("http://", "")
    return url.split("/")[0].replace("www.", "")


def _safe_get(url: str, timeout: int = 20) -> requests.Response | None:
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        if response.status_code < 400:
            return response
    except Exception:
        return None
    return None


def _normalize_date(value: Any) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    for fmt in DATE_PATTERNS:
        try:
            return dt.datetime.strptime(text, fmt)
        except Exception:
            continue
    try:
        return pd.to_datetime(text, utc=False).to_pydatetime()
    except Exception:
        return None


def classify_event(text: str) -> str:
    lowered = text.lower()
    for event_type, patterns in EVENT_PATTERNS.items():
        if any(re.search(pat, lowered, flags=re.IGNORECASE) for pat in patterns):
            return event_type
    return "drop"


def extract_price_points(text: str) -> list[float]:
    prices: list[float] = []
    for match in PRICE_PATTERN.findall(text or ""):
        cleaned = match.replace(",", "").strip()
        try:
            prices.append(float(cleaned))
        except Exception:
            continue
    return prices


def ddgs_available() -> bool:
    return DDGS is not None


def search_web(query: str, max_results: int = 8, mode: str = "text") -> list[dict[str, Any]]:
    if DDGS is None:
        return []

    with DDGS() as ddgs:
        try:
            if mode == "news":
                results = list(ddgs.news(query, max_results=max_results, safesearch="moderate"))
            else:
                results = list(ddgs.text(query, max_results=max_results, safesearch="moderate"))
            return results
        except Exception:
            return []


def build_brand_queries(brand: dict[str, Any], categories: Iterable[str]) -> list[tuple[str, str]]:
    queries: list[tuple[str, str]] = []
    for category in categories:
        category_terms = brand.get("category_queries", {}).get(category, [category.lower()])
        seed = category_terms[0]
        queries.extend(
            [
                (category, f'{brand["name"]} Japan {seed} new drop collaboration store opening'),
                (category, f'{brand["name"]} Japan price {seed}'),
                (category, f'{brand["name"]} global strategy expansion {seed}'),
            ]
        )
    return queries


def run_market_scan(brands: list[dict[str, Any]], categories: list[str], max_results: int = 6) -> pd.DataFrame:
    rows: list[SearchRecord] = []
    for brand in brands:
        queries = build_brand_queries(brand, categories)
        official_domains = brand.get("official_domains", [])
        for category, query in queries:
            for mode in ("news", "text"):
                results = search_web(query, max_results=max_results, mode=mode)
                for item in results:
                    url = item.get("url") or item.get("href") or ""
                    title = item.get("title") or ""
                    snippet = item.get("body") or item.get("snippet") or ""
                    published = _normalize_date(item.get("date") or item.get("published"))
                    domain = _domain_from_url(url)
                    text_blob = f"{title} {snippet}"
                    rows.append(
                        SearchRecord(
                            brand=brand["name"],
                            category=category,
                            query=query,
                            source_type=mode,
                            title=title,
                            snippet=snippet,
                            url=url,
                            domain=domain,
                            published_at=published,
                            event_type=classify_event(text_blob),
                            price_points=extract_price_points(text_blob),
                            is_official=any(d in domain for d in official_domains),
                        )
                    )
    if not rows:
        return pd.DataFrame(
            columns=[
                "brand",
                "category",
                "query",
                "source_type",
                "title",
                "snippet",
                "url",
                "domain",
                "published_at",
                "event_type",
                "price_points",
                "is_official",
            ]
        )
    return pd.DataFrame([r.__dict__ for r in rows]).drop_duplicates(subset=["brand", "title", "url"])


def fetch_page_text(url: str) -> str:
    response = _safe_get(url)
    if not response:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(" ", strip=True)


def extract_article_cards(url: str, limit: int = 20) -> list[dict[str, str]]:
    response = _safe_get(url)
    if not response:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    cards: list[dict[str, str]] = []
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        text = link.get_text(" ", strip=True)
        if not href or not text or len(text) < 8:
            continue
        if href.startswith("/"):
            base = "/".join(url.split("/")[:3])
            href = f"{base}{href}"
        cards.append({"title": text, "url": href})
        if len(cards) >= limit:
            break
    return cards


def summarize_search_stats(scan_df: pd.DataFrame) -> pd.DataFrame:
    if scan_df.empty:
        return pd.DataFrame(columns=["brand", "events", "official_hits", "avg_price_mentions"])

    price_avg = (
        scan_df.assign(price_count=scan_df["price_points"].map(len))
        .groupby("brand", as_index=False)
        .agg(events=("title", "count"), official_hits=("is_official", "sum"), avg_price_mentions=("price_count", "mean"))
    )
    return price_avg.sort_values(["events", "official_hits"], ascending=[False, False])
