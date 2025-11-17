import pandas as pd
from pathlib import Path

# Paths are relative to backend_api/
RESULTS_FILE = Path("jmeter/data/results/jmeter_results.csv")
REPORT_FILE = Path("jmeter/data/results/performance_summary.txt")


def load_results():
    print("📊 Loading JMeter results...")
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"{RESULTS_FILE} not found. "
            "Make sure you ran JMeter and the Simple Data Writer path is correct."
        )
    df = pd.read_csv(RESULTS_FILE)
    print("✔ File loaded successfully.")
    return df


def summarize(df):
    total = len(df)
    success_rate = df["success"].mean() * 100
    avg_latency = df["elapsed"].mean()
    median_latency = df["elapsed"].median()
    p90 = df["elapsed"].quantile(0.90)
    p95 = df["elapsed"].quantile(0.95)
    p99 = df["elapsed"].quantile(0.99)

    summary = {
        "Total Requests": total,
        "Success Rate (%)": round(success_rate, 2),
        "Average Response Time (ms)": round(avg_latency, 2),
        "Median Response Time (ms)": round(median_latency, 2),
        "P90 Response Time (ms)": round(p90, 2),
        "P95 Response Time (ms)": round(p95, 2),
        "P99 Response Time (ms)": round(p99, 2),
    }

    return summary


def breakdown_by_sampler(df):
    stats = df.groupby("label")["elapsed"].agg(
        ["count", "mean", "median", "max", "min"]
    )
    return stats


def print_and_save(summary, stats):
    lines = []

    lines.append("=== PERFORMANCE SUMMARY ===")
    for k, v in summary.items():
        lines.append(f"{k}: {v}")
    lines.append("")

    lines.append("=== BREAKDOWN BY ENDPOINT (label) ===")
    lines.append(str(stats))

    report_text = "\n".join(lines)

    # Print to console
    print("\n" + report_text)

    # Save to file
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_FILE.open("w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n📝 Report written to: {REPORT_FILE}")


if __name__ == "__main__":
    df = load_results()
    summary = summarize(df)
    stats = breakdown_by_sampler(df)
    print_and_save(summary, stats)
