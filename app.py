from __future__ import annotations

import datetime as dt
import math
from typing import Any

import pandas as pd
import streamlit as st

from dashboard.briefs import build_brand_delta_table, build_executive_brief
from dashboard.config import BRANDS, DEFAULT_CATEGORIES
from dashboard.intelligence import ddgs_available, run_market_scan, summarize_search_stats
from dashboard.site_stats import own_brand_snapshot_frame

st.set_page_config(
    page_title="Japan Market Competitor Intelligence",
    layout="wide",
    page_icon="📈",
)


@st.cache_data(ttl=60 * 60)
def load_scan(selected_brand_names: list[str], selected_categories: list[str], max_results: int) -> pd.DataFrame:
    selected_brands = [b for b in BRANDS if b["name"] in selected_brand_names]
    return run_market_scan(selected_brands, selected_categories, max_results=max_results)


@st.cache_data(ttl=60 * 60)
def load_own_brand() -> pd.DataFrame:
    own_brand = next(brand for brand in BRANDS if brand.get("is_own_brand"))
    return own_brand_snapshot_frame(own_brand)


def fmt_currency(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    return f"¥{value:,.0f}"


def extract_price_summary(price_points: list[float]) -> str:
    if not price_points:
        return ""
    cleaned = [x for x in price_points if x > 0]
    if not cleaned:
        return ""
    return f"{min(cleaned):,.0f}–{max(cleaned):,.0f}"


st.title("Japan market competitor intelligence dashboard")
st.caption("Live prototype: web search + official-site scraping + heuristic AI briefing. No external API keys required.")

with st.sidebar:
    st.header("Control tower")
    selected_brand_names = st.multiselect(
        "Brands",
        options=[b["name"] for b in BRANDS],
        default=[b["name"] for b in BRANDS],
    )
    selected_categories = st.multiselect(
        "Categories",
        options=DEFAULT_CATEGORIES,
        default=DEFAULT_CATEGORIES,
    )
    max_results = st.slider("Search depth per query", min_value=3, max_value=12, value=6)
    st.info(
        "This prototype uses DuckDuckGo-powered search via the ddgs Python package, plus direct page scraping where available."
    )
    refresh = st.button("Refresh live scan", type="primary")

if not ddgs_available():
    st.error("The ddgs package is unavailable. Install requirements.txt and rerun the app.")
    st.stop()

if refresh:
    st.cache_data.clear()

scan_df = load_scan(selected_brand_names, selected_categories, max_results)
own_brand_df = load_own_brand()
summary_df = summarize_search_stats(scan_df)
delta_df = build_brand_delta_table(scan_df, own_brand_df)
brief_text = build_executive_brief(scan_df, own_brand_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tracked brands", len(selected_brand_names))
col2.metric("Signals collected", int(len(scan_df)))
col3.metric("Official-domain hits", int(scan_df["is_official"].sum()) if not scan_df.empty else 0)
col4.metric("Latest run", dt.datetime.now().strftime("%Y-%m-%d %H:%M"))

own = own_brand_df.iloc[0] if not own_brand_df.empty else None
if own is not None:
    st.subheader("Beyond The Vines benchmark layer")
    a, b, c, d, e = st.columns(5)
    a.metric("Observed bag SKUs", int(own["bags_sku_count_observed"] or 0))
    b.metric("Observed fashion SKUs", int(own["fashion_sku_count_observed"] or 0))
    c.metric("Observed lifestyle SKUs", int(own["lifestyle_sku_count_observed"] or 0))
    d.metric("Observed bag median price", fmt_currency(own["bags_median_price"]))
    e.metric("Japan store mentions", int(own["store_mentions_japan"] or 0))

    with st.expander("Own-brand detail snapshot", expanded=False):
        snapshot_rows = [
            ["Bags", int(own["bags_sku_count_observed"] or 0), fmt_currency(own["bags_min_price"]), fmt_currency(own["bags_median_price"]), fmt_currency(own["bags_max_price"])],
            ["Fashion", int(own["fashion_sku_count_observed"] or 0), fmt_currency(own["fashion_min_price"]), fmt_currency(own["fashion_median_price"]), fmt_currency(own["fashion_max_price"])],
            ["Lifestyle", int(own["lifestyle_sku_count_observed"] or 0), fmt_currency(own["lifestyle_min_price"]), fmt_currency(own["lifestyle_median_price"]), fmt_currency(own["lifestyle_max_price"])],
            ["New In", int(own["new_in_sku_count_observed"] or 0), "n/a", fmt_currency(own["new_in_median_price"]), "n/a"],
        ]
        st.dataframe(
            pd.DataFrame(snapshot_rows, columns=["Category", "Observed SKUs", "Min price", "Median price", "Max price"]),
            use_container_width=True,
            hide_index=True,
        )
        st.json(
            {
                "events_count_observed": int(own.get("events_count_observed", 0) or 0),
                "collaborations_count_observed": int(own.get("collaborations_count_observed", 0) or 0),
                "press_count_observed": int(own.get("press_count_observed", 0) or 0),
                "express_count_observed": int(own.get("express_count_observed", 0) or 0),
                "store_mentions_total": int(own.get("store_mentions_total", 0) or 0),
                "store_mentions_japan": int(own.get("store_mentions_japan", 0) or 0),
                "popup_mentions_active_or_recent": int(own.get("popup_mentions_active_or_recent", 0) or 0),
            }
        )

tab1, tab2, tab3, tab4 = st.tabs(["Live feed", "Benchmark", "Trend charts", "AI brief"])

with tab1:
    st.subheader("Live market feed")
    if scan_df.empty:
        st.warning("No live search results returned.")
    else:
        feed = scan_df.copy()
        feed["published_at"] = pd.to_datetime(feed["published_at"], errors="coerce")
        feed["price_band"] = feed["price_points"].map(extract_price_summary)
        display_cols = [
            "published_at",
            "brand",
            "category",
            "event_type",
            "domain",
            "is_official",
            "price_band",
            "title",
            "url",
        ]
        st.dataframe(
            feed.sort_values("published_at", ascending=False)[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "url": st.column_config.LinkColumn("Source"),
                "published_at": st.column_config.DatetimeColumn("Published", format="YYYY-MM-DD HH:mm"),
            },
        )

with tab2:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Brand signal leaderboard")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    with right:
        st.subheader("Brand comparison matrix")
        st.dataframe(delta_df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Signal trends")
    if scan_df.empty:
        st.info("Trend charts will render after a successful scan.")
    else:
        chart_df = scan_df.copy()
        chart_df["published_at"] = pd.to_datetime(chart_df["published_at"], errors="coerce")
        chart_df["date"] = chart_df["published_at"].dt.date

        trend = (
            chart_df.dropna(subset=["date"]) 
            .groupby(["date", "brand"], as_index=False)
            .size()
            .pivot(index="date", columns="brand", values="size")
            .fillna(0)
        )
        mix = (
            chart_df.dropna(subset=["date"]) 
            .groupby(["date", "event_type"], as_index=False)
            .size()
            .pivot(index="date", columns="event_type", values="size")
            .fillna(0)
        )
        st.line_chart(trend)
        st.bar_chart(mix)

with tab4:
    st.subheader("AI-written brief")
    st.markdown(brief_text)
    if not scan_df.empty:
        recent = scan_df.sort_values("published_at", ascending=False).head(12)[
            ["brand", "event_type", "title", "url"]
        ]
        st.caption("Most recent evidence sampled into the brief")
        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True,
            column_config={"url": st.column_config.LinkColumn("Source")},
        )

st.divider()
with st.expander("Implementation notes"):
    st.markdown(
        """
- Official-site scraping is stronger for Beyond The Vines than for the competitor set because the app includes direct collection and stores-page targets for your brand.
- Competitor pricing and launch detection rely primarily on live search results unless you add brand-specific collection URLs.
- The dashboard is production-ready enough for decision support, but not yet a SKU-master system. For production v2, add scheduled snapshots and normalized product matching.
        """
    )
