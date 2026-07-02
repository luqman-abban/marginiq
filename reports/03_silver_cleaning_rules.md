# Silver layer — cleaning & transformation rules

Every rule below is traceable to a finding in `01_raw_profiling.md`.
These rules are the specification for the M3 transformation SQL.
Principle: silver never destroys information — it makes ambiguity explicit.

## R1 — Calendar with is_open flag
Finding: exactly 4 dates missing from sales (Dec 25 of 2013–2016).
Rule: build a dim_date spanning 2013-01-01..2017-08-15 with `is_open`
(FALSE on Dec 25). All baseline/velocity calculations exclude closed days.
Rationale: closed days are not zero-demand days; including them biases
every daily average downward.

## R2 — Promotion tracking era
Finding: onpromotion is NULL for the entire 2013-01-01..2014-03-31 span,
then never again. Clean cutoff = system go-live, not data corruption.
Rule: add `promo_tracked` flag (date >= 2014-04-01). Within the tracked
era, keep onpromotion as-is. Before it, set onpromotion to NULL and
promo_tracked to FALSE. The promo inefficiency module reads ONLY the
tracked era.
Rationale: NULL means untracked, not un-promoted. Imputing FALSE would
poison promo baselines with unlabeled promotions.

## R3 — Returns vs. adjustments
Finding: 7,795 negative unit_sales rows; extreme value -15,372 on a single
store-item-day is not plausible customer returns.
Rule: classify negatives into `return` (small magnitude) vs `adjustment`
(extreme magnitude). Initial threshold: |unit_sales| above the pair's own
99.9th percentile of positive daily sales => adjustment. Threshold is a
config value, revisited in M5 with distribution analysis.
Rationale: returns are a leakage signal; adjustments are accounting noise
that would wildly overstate returns loss if mixed in.

## R4 — Oil price fill
Finding: 43 NULL prices; gaps are weekends/market holidays (no trading).
Rule: forward-fill (last observed price carries forward). Keep a
`oil_price_filled` flag on filled rows.
Rationale: the last traded price IS the prevailing price on non-trading
days; interpolation would invent prices using future information (leakage
into forecasting features).

## R5 — Dead catalog items
Finding: 4,100 catalog items, only 4,036 ever sold.
Rule: keep all items in dim_item with flag `ever_sold`. Never-sold items
are excluded from demand models but reported to the tail-bleed module.
Rationale: dead catalog weight is itself a (minor) finding; deleting it
hides it.

## R6 — Assortment windows (the core rule)
Finding: sales grid is ~34% dense; missing store-item-day rows are
ambiguous (no demand vs. stockout vs. not stocked).
Rule: derive per store-item pair: first_sale_date, last_sale_date, and
active flag. Gap interpretation:
  - before first_sale_date: not introduced -> ignore
  - after last_sale_date: discontinued -> exclude from stockouts, feed
    tail-bleed
  - inside the window: candidate event, scored in M5 against the pair's
    own sales velocity (a gap is suspicious in proportion to how unusual
    silence is for that pair)
Do NOT densify the grid with zeros in silver.
Rationale: zero-filling manufactures false events — discontinued items
would look like catastrophic failures and never-stocked items like empty
shelves; the stockout model would train on false alarms.

## R7 — True holiday dates
Finding: holidays include type=Transfer and transferred=TRUE rows; the
official date and the celebrated date can differ.
Rule: build dim_holiday resolving to CELEBRATED dates: transferred=TRUE
rows lose their holiday effect; type=Transfer rows carry it. Bridge and
Additional days count as holiday-effect days; type=Work Day is a
compensating workday (not a holiday effect).
Rationale: demand responds to when people actually celebrate, not to the
statute book.

## R8 — Keep unit_sales fractional
Finding: 258k distinct unit_sales values; DOUBLE type.
Rule: no rounding. Fractional units are weight-based sales.
Rationale: rounding silently corrupts produce volumes — a top family for
this retailer.

## Out of scope for silver (deferred)
- transactions vs sales date mismatch (1,682 vs 1,684): investigate in M3.
- Store openings mid-period (new stores will show as all-gap early eras;
  handled naturally by R6 assortment windows — verify in M3).
