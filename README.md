# MarginIQ — Profit Leakage & Decision Intelligence Platform

> Most dashboards tell you what happened. MarginIQ tells you where the business
> is losing money, why, and what fixing it is worth — in dollars.

## Why this exists

Every operations-heavy business loses margin in the same few ways: it forecasts
demand it doesn't get right, runs out of what customers actually wanted, gives
away more discount than the sales lift justifies, and absorbs losses from
returns and irregular transactions. These leaks are individually small and
invisible on standard revenue dashboards — which is exactly why they persist
year after year.

MarginIQ detects each leak, converts it into a dollar estimate using explicit
and auditable assumptions, and ranks the fixes by financial impact. The engine
is domain-agnostic by design: industry knowledge lives in configuration, so the
same system could audit a manufacturer, a logistics network, or a subscription
business.

**The demonstration case.** MarginIQ is demonstrated on 125 million real
transactions from Corporación Favorita, a 54-store grocery chain in Ecuador
(2013–2017). Grocery retail runs on 2–4% net margins — for a chain this size,
a 1% margin leak is not a rounding error; it is the entire profit line. As a
bonus, Ecuador's oil-dependent economy makes the included oil-price data a
genuine external economic factor.

**Who uses it:**

- CFO — "Where are we losing money, ranked by dollar impact?"
- VP Supply Chain — "Which stores and items bleed through stockouts and waste?"
- Head of Merchandising — "Which promotions actually made money?"
- Category managers — daily drill-down and recommendation queue

## Leakage categories (v1.0)

1. **Stockout opportunity cost** — items with healthy sales velocity that go
   silent mid-assortment; lost units estimated against the pair's own baseline.
2. **Promotion inefficiency** — promotions whose incremental margin did not
   cover the discount given away (tracked era: Apr 2014 onward).
3. **Forecast bias cost** — systematic over/under-forecasting converted to
   dollars: waste on perishables, lost sales on stockouts.
4. **Returns & anomaly loss** — quantified returns cost, separated from
   inventory adjustments; statistical anomaly flagging on store-item margins.

Backlog (v1.1): promotion cannibalization, perishable waste model, tail-bleed
discontinuation analysis.

## Architecture

*In progress — diagram and narrative land with Milestone 3–4.*
Raw CSVs → DuckDB medallion warehouse (bronze / silver / gold) → Python
analytics engine → governed semantic layer (YAML metrics) → Power BI executive
dashboard · AI insight generator · scenario simulator.

## The cost & margin assumption layer

The source data contains sales but not costs. Rather than inventing margins
silently, MarginIQ uses an explicit, configurable assumption layer: gross
margin ranges and perishability/waste rates per product family, sourced from
public grocery-industry benchmarks and defined in `config/cost_assumptions.yaml`.
Every dollar figure in the system is traceable to a stated assumption, and the
scenario simulator can flex those assumptions.

## Data

- Source: [Corporación Favorita Grocery Sales Forecasting](https://www.kaggle.com/c/favorita-grocery-sales-forecasting) (Kaggle)
- 125,497,040 sales rows · 54 stores · 4,100 items · 4.6 years · plus store,
  item, footfall, oil-price, and holiday tables
- [Raw profiling report](reports/01_raw_profiling.md) — row counts, null
  analysis, integrity checks on all six source tables
- [Data dictionary](reports/02_data_dictionary.md) — every column's business
  meaning and caveats
- [Silver cleaning rules](reports/03_silver_cleaning_rules.md) — every
  transformation decision, each traceable to a profiling finding

Selected profiling findings: promotion tracking only exists from Apr 2014
(nulls before are *untracked*, not un-promoted); four missing dates are all
Dec 25 store closures; extreme negative sales are inventory adjustments, not
customer returns; ~64 catalog items never sold a single unit in 4.6 years.

## Warehouse & modeling

*In progress — Milestone 3: star schema, assortment windows, transformation
SQL, performance benchmarks.*

## Semantic layer

*In progress — Milestone 4: governed metric definitions in YAML, consumed by
the dashboard, the AI layer, and the simulator.*

## Analytics modules

*In progress — Milestone 5: demand baselines, stockout detection, promotion
efficiency, forecast bias costing, returns anomaly flagging.*

## Executive dashboard

*In progress — Milestone 6: Power BI decision pages. Every page answers: what
happened, why, what to do, and what it's worth.*

## AI insight generator & scenario simulator

*In progress — Milestone 7: Claude-powered Q&A grounded in the semantic layer;
what-if simulator (oil price, demand, promo depth).*

## Key findings

*Populated in Milestones 5–6 — top quantified leaks and recommended actions.*

## Project structure

```
marginiq/
├── src/          # ingestion & transformation code
├── reports/      # profiling, dictionary, cleaning rules, findings
├── config/       # assumptions & metric definitions (YAML)
└── data/         # local only — never committed (see .gitignore)
```

## Reproducibility

*Full guide lands in Milestone 8.* Current quick start: clone the repo, place
the extracted Kaggle CSVs in `data/raw/`, then `pip install -r
requirements.txt` and `python src/ingest_bronze.py` — produces the bronze
warehouse and the profiling report. Developed in Kaggle Notebooks (data
pre-attached), productionized locally.

## Roadmap

- [x] M1 — Business framing & architecture
- [x] M2 — Bronze layer, profiling, data dictionary, cleaning rules
- [ ] M3 — Silver/gold warehouse & transformation SQL
- [ ] M4 — Semantic layer & Python package
- [ ] M5 — Analytics & leakage quantification
- [ ] M6 — Power BI executive dashboard
- [ ] M7 — AI insight generator & scenario simulator
- [ ] M8 — Packaging, case study & release v1.0

## License & attribution

Dataset © Corporación Favorita via Kaggle, used under the competition's terms
for educational/portfolio purposes. Code: MIT License. Industry margin
benchmarks cited in `config/cost_assumptions.yaml` (Milestone 4).
