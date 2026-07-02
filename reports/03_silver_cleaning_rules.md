# Data dictionary — bronze layer

Source: Corporación Favorita Grocery Sales Forecasting (Kaggle).
Grain, meaning, and caveats below reflect findings from `01_raw_profiling.md`.

## bronze_sales (train.csv) — 125,497,040 rows
Grain: one row per store, item, and date **where at least one unit moved**.
Absence of a row is ambiguous (no demand vs. stockout) — see cleaning rule R6.

| column | type | meaning | caveats |
|---|---|---|---|
| id | BIGINT | surrogate row id from source | no business meaning; dropped in silver |
| date | DATE | transaction date | 4 missing dates = Dec 25 closures (R1) |
| store_nbr | BIGINT | store identifier, joins to bronze_stores | 54 stores |
| item_nbr | BIGINT | item identifier, joins to bronze_items | only 4,036 of 4,100 catalog items ever appear (R5) |
| unit_sales | DOUBLE | units sold; fractional = weight-based items (e.g., kg of produce) | negative = returns OR inventory adjustments (R3); do not round |
| onpromotion | BOOLEAN | item on promotion that day at that store | NULL for entire 2013-01-01..2014-03-31 era = untracked, not un-promoted (R2) |

## bronze_stores (stores.csv) — 54 rows
Grain: one row per store.

| column | type | meaning | caveats |
|---|---|---|---|
| store_nbr | BIGINT | store identifier | |
| city / state | VARCHAR | store location (22 cities, 16 states) | enables geo analysis |
| type | VARCHAR | store format A–E | format definitions not documented by source |
| cluster | BIGINT | source-provided grouping of similar stores (17) | clustering method undocumented; use with care |

## bronze_items (items.csv) — 4,100 rows
Grain: one row per catalog item.

| column | type | meaning | caveats |
|---|---|---|---|
| item_nbr | BIGINT | item identifier | ~64 items never sold anywhere (R5) |
| family | VARCHAR | product family (33, e.g., GROCERY I, PRODUCE) | key for the cost & margin assumption layer |
| class | BIGINT | finer category (337) | |
| perishable | BIGINT | 1 = perishable | drives waste assumptions; source weights perishables 1.25 in scoring |

## bronze_transactions (transactions.csv) — 83,488 rows
Grain: one row per store per date; count of till transactions.

| column | type | meaning | caveats |
|---|---|---|---|
| date | DATE | | 1,682 distinct dates vs 1,684 in sales — minor mismatch, investigate in silver |
| store_nbr | BIGINT | | |
| transactions | BIGINT | store footfall proxy | useful denominator for per-basket metrics |

## bronze_oil (oil.csv) — 1,218 rows
Grain: one row per trading day; WTI oil price (Ecuador is oil-dependent).

| column | type | meaning | caveats |
|---|---|---|---|
| date | DATE | trading date | weekends/market holidays absent |
| dcoilwtico | DOUBLE | WTI price USD | 43 NULLs; forward-filled in silver (R4) |

## bronze_holidays (holidays_events.csv) — 350 rows
Grain: one row per holiday/event per locale.

| column | type | meaning | caveats |
|---|---|---|---|
| date | DATE | official date | 312 distinct dates — some dates host multiple events |
| type | VARCHAR | Holiday / Event / Transfer / Additional / Bridge / Work Day | "Transfer" rows: celebration moved to another date (R7) |
| locale | VARCHAR | National / Regional / Local | match to store's state/city for relevance |
| locale_name | VARCHAR | which country/state/city it applies to | |
| description | VARCHAR | event name | |
| transferred | BOOLEAN | TRUE = official date not actually celebrated | must pair with Transfer rows to get true celebrated dates |
