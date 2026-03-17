from __future__ import annotations

import math
from typing import Any

import pandas as pd


def _fmt_price(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    return f"¥{value:,.0f}"


def build_executive_brief(scan_df: pd.DataFrame, own_brand_df: pd.DataFrame) -> str:
    if scan_df.empty:
        return "No live web results returned. Check connectivity or broaden the date range."

    top_brands = (
        scan_df.groupby("brand", as_index=False)
        .agg(signals=("title", "count"), official_hits=("is_official", "sum"))
        .sort_values(["signals", "official_hits"], ascending=[False, False])
        .head(5)
    )
    event_mix = scan_df["event_type"].value_counts().to_dict()
    latest = (
        scan_df.sort_values("published_at", ascending=False)
        [["brand", "title", "event_type", "domain"]]
        .head(8)
        .to_dict("records")
    )

    own = own_brand_df.iloc[0].to_dict() if not own_brand_df.empty else {}
    strongest_competitor = top_brands.iloc[0]["brand"] if not top_brands.empty else "n/a"
    brief_lines = [
        "## AI market brief",
        f"Signal volume is currently led by **{strongest_competitor}**, based on the number of live search hits captured in this run.",
        f"The dominant signal types in this snapshot are: {', '.join(f'{k} ({v})' for k, v in list(event_mix.items())[:4])}.",
        "",
        "### Own-brand benchmark",
        f"Beyond The Vines observed bag assortment: **{int(own.get('bags_sku_count_observed', 0) or 0)} SKUs**, median observed bag price **{_fmt_price(own.get('bags_median_price'))}**.",
        f"Observed fashion assortment: **{int(own.get('fashion_sku_count_observed', 0) or 0)} SKUs**, median observed fashion price **{_fmt_price(own.get('fashion_median_price'))}**.",
        f"Observed lifestyle assortment: **{int(own.get('lifestyle_sku_count_observed', 0) or 0)} SKUs**, median observed lifestyle price **{_fmt_price(own.get('lifestyle_median_price'))}**.",
        f"Store footprint signals captured from the official stores page: **{int(own.get('store_mentions_total', 0) or 0)} store mentions**, **{int(own.get('store_mentions_japan', 0) or 0)} Japan-store mentions**, **{int(own.get('popup_mentions_active_or_recent', 0) or 0)} active/recent popup mentions**.",
        "",
        "### What to watch next",
        "1. Compare each competitor's collaboration and store-opening intensity against Beyond The Vines' current launch cadence.",
        "2. Watch for sustained pricing mentions in official-domain pages; repeated movement usually signals markdowns, new assortment tiers, or premiumization.",
        "3. Treat spikes in 'strategy' and 'performance' signals as early indicators of market expansion or repositioning.",
        "",
        "### Latest notable items",
    ]

    for item in latest:
        brief_lines.append(
            f"- **{item['brand']}** | {item['event_type']} | {item['title']} ({item['domain']})"
        )
    return "\n".join(brief_lines)


def build_brand_delta_table(scan_df: pd.DataFrame, own_brand_df: pd.DataFrame) -> pd.DataFrame:
    benchmark = (
        scan_df.groupby(["brand", "event_type"], as_index=False)
        .size()
        .pivot(index="brand", columns="event_type", values="size")
        .fillna(0)
        .reset_index()
    )

    if own_brand_df.empty:
        return benchmark

    own_row = own_brand_df.iloc[0]
    benchmark["observed_bag_skus"] = benchmark["brand"].map(
        lambda x: own_row["bags_sku_count_observed"] if x == "Beyond The Vines" else None
    )
    benchmark["observed_fashion_skus"] = benchmark["brand"].map(
        lambda x: own_row["fashion_sku_count_observed"] if x == "Beyond The Vines" else None
    )
    benchmark["observed_lifestyle_skus"] = benchmark["brand"].map(
        lambda x: own_row["lifestyle_sku_count_observed"] if x == "Beyond The Vines" else None
    )
    return benchmark.sort_values("brand")
