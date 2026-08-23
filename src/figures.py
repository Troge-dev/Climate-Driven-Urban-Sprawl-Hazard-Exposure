"""
Figure generation for the CDO Sprawl x Hazard pipeline.
Produces the visuals used in the notebook / report / deck.

Run:
    python src/figures.py
(requires data/processed/cdo_sprawl_hazard_ready.csv -- run pipeline.py first)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from shapely import wkt

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PROCESSED = os.path.join(BASE_DIR, "data", "processed", "cdo_sprawl_hazard_ready.csv")
RAW_DIR = os.path.join(BASE_DIR, "data", "cchain_raw")
FIG_DIR = os.path.join(BASE_DIR, "figures")

TIER_COLORS = {
    "Tier 1: Monitor": "#4C8C4A",
    "Tier 2: Priority Mitigation": "#E8A33D",
    "Tier 3: Critical Intervention": "#C0392B",
}


def load_scored():
    return pd.read_csv(PROCESSED)


def fig_top_risk_bar(df, n=15):
    top = df.sort_values("risk_score", ascending=False).head(n).iloc[::-1]
    colors = [TIER_COLORS[t] for t in top["risk_tier"]]

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(top["adm4_en"], top["risk_score"], color=colors)
    ax.set_xlabel("Composite Sprawl-Hazard Risk Score")
    ax.set_title(f"Top {n} Highest-Risk Barangays — Cagayan de Oro City")
    ax.set_xlim(0, top["risk_score"].max() * 1.15)
    for i, (score, tier) in enumerate(zip(top["risk_score"], top["risk_tier"])):
        ax.text(score + 0.01, i, f"{score:.2f}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "top_risk_barangays.png"), dpi=150)
    plt.close(fig)


def fig_hazard_vs_growth(df):
    fig, ax = plt.subplots(figsize=(8, 6.5))
    for tier, color in TIER_COLORS.items():
        sub = df[df["risk_tier"] == tier]
        ax.scatter(
            sub["hazard_exposure"], sub["pop_cagr"] * 100,
            s=60, c=color, label=tier, edgecolors="white", linewidths=0.5, alpha=0.85,
        )
    ax.set_xlabel("Hazard Exposure (% area high flood/landslide risk)")
    ax.set_ylabel("Population CAGR 2000–2020 (%)")
    ax.set_title("Where Growth Meets Danger: Hazard Exposure vs. Population Growth")
    ax.legend(frameon=False, fontsize=9)
    ax.axhline(df["pop_cagr"].mean() * 100, color="grey", ls="--", lw=0.8, alpha=0.6)
    ax.axvline(df["hazard_exposure"].mean(), color="grey", ls="--", lw=0.8, alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "hazard_vs_growth.png"), dpi=150)
    plt.close(fig)


def fig_barangay_risk_map(df):
    """Poor-man's choropleth: parse each barangay polygon from brgy_geography
    and fill it by risk tier color. No GDAL/geopandas dependency."""
    geo = pd.read_csv(os.path.join(RAW_DIR, "brgy_geography.csv"))
    merged = geo.merge(df[["adm4_pcode", "risk_tier", "risk_score"]], on="adm4_pcode", how="inner")

    fig, ax = plt.subplots(figsize=(8, 9))
    patches, colors = [], []
    for _, row in merged.iterrows():
        try:
            geom = wkt.loads(row["geometry"])
        except Exception:
            continue
        polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
        for poly in polys:
            xy = list(poly.exterior.coords)
            patches.append(MplPolygon(xy, closed=True))
            colors.append(TIER_COLORS.get(row["risk_tier"], "#999999"))

    pc = PatchCollection(patches, facecolor=colors, edgecolor="#222222", linewidths=0.3)
    ax.add_collection(pc)
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.set_title("Cagayan de Oro City — Barangay Sprawl-Hazard Risk Tiers")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    handles = [plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=c, markersize=12, label=t)
               for t, c in TIER_COLORS.items()]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "cdo_risk_map.png"), dpi=150)
    plt.close(fig)


def run():
    os.makedirs(FIG_DIR, exist_ok=True)
    df = load_scored()
    fig_top_risk_bar(df)
    fig_hazard_vs_growth(df)
    fig_barangay_risk_map(df)
    print(f"Figures written to {FIG_DIR}/")


if __name__ == "__main__":
    run()
