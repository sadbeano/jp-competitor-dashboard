from __future__ import annotations

import math
import re
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .intelligence import USER_AGENT, _safe_get, extract_article_cards, fetch_page_text

MONEY_REGEX = re.compile(r"(?:¥|JPY|\$|USD|S\$|SGD|€|EUR)\s?([0-9]{1,3}(?:[,\.][0-9]{3})*(?:\.[0-9]{2})?|[0-9]{2,})")
TITLE_PRICE_BLOCK = re.compile(r"([A-Za-z0-9\-\'&/\s]{3,80})\s+(?:¥|JPY|\$|USD|S\$|SGD|€|EUR)\s?([0-9]{1,3}(?:[,\.][0-9]{3})*(?:\.[0-9]{2})?|[0-9]{2,})")
STORE_LINE_PATTERN = re.compile(r"\b(?:Tokyo|Osaka|Kyoto|Nagoya|Singapore|Japan|New York|Shibuya|Shinjuku|Yokohama|Guangzhou)\b", re.IGNORECASE)


def _parse_prices_from_html(html: str) -> list[float]:
    prices: list[float] = []
    for match in MONEY_REGEX.findall(html):
        cleaned = match.replace(",", "")
        try:
            prices.append(float(cleaned))
        except Exception:
            continue
    return prices


def _extract_products_from_page(url: str) -> list[dict[str, Any]]:
    response = _safe_get(url)
    if not response:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    products: list[dict[str, Any]] = []

    for name, price in TITLE_PRICE_BLOCK.findall(text):
        cleaned_name = " ".join(name.split())
        if len(cleaned_name) < 4:
            continue
        try:
            products.append({"title": cleaned_name, "price": float(price.replace(",", ""))})
        except Exception:
            continue

    seen = set()
    unique_products: list[dict[str, Any]] = []
    for item in products:
        key = (item["title"], item["price"])
        if key in seen:
            continue
        seen.add(key)
        unique_products.append(item)
    return unique_products


def category_snapshot(urls: list[str]) -> dict[str, Any]:
    all_products: list[dict[str, Any]] = []
    scanned_urls = 0
    for url in urls:
        products = _extract_products_from_page(url)
        if products:
            scanned_urls += 1
            all_products.extend(products)

    prices = [item["price"] for item in all_products if item.get("price")]
    if not prices:
        return {
            "sku_count_observed": 0,
            "median_price": math.nan,
            "min_price": math.nan,
            "max_price": math.nan,
            "sample_products": [],
            "scanned_urls": scanned_urls,
        }

    sample_products = all_products[:8]
    return {
        "sku_count_observed": len(all_products),
        "median_price": float(pd.Series(prices).median()),
        "min_price": float(min(prices)),
        "max_price": float(max(prices)),
        "sample_products": sample_products,
        "scanned_urls": scanned_urls,
    }


def store_snapshot(stores_page: str) -> dict[str, Any]:
    text = fetch_page_text(stores_page)
    if not text:
        return {"total_store_mentions": 0, "japan_store_mentions": 0, "active_popup_mentions": 0}

    total_store_mentions = len(re.findall(r"(?:Design Store|Design Post|The BTV Express|Store,|Store )", text, flags=re.IGNORECASE))
    japan_section = text.split("Japan")[-1] if "Japan" in text else text
    japan_store_mentions = len(re.findall(r"(?:Tokyo|Osaka|Shinjuku|Shibuya|Umeda|Isetan|PARCO)", japan_section, flags=re.IGNORECASE))
    active_popup_mentions = len(re.findall(r"open from .*?2026|open from .*?2025", text, flags=re.IGNORECASE))
    return {
        "total_store_mentions": total_store_mentions,
        "japan_store_mentions": japan_store_mentions,
        "active_popup_mentions": active_popup_mentions,
    }


def content_snapshot(content_pages: dict[str, str]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for label, url in content_pages.items():
        cards = extract_article_cards(url, limit=24)
        output[f"{label}_count_observed"] = len(cards)
        output[f"{label}_sample_titles"] = [card["title"] for card in cards[:6]]
    return output


def own_brand_snapshot(brand: dict[str, Any]) -> dict[str, Any]:
    collections = brand.get("collections", {})
    bag_stats = category_snapshot(collections.get("bags", []))
    fashion_stats = category_snapshot(collections.get("fashion", []))
    lifestyle_stats = category_snapshot(collections.get("lifestyle", []))
    new_in_stats = category_snapshot(collections.get("new_in", []))
    stores = store_snapshot(brand.get("stores_page", ""))
    content = content_snapshot(brand.get("content_pages", {}))

    return {
        "brand": brand["name"],
        "bags_sku_count_observed": bag_stats["sku_count_observed"],
        "bags_median_price": bag_stats["median_price"],
        "bags_min_price": bag_stats["min_price"],
        "bags_max_price": bag_stats["max_price"],
        "fashion_sku_count_observed": fashion_stats["sku_count_observed"],
        "fashion_median_price": fashion_stats["median_price"],
        "fashion_min_price": fashion_stats["min_price"],
        "fashion_max_price": fashion_stats["max_price"],
        "lifestyle_sku_count_observed": lifestyle_stats["sku_count_observed"],
        "lifestyle_median_price": lifestyle_stats["median_price"],
        "lifestyle_min_price": lifestyle_stats["min_price"],
        "lifestyle_max_price": lifestyle_stats["max_price"],
        "new_in_sku_count_observed": new_in_stats["sku_count_observed"],
        "new_in_median_price": new_in_stats["median_price"],
        "store_mentions_total": stores["total_store_mentions"],
        "store_mentions_japan": stores["japan_store_mentions"],
        "popup_mentions_active_or_recent": stores["active_popup_mentions"],
        **content,
    }


def own_brand_snapshot_frame(brand: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([own_brand_snapshot(brand)])
