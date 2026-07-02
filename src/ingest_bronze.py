"""
MarginIQ - M2: Bronze layer ingestion + raw data profiling.

Bronze principle: land the data EXACTLY as received. No cleaning, no type
coercion beyond what's needed to read it, no filtering. Cleaning happens in
silver, so we can always trace a number back to its raw form.

Run from the repo root:  python src/ingest_bronze.py
"""

from pathlib import Path
import duckdb

RAW_DIR = Path("data/raw")
DB_PATH = "data/marginiq.duckdb"
REPORT_PATH = Path("reports/01_raw_profiling.md")

# filename -> bronze table name
FILES = {
    "train.csv": "bronze_sales",
    "stores.csv": "bronze_stores",
    "items.csv": "bronze_items",
    "transactions.csv": "bronze_transactions",
    "oil.csv": "bronze_oil",
    "holidays_events.csv": "bronze_holidays",
}


def main() -> None:
    con = duckdb.connect(DB_PATH)
    # Be explicit about resources; DuckDB spills to disk beyond this.
    con.execute("SET memory_limit='8GB'; SET threads=4;")

    lines = ["# Raw data profiling report\n"]

    for fname, table in FILES.items():
        path = RAW_DIR / fname
        if not path.exists():
            print(f"!! missing {path} - skipping")
            continue

        print(f"Ingesting {fname} -> {table} ...")
        # read_csv with sample-based type inference; all_varchar=false is
        # fine for bronze here because we validate types in the report.
        con.execute(
            f"CREATE OR REPLACE TABLE {table} AS "
            f"SELECT * FROM read_csv_auto('{path}', sample_size=-1)"
        )

        n_rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        cols = con.execute(f"DESCRIBE {table}").fetchall()

        lines.append(f"\n## {table}  (source: {fname})\n")
        lines.append(f"- rows: **{n_rows:,}**\n")
        lines.append("| column | type | nulls | null % | distinct |")
        lines.append("|---|---|---|---|---|")

        for col_name, col_type, *_ in cols:
            nulls, distinct = con.execute(
                f'SELECT COUNT(*) - COUNT("{col_name}"), '
                f'COUNT(DISTINCT "{col_name}") FROM {table}'
            ).fetchone()
            pct = 100 * nulls / n_rows if n_rows else 0
            lines.append(
                f"| {col_name} | {col_type} | {nulls:,} | {pct:.2f}% | {distinct:,} |"
            )

    # --- Targeted checks: the three traps -----------------------------------
    lines.append("\n## Targeted integrity checks\n")

    neg = con.execute(
        "SELECT COUNT(*), MIN(unit_sales) FROM bronze_sales WHERE unit_sales < 0"
    ).fetchone()
    lines.append(f"- Negative unit_sales rows (returns): **{neg[0]:,}** (min: {neg[1]})")

    dates = con.execute(
        "SELECT MIN(date), MAX(date), COUNT(DISTINCT date) FROM bronze_sales"
    ).fetchone()
    span = con.execute(
        "SELECT DATEDIFF('day', MIN(date), MAX(date)) + 1 FROM bronze_sales"
    ).fetchone()[0]
    lines.append(
        f"- Sales date range: {dates[0]} to {dates[1]} | distinct dates: "
        f"{dates[2]:,} of {span:,} calendar days"
    )

    oil_gap = con.execute(
        "SELECT COUNT(*) FROM bronze_oil WHERE dcoilwtico IS NULL"
    ).fetchone()[0]
    lines.append(f"- Oil price rows with NULL price: **{oil_gap:,}**")

    # Sparsity: how many store-item-day combinations actually have rows vs.
    # the theoretical full grid? The gap = implicit zeros (or stockouts...).
    actual = con.execute("SELECT COUNT(*) FROM bronze_sales").fetchone()[0]
    grid = con.execute(
        "SELECT (SELECT COUNT(DISTINCT store_nbr) FROM bronze_sales) * "
        "(SELECT COUNT(DISTINCT item_nbr) FROM bronze_sales) * "
        "(SELECT COUNT(DISTINCT date) FROM bronze_sales)"
    ).fetchone()[0]
    lines.append(
        f"- Grid sparsity: {actual:,} rows vs {grid:,} possible "
        f"store-item-day slots -> **{100 * actual / grid:.1f}% dense**. "
        f"Missing rows are AMBIGUOUS: zero demand or stockout."
    )

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nDone. Report written to {REPORT_PATH}")
    con.close()


if __name__ == "__main__":
    main()