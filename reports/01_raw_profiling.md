# Raw data profiling report


## bronze_sales  (source: train.csv)

- rows: **125,497,040**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| id | BIGINT | 0 | 0.00% | 125,497,040 |
| date | DATE | 0 | 0.00% | 1,684 |
| store_nbr | BIGINT | 0 | 0.00% | 54 |
| item_nbr | BIGINT | 0 | 0.00% | 4,036 |
| unit_sales | DOUBLE | 0 | 0.00% | 258,474 |
| onpromotion | BOOLEAN | 21,657,651 | 17.26% | 2 |

## bronze_stores  (source: stores.csv)

- rows: **54**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| store_nbr | BIGINT | 0 | 0.00% | 54 |
| city | VARCHAR | 0 | 0.00% | 22 |
| state | VARCHAR | 0 | 0.00% | 16 |
| type | VARCHAR | 0 | 0.00% | 5 |
| cluster | BIGINT | 0 | 0.00% | 17 |

## bronze_items  (source: items.csv)

- rows: **4,100**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| item_nbr | BIGINT | 0 | 0.00% | 4,100 |
| family | VARCHAR | 0 | 0.00% | 33 |
| class | BIGINT | 0 | 0.00% | 337 |
| perishable | BIGINT | 0 | 0.00% | 2 |

## bronze_transactions  (source: transactions.csv)

- rows: **83,488**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| date | DATE | 0 | 0.00% | 1,682 |
| store_nbr | BIGINT | 0 | 0.00% | 54 |
| transactions | BIGINT | 0 | 0.00% | 4,993 |

## bronze_oil  (source: oil.csv)

- rows: **1,218**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| date | DATE | 0 | 0.00% | 1,218 |
| dcoilwtico | DOUBLE | 43 | 3.53% | 998 |

## bronze_holidays  (source: holidays_events.csv)

- rows: **350**

| column | type | nulls | null % | distinct |
|---|---|---|---|---|
| date | DATE | 0 | 0.00% | 312 |
| type | VARCHAR | 0 | 0.00% | 6 |
| locale | VARCHAR | 0 | 0.00% | 3 |
| locale_name | VARCHAR | 0 | 0.00% | 24 |
| description | VARCHAR | 0 | 0.00% | 103 |
| transferred | BOOLEAN | 0 | 0.00% | 2 |

## Targeted integrity checks

- Negative unit_sales rows (returns): **7,795** (min: -15372.0)
- Sales date range: 2013-01-01 to 2017-08-15 | distinct dates: 1,684 of 1,688 calendar days
- Oil price rows with NULL price: **43**
- Grid sparsity: 125,497,040 rows vs 367,017,696 possible store-item-day slots -> **34.2% dense**. Missing rows are AMBIGUOUS: zero demand or stockout.