from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mumby import Mumby
from scipy.integrate import odeint
from scipy.optimize import differential_evolution

# 1. Configuration
DATA_PATH = "all_data.csv"  # <-- Change this to your dataset filename
MIN_YEARS_PER_SITE = 3  # Minimum survey years required per site
PARAM_KEYS = ["a", "g", "y", "r", "d"]


# 2. Load & Aggregate GBR Transect Data
def load_and_prepare_data(filepath, min_years=3):
    path = Path(filepath)
    if path.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, sep=None, engine="python")

    # Clean column names and drop any unnamed index column
    unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
    if unnamed:
        df = df.drop(columns=unnamed)
    df.columns = df.columns.str.strip()

    df["GROUP_CODE"] = df["GROUP_CODE"].astype(str).str.strip().str.upper()
    df["REEF"] = df["REEF"].astype(str).str.strip()
    df["REPORT_YEAR"] = pd.to_numeric(df["REPORT_YEAR"], errors="coerce")
    df["SITE_NO"] = pd.to_numeric(df["SITE_NO"], errors="coerce")
    df["cover"] = pd.to_numeric(df["cover"], errors="coerce")

    df = df[df["GROUP_CODE"].isin(["HC", "MA"])].dropna(
        subset=["REEF", "SITE_NO", "REPORT_YEAR", "cover"]
    )
    df["REPORT_YEAR"] = df["REPORT_YEAR"].astype(int)
    df["SITE_NO"] = df["SITE_NO"].astype(int)

    # Average across transects for each site-year while keeping sector/shelf metadata
    meta_cols = [
        c for c in ["P_CODE", "A_SECTOR", "SHELF"] if c in df.columns
    ]
    group_cols = meta_cols + ["REEF", "SITE_NO", "REPORT_YEAR", "GROUP_CODE"]

    df_site = (
        df.groupby(group_cols)["cover"]
        .mean()
        .unstack("GROUP_CODE")
        .reset_index()
        .dropna(subset=["HC", "MA"])
    )

    # Convert % cover to [0, 1] proportions and ensure C + M <= 1
    c_prop = np.clip(df_site["HC"].values / 100.0, 0.0, 1.0)
    m_prop = np.clip(df_site["MA"].values / 100.0, 0.0, 1.0)
    total = c_prop + m_prop
    over = total > 1.0
    if np.any(over):
        c_prop[over] /= total[over]
        m_prop[over] /= total[over]

    df_site["C_obs"] = c_prop
    df_site["M_obs"] = m_prop
    df_site["T_obs"] = np.clip(1.0 - c_prop - m_prop, 0.0, 1.0)

    # Keep sites with at least `min_years` observation years
    yr_counts = df_site.groupby(["REEF", "SITE_NO"])["REPORT_YEAR"].transform(
        "nunique"
    )
    df_valid = (
        df_site[yr_counts >= min_years]
        .sort_values(["REEF", "SITE_NO", "REPORT_YEAR"])
        .reset_index(drop=True)
    )

    site_groups = [
        (key, grp.reset_index(drop=True))
        for key, grp in df_valid.groupby(["REEF", "SITE_NO"])
    ]
    return df_valid, site_groups

# 3. Fast Vectorized Objective Function Using Mumby Parameters
def build_fast_objective(model, df_valid):
    bounds = [model.parameter_range[k] for k in PARAM_KEYS]

    # Map each (REEF, SITE_NO) to an integer index 0..n_sites-1
    df_indexed = df_valid.copy()
    df_indexed["site_idx"] = df_indexed.groupby(["REEF", "SITE_NO"]).ngroup()
    n_sites = df_indexed["site_idx"].nunique()

    min_yr = int(df_indexed["REPORT_YEAR"].min())
    max_yr = int(df_indexed["REPORT_YEAR"].max())
    n_years = max_yr - min_yr + 1

    # Initial conditions for each site at its first survey year
    first_rows = (
        df_indexed.sort_values(["site_idx", "REPORT_YEAR"])
        .groupby("site_idx")
        .first()
        .reset_index()
    )
    start_yrs = first_rows["REPORT_YEAR"].values
    c0_vec = first_rows["C_obs"].values
    m0_vec = first_rows["M_obs"].values

    obs_site_idx = df_indexed["site_idx"].values
    obs_yr_idx = df_indexed["REPORT_YEAR"].values - min_yr
    c_obs_vec = df_indexed["C_obs"].values
    m_obs_vec = df_indexed["M_obs"].values

    def loss_fn(params):
        a, g, y, r, d = [
            np.clip(val, lo, hi) for val, (lo, hi) in zip(params, bounds)
        ]

        def rhs(C, M):
            T = 1.0 - C - M
            denom = np.maximum(M + T, 1e-12)
            dC = r * T * C - d * C - a * M * C
            dM = a * M * C - (g * M) / denom + y * M * T
            return dC, dM

        substeps = 10
        dt = 1.0 / substeps
        traj_C = np.zeros((n_years, n_sites))
        traj_M = np.zeros((n_years, n_sites))

        C = c0_vec.copy()
        M = m0_vec.copy()

        init_0 = start_yrs == min_yr
        traj_C[0, init_0] = C[init_0]
        traj_M[0, init_0] = M[init_0]

        for step_yr in range(min_yr, max_yr):
            active = start_yrs <= step_yr
            for _ in range(substeps):
                k1_c, k1_m = rhs(C, M)
                k2_c, k2_m = rhs(C + 0.5 * dt * k1_c, M + 0.5 * dt * k1_m)
                k3_c, k3_m = rhs(C + 0.5 * dt * k2_c, M + 0.5 * dt * k2_m)
                k4_c, k4_m = rhs(C + dt * k3_c, M + dt * k3_m)
                C = np.where(
                    active, C + (dt / 6.0) * (k1_c + 2 * k2_c + 2 * k3_c + k4_c), C
                )
                M = np.where(
                    active, M + (dt / 6.0) * (k1_m + 2 * k2_m + 2 * k3_m + k4_m), M
                )

            if np.any(np.isnan(C)) or np.any(C < -0.05) or np.any(C > 1.05):
                return 1e6

            yr_idx = (step_yr + 1) - min_yr
            traj_C[yr_idx] = C
            traj_M[yr_idx] = M

        pred_C = traj_C[obs_yr_idx, obs_site_idx]
        pred_M = traj_M[obs_yr_idx, obs_site_idx]
        return float(
            np.sum((c_obs_vec - pred_C) ** 2 + (m_obs_vec - pred_M) ** 2)
        )

    return loss_fn, bounds


def single_site_loss(params, model, bounds, years, c_obs, m_obs):
    clipped = [
        np.clip(val, lo, hi) for val, (lo, hi) in zip(params, bounds)
    ]
    model.set_parameters(dict(zip(PARAM_KEYS, clipped)))
    sol = odeint(model.ode, [c_obs[0], m_obs[0]], years)
    if np.any(np.isnan(sol)) or np.any(sol < -0.05) or np.any(sol > 1.05):
        return 1e6
    return float(
        np.sum((c_obs - sol[:, 0]) ** 2 + (m_obs - sol[:, 1]) ** 2)
    )


# 4. Run Full Analysis Pipeline
if __name__ == "__main__":
    df_valid, site_groups = load_and_prepare_data(
        DATA_PATH, min_years=MIN_YEARS_PER_SITE
    )
    print(
        f"Loaded {len(df_valid)} site-year observations across {len(site_groups)} sites "
        f"({df_valid['REEF'].nunique()} reefs, {df_valid['REPORT_YEAR'].min()}–{df_valid['REPORT_YEAR'].max()})."
    )

    model = Mumby()
    global_loss_fn, bounds = build_fast_objective(model, df_valid)

    # Step B: Fit Global Model (with live step progress)
    print("\nFitting global GBR parameters across all sites...")
    res_global = differential_evolution(
        global_loss_fn,
        bounds,
        maxiter=100,
        popsize=8,
        tol=1e-4,
        disp=True,  # Prints live progress at each iteration
        seed=42,
    )
    global_params = dict(zip(PARAM_KEYS, res_global.x))
    global_rss = res_global.fun
    global_k = len(PARAM_KEYS)
    print(
        "\nGlobal Fitted Parameters:",
        {k: round(v, 4) for k, v in global_params.items()},
    )

    # Step C: Fit Site-Specific Models (with progress every 25 sites)
    print(f"\nFitting site-specific parameters for {len(site_groups)} sites...")
    site_records = []
    for idx, ((reef, site_no), site_df) in enumerate(site_groups, start=1):
        if idx % 25 == 0 or idx == 1 or idx == len(site_groups):
            print(f"  Progress: {idx}/{len(site_groups)} sites ({reef} - Site {site_no})")

        years = site_df["REPORT_YEAR"].values
        c_obs = site_df["C_obs"].values
        m_obs = site_df["M_obs"].values

        res_site = differential_evolution(
            single_site_loss,
            bounds,
            args=(model, bounds, years, c_obs, m_obs),
            maxiter=80,
            popsize=6,
            tol=1e-4,
            seed=42,
        )
        rec = {
            "REEF": reef,
            "SITE_NO": site_no,
            "A_SECTOR": (
                site_df["A_SECTOR"].iloc[0]
                if "A_SECTOR" in site_df.columns
                else "NA"
            ),
            "SHELF": (
                site_df["SHELF"].iloc[0] if "SHELF" in site_df.columns else "NA"
            ),
            "n_years": len(site_df),
            "max_MA": site_df["M_obs"].max(),
            "rss": res_site.fun,
        }
        rec.update(dict(zip(PARAM_KEYS, res_site.x)))
        site_records.append(rec)

    df_site_params = pd.DataFrame(site_records)
    df_site_params.to_csv("gbr_site_parameters.csv", index=False)
    print("Saved site-specific fits to 'gbr_site_parameters.csv'.")

    # Step D: Compare Global vs. Site-Specific (RSS & AIC)
    total_obs = sum(len(g) * 2 for _, g in site_groups)
    site_rss_total = df_site_params["rss"].sum()
    site_k_total = len(df_site_params) * len(PARAM_KEYS)

    aic_global = total_obs * np.log(global_rss / total_obs) + 2 * global_k
    aic_site = (
        total_obs * np.log(max(site_rss_total, 1e-12) / total_obs)
        + 2 * site_k_total
    )

    print("\n--- Model Comparison (Global vs. Site-Specific) ---")
    print(
        f"Global Model        -> RSS: {global_rss:.4f} | Params: {global_k:4d} | AIC: {aic_global:.2f}"
    )
    print(
        f"Site-Specific Model -> RSS: {site_rss_total:.4f} | Params: {site_k_total:4d} | AIC: {aic_site:.2f}"
    )

    # Step E: Summarize & Plot Variation in Site-Specific Parameters
    # Note: Macroalgal parameters (a, g, y) are only identifiable where MA > 0
    active_ma_sites = df_site_params[df_site_params["max_MA"] > 0.005]
    print(
        f"\n--- Parameter Variation Across Sites (n = {len(active_ma_sites)} sites with MA > 0.5%) ---"
    )
    summary = active_ma_sites[PARAM_KEYS].describe().T
    summary["CV"] = summary["std"] / summary["mean"]
    print(summary[["mean", "std", "min", "50%", "max", "CV"]].round(4))

    fig, axes = plt.subplots(1, 5, figsize=(15, 4))
    for ax, param in zip(axes, PARAM_KEYS):
        if "SHELF" in active_ma_sites.columns and active_ma_sites["SHELF"].nunique() > 1:
            sns.boxplot(
                data=active_ma_sites,
                x="SHELF",
                y=param,
                ax=ax,
                color="skyblue",
            )
        else:
            sns.boxplot(y=active_ma_sites[param], ax=ax, color="skyblue")
        ax.axhline(
            global_params[param],
            color="#d62728",
            linestyle="--",
            label="Global fit",
        )
        ax.set_title(f"Parameter: {param}")
    axes[0].legend(frameon=False)
    plt.tight_layout()
    plt.savefig("gbr_parameter_variation.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Step F: Generate Mumby-Style Graphs Using Fitted GBR Parameters
    # Pick the site with the highest observed macroalgae as an illustrative trajectory
    best_idx = df_site_params["max_MA"].idxmax()
    target_reef = df_site_params.loc[best_idx, "REEF"]
    target_site = df_site_params.loc[best_idx, "SITE_NO"]
    sample_df = dict(site_groups)[(target_reef, target_site)]
    site_fit = df_site_params.loc[best_idx, PARAM_KEYS].to_dict()

    model.set_parameters(site_fit)
    model.set_start_conditions(
        [sample_df["C_obs"].iloc[0], sample_df["M_obs"].iloc[0]]
    )

    # 1. Time-series fit vs. observed coral cover (Fig. 1 style)
    model.plot_fig1(
        years=[
            sample_df["REPORT_YEAR"].min(),
            sample_df["REPORT_YEAR"].max(),
        ],
        obs_years=sample_df["REPORT_YEAR"].values,
        obs_coral_pct=sample_df["C_obs"].values * 100.0,
        a_values=(site_fit["a"], min(site_fit["a"] * 1.5, 0.5)),
        save_path="gbr_fig1_site_fit.png",
    )

    # 2. Grazing hysteresis threshold for global GBR parameters (Fig. 2 style)
    model.set_parameters(global_params)
    model.plot_fig2(
        a_values=(
            global_params["a"],
            min(global_params["a"] * 1.5, 0.5),
        ),
        save_path="gbr_fig2_hysteresis.png",
    )

    # 3. Phase plane at high vs. low grazing (Fig. 3 style)
    model.plot_fig3(
        g_values=(
            global_params["g"],
            max(global_params["g"] * 0.4, 0.02),
        ),
        save_path="gbr_fig3_phase_plane.png",
    )
    print(
        "\nDone! Generated: gbr_site_parameters.csv, gbr_parameter_variation.png, "
        "gbr_fig1_site_fit.png, gbr_fig2_hysteresis.png, and gbr_fig3_phase_plane.png."
    )