import csv
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def read_csv(filename):
    with open(DATA_DIR / filename, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


all_records = read_csv("standardized_components.csv")
valid_records = read_csv("valid_components.csv")
invalid_records = read_csv("validation_report.csv")

total = len(all_records)
valid = len(valid_records)
invalid = len(invalid_records)

if total == 0:
    raise ValueError("No component records found.")

if valid + invalid != total:
    raise ValueError(
        "Record counts do not match. Rerun quality_control.py."
    )

print("\nMARITIME METADATA QUALITY REPORT")
print("=" * 45)

print(f"Total records: {total}")
print(f"Valid records: {valid}")
print(f"Invalid records: {invalid}")
print(f"Validation success rate: {valid / total * 100:.2f}%")

print("\nERROR BREAKDOWN")
print("-" * 45)

error_counts = Counter()

for record in invalid_records:
    for error in record["errors"].split("; "):
        if not error.strip():
            continue

        error_type = error.split(":")[0]
        error_counts[error_type] += 1

for error, count in error_counts.most_common():
    print(f"{error}: {count}")

print("\nCOMPONENTS BY CATEGORY")
print("-" * 45)

category_counts = Counter(
    record["category"] for record in all_records
)

for category, count in category_counts.most_common():
    print(f"{category}: {count}")

print("\nINVALID RECORDS BY CATEGORY")
print("-" * 45)

records_by_id = {
    record["component_id"]: record
    for record in all_records
}

invalid_category_counts = Counter()

for record in invalid_records:
    component_id = record["component_id"]
    original = records_by_id.get(component_id)

    if original:
        invalid_category_counts[original["category"]] += 1

for category, count in invalid_category_counts.most_common():
    category_total = category_counts[category]
    failure_rate = count / category_total * 100

    print(f"{category}: {count} invalid ({failure_rate:.2f}%)")

print("\nREPORT COMPLETE")


REPORT_OUTPUT = DATA_DIR / "quality_summary.csv"

with open(REPORT_OUTPUT, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "category",
        "total_records",
        "invalid_records",
        "valid_records",
        "failure_rate_percent"
    ])

    for category, count in sorted(category_counts.items()):
        invalid_count = invalid_category_counts[category]
        valid_count = count - invalid_count
        failure_rate = round(invalid_count / count * 100, 2)

        writer.writerow([
            category,
            count,
            invalid_count,
            valid_count,
            failure_rate
        ])

print(f"CSV summary saved to {REPORT_OUTPUT.name}")
