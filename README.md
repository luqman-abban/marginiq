# Corporaci-n-Favorita-Grocery-Sales-Forecasting


# MarginIQ — Profit Leakage & Decision Intelligence Platform

> Most dashboards tell you what happened. MarginIQ tells you where the business
> is losing money, why, and what fixing it is worth — in dollars.

<!-- Badges: build status, license, Python version, release — added in M8 -->

## Why this exists

Grocery retail runs on 2–4% net margins. For a chain with 54 stores and
thousands of SKUs, a 1% margin leak is not a rounding error — it is the entire
profit line. MarginIQ is a decision-intelligence system built on 125M rows of
real transaction data from Corporación Favorita (Ecuador, 2013–2017) that
detects, quantifies, and ranks margin leakage, then recommends actions with
estimated dollar impact.

**Who uses it:**
- CFO — "Where are we losing money, ranked by dollar impact?"
- VP Supply Chain — "Which stores and items bleed through stockouts and waste?"
- Head of Merchandising — "Which promotions actually made money?"
- Category managers — daily drill-down and recommendation queue

## Leakage categories (v1.0)

<!-- Final four chosen for v1, with one-line definitions. Backlog items link
     to GitHub Issues. Filled in at end of M1. -->

## Architecture

<!-- Diagram image + narrative. Raw CSVs -> DuckDB bronze/silver/gold ->
     Python analytics engine -> semantic layer (YAML metrics) ->
     Power BI / Claude insight generator / Streamlit simulator.
     Added in M1, refined in M4. -->

## The cost & margin assumption layer

The source data contains sales but not costs. Rather than inventing margins
silently, MarginIQ uses an explicit, configurable assumption layer: gross
margin ranges and perishability/waste rates per product family, sourced from
public grocery-industry benchmarks and defined in `config/cost_assumptions.yaml`.
Every dollar figure in the system is traceable to a stated assumption, and the
scenario simulator can flex those assumptions.

<!-- Benchmark sources table added in M2. -->

## Data

<!-- Source, license, table descriptions, row counts, data dictionary link,
     data quality report link. Added in M2. -->

## Warehouse & modeling

<!-- Medallion layers, star schema diagram, key SQL patterns, performance
     benchmarks (before/after indexing & partitioning). Added in M3. -->

## Semantic layer

<!-- How metrics are defined once in YAML and consumed by Power BI, the AI
     layer, and the simulator. Example metric definition. Added in M4. -->

## Analytics modules

<!-- Forecasting (incl. forecast bias cost), anomaly detection, promo
     efficiency, leakage quantification. Methodology + validation. M5. -->

## Executive dashboard

<!-- Screenshots: executive summary, leakage drill-through, forecast page,
     decision page. Each page answers: what happened / why / what to do /
     expected impact. Added in M6. -->

## AI insight generator & scenario simulator

<!-- How Claude is grounded in the semantic layer (and why that prevents
     metric hallucination). Simulator demo GIF: "what if oil +15%?" M7. -->

## Key findings

<!-- Top 5 quantified insights and recommendations, e.g. "Stockouts in the
     produce family cost an estimated $X.XM/year across 12 stores." M5–M6. -->

## Project structure

<!-- Folder tree with one-line descriptions. Added in M4. -->

## Reproducibility

<!-- Setup, data download instructions, make targets, sampling strategy
     (3-store dev sample vs full run), expected runtimes. Added in M8. -->

## Roadmap

<!-- v1.1 backlog: promo cannibalization, perishable waste model, returns
     anomaly module. Links to GitHub Issues. -->

## License & attribution

<!-- Dataset: Corporación Favorita Grocery Sales Forecasting (Kaggle).
     Code license. Industry benchmark citations. -->
