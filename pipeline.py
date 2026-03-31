# lógica del etl: limpieza de datos, kpis y detección de anomalías

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

PALETTE = ["#1C2F5E", "#2C7BB6", "#ABD9E9", "#FDAE61", "#D7191C", "#1A9641", "#7B2D8B"]


def load_data():
    print("Cargando datos...")
    df = pd.read_csv("data/campaigns.csv", parse_dates=["date"])
    print(f"  {len(df)} filas cargadas")
    return df


def calculate_kpis(df):
    df = df.copy()
    df["CTR"]  = (df["clicks"] / df["impressions"]).replace([np.inf, np.nan], 0).round(4)
    df["CPC"]  = (df["spend"]  / df["clicks"]).replace([np.inf, np.nan], 0).round(2)
    df["CPL"]  = (df["spend"]  / df["conversions"]).replace([np.inf, np.nan], 0).round(2)
    df["CVR"]  = (df["conversions"] / df["clicks"]).replace([np.inf, np.nan], 0).round(4)
    df["ROAS"] = ((df["conversions"] * 35) / df["spend"]).replace([np.inf, np.nan], 0).round(2)
    return df


def flag_anomalies(df):
    # día con gasto > 2 desviaciones sobre la media de su campaña
    df = df.copy()
    df["anomaly"] = False
    for campaign, group in df.groupby("campaign"):
        mean = group["spend"].mean()
        std  = group["spend"].std()
        mask = (df["campaign"] == campaign) & (df["spend"] > mean + 2 * std)
        df.loc[mask, "anomaly"] = True
    print(f"  Anomalías detectadas: {df['anomaly'].sum()}")
    return df


def campaign_summary(df):
    agg = df.groupby(["campaign", "channel"]).agg(
        total_spend  =("spend",       "sum"),
        total_impr   =("impressions",  "sum"),
        total_clicks =("clicks",       "sum"),
        total_conv   =("conversions",  "sum"),
        avg_CTR      =("CTR",          "mean"),
        avg_CPC      =("CPC",          "mean"),
        avg_CPL      =("CPL",          "mean"),
        avg_ROAS     =("ROAS",         "mean"),
        anomaly_days =("anomaly",      "sum"),
    ).reset_index().round(2)
    return agg.sort_values("total_spend", ascending=False)


def channel_summary(df):
    return df.groupby("channel").agg(
        total_spend  =("spend",       "sum"),
        total_clicks =("clicks",      "sum"),
        total_conv   =("conversions", "sum"),
        avg_CTR      =("CTR",         "mean"),
        avg_CPL      =("CPL",         "mean"),
        avg_ROAS     =("ROAS",        "mean"),
    ).reset_index().round(2).sort_values("avg_ROAS", ascending=False)


def weekly_trend(df):
    df = df.copy()
    df["week"] = df["date"].dt.to_period("W").dt.start_time
    agg = df.groupby("week").agg(
        spend       =("spend",       "sum"),
        clicks      =("clicks",      "sum"),
        conversions =("conversions", "sum"),
    ).reset_index()
    agg["CPL"] = (agg["spend"] / agg["conversions"]).replace([np.inf, np.nan], 0).round(2)
    return agg


def plot_spend_by_channel(summary):
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(summary["channel"], summary["total_spend"], color=PALETTE[:len(summary)])
    ax.bar_label(bars, fmt="$%.0f", padding=4, fontsize=9)
    ax.set_xlabel("Gasto total (USD)")
    ax.set_title("Gasto total por canal", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "spend_by_channel.png", dpi=150)
    plt.close()


def plot_roas_vs_cpl(summary):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(
        summary["avg_CPL"], summary["avg_ROAS"],
        s=summary["total_spend"] / 10,
        c=PALETTE[:len(summary)], alpha=0.8, edgecolors="white", linewidths=0.8
    )
    for _, row in summary.iterrows():
        ax.annotate(row["campaign"], (row["avg_CPL"], row["avg_ROAS"]),
                    fontsize=7.5, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("CPL promedio (USD)")
    ax.set_ylabel("ROAS promedio")
    ax.set_title("ROAS vs CPL por campaña\n(tamaño = gasto total)", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "roas_vs_cpl.png", dpi=150)
    plt.close()


def plot_weekly_trend(weekly):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax2 = ax1.twinx()
    ax1.bar(weekly["week"], weekly["spend"], width=5, color="#1C2F5E", alpha=0.7, label="Gasto")
    ax2.plot(weekly["week"], weekly["conversions"], color="#D7191C", linewidth=2,
             marker="o", markersize=4, label="Conversiones")
    ax1.set_ylabel("Gasto semanal (USD)", color="#1C2F5E")
    ax2.set_ylabel("Conversiones", color="#D7191C")
    ax1.set_title("Gasto semanal vs conversiones", fontweight="bold")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax1.get_xticklabels(), rotation=30, ha="right")
    ax1.spines[["top", "right"]].set_visible(False)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "weekly_trend.png", dpi=150)
    plt.close()


def plot_ctr_heatmap(df):
    pivot = df.pivot_table(values="CTR", index="campaign",
                           columns=df["date"].dt.month, aggfunc="mean")
    pivot.columns = ["Enero", "Febrero", "Marzo"]
    fig, ax = plt.subplots(figsize=(7, 4))
    im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([c[:22] for c in pivot.index], fontsize=8)
    plt.colorbar(im, ax=ax, label="CTR promedio")
    ax.set_title("Heatmap de CTR por campaña y mes", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ctr_heatmap.png", dpi=150)
    plt.close()


def export_excel(df, camp_sum, chan_sum, weekly):
    path = OUTPUT_DIR / "campaign_report.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        camp_sum.to_excel(writer, sheet_name="Resumen campañas", index=False)
        chan_sum.to_excel(writer, sheet_name="Resumen canales",  index=False)
        weekly.to_excel(writer,   sheet_name="Tendencia semanal", index=False)
        df[df["anomaly"]].to_excel(writer, sheet_name="Anomalías", index=False)
        df.to_excel(writer,       sheet_name="Datos + KPIs",       index=False)
    print(f"  Excel exportado → {path}")


def main():
    print("\nAd Campaign Performance Tracker")
    print(f"Ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    df       = load_data()
    df       = calculate_kpis(df)
    df       = flag_anomalies(df)
    camp_sum = campaign_summary(df)
    chan_sum  = channel_summary(df)
    weekly   = weekly_trend(df)

    print("\nResumen por campaña:")
    print(camp_sum[["campaign", "total_spend", "avg_CTR", "avg_CPL", "avg_ROAS"]].to_string(index=False))

    print("\nRanking de canales por ROAS:")
    print(chan_sum[["channel", "total_spend", "avg_ROAS", "avg_CPL"]].to_string(index=False))

    print("\nGenerando gráficos...")
    plot_spend_by_channel(chan_sum)
    plot_roas_vs_cpl(camp_sum)
    plot_weekly_trend(weekly)
    plot_ctr_heatmap(df)

    print("Exportando Excel...")
    export_excel(df, camp_sum, chan_sum, weekly)

    print("\nListo. Resultados en outputs/\n")


if __name__ == "__main__":
    main()
