# web_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from strategies.adaptive import AdaptiveStrategy
from strategies.adp import ADPStrategy
from simulation.monte_carlo import run_monte_carlo
from config.city_config import CityConfig


st.set_page_config(page_title="Energy City Optimization", layout="wide")

st.title("🏙 Energy City Optimization Platform")

# =========================
# CONFIG
# =========================

st.sidebar.header("City Configuration")

apartments = st.sidebar.slider(
    "Apartments",
    min_value=10000,
    max_value=100000,
    value=40000,
    step=5000
)

houses = st.sidebar.slider(
    "Private Houses",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=1000
)

public = st.sidebar.slider(
    "Public Buildings",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)

simulations = st.sidebar.slider(
    "Monte Carlo Simulations",
    min_value=100,
    max_value=2000,
    value=500,
    step=100
)

config = CityConfig(
    apartments=apartments,
    houses=houses,
    public=public
)
# =========================
# RUN
# =========================

if st.button("Run Simulation"):

    st.write("Running simulations...")

    # ===== Adaptive =====
    adaptive = AdaptiveStrategy(epsilon=0.1)

    energies_adapt, budgets_adapt = run_monte_carlo(
        adaptive,
        config,
        simulations=simulations
    )

    # ===== ADP =====
    adp = ADPStrategy()

    try:
        adp.weights = np.load("adp_weights.npy")
    except:
        st.warning("ADP weights not found. Using untrained ADP.")

    energies_adp, budgets_adp = run_monte_carlo(
        adp,
        config,
        simulations=simulations
    )

    st.header("📊 Strategy Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Adaptive Mean Energy", round(np.mean(energies_adapt), 3))
        st.metric("Adaptive Std", round(np.std(energies_adapt), 3))

    with col2:
        st.metric("ADP Mean Energy", round(np.mean(energies_adp), 3))
        st.metric("ADP Std", round(np.std(energies_adp), 3))

    # =========================
    # HISTOGRAM
    # =========================

    st.subheader("Energy Distribution Comparison")

    fig, ax = plt.subplots()

    ax.hist(energies_adapt, bins=30, alpha=0.6, label="Adaptive")
    ax.hist(energies_adp, bins=30, alpha=0.6, label="ADP")

    ax.set_title("Final Energy Distribution")
    ax.legend()

    st.pyplot(fig)

    # =========================
    # RISK ADJUSTED
    # =========================

    sharpe_adapt = np.mean(budgets_adapt) / np.std(budgets_adapt)
    sharpe_adp = np.mean(budgets_adp) / np.std(budgets_adp)

    st.header("📈 Risk-Adjusted Performance")

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Adaptive Sharpe-like", round(sharpe_adapt, 3))

    with col4:
        st.metric("ADP Sharpe-like", round(sharpe_adp, 3))

    # =========================
    # STATISTICAL TEST
    # =========================

    st.header("🔬 Statistical Significance")

    t_stat, p_value = stats.ttest_ind(
        energies_adapt,
        energies_adp,
        equal_var=False
    )

    mean_diff = np.mean(energies_adapt) - np.mean(energies_adp)

    pooled_std = np.sqrt(
        (np.std(energies_adapt)**2 + np.std(energies_adp)**2) / 2
    )

    cohens_d = mean_diff / pooled_std

    # 95% CI
    ci_low, ci_high = stats.t.interval(
        0.95,
        len(energies_adapt) - 1,
        loc=mean_diff,
        scale=stats.sem(energies_adapt)
    )

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric("t-statistic", round(t_stat, 4))

    with col6:
        st.metric("p-value", f"{p_value:.6f}")

    with col7:
        st.metric("Cohen's d", round(cohens_d, 3))

    st.write("95% Confidence Interval of Mean Difference:",
             (round(ci_low, 3), round(ci_high, 3)))

st.header("🌍 Multi-City Generalization Study")

if st.button("Run Generalization Study"):

    st.write("Running multi-city evaluation...")

    apartments_range = np.linspace(20000, 80000, 6).astype(int)
    houses_range = np.linspace(2000, 12000, 6).astype(int)

    heatmap = np.zeros((len(houses_range), len(apartments_range)))

    # Завантажуємо ADP
    adp = ADPStrategy()
    try:
        adp.weights = np.load("adp_weights.npy")
    except:
        st.error("Train ADP first!")
        st.stop()

    for i, h in enumerate(houses_range):
        for j, a in enumerate(apartments_range):

            config = CityConfig(
                apartments=a,
                houses=h,
                public=300
            )

            adaptive = AdaptiveStrategy(epsilon=0.1)

            energies_adapt, _ = run_monte_carlo(
                adaptive,
                config,
                simulations=300
            )

            energies_adp, _ = run_monte_carlo(
                adp,
                config,
                simulations=300
            )

            heatmap[i, j] = np.mean(energies_adapt) - np.mean(energies_adp)

    # ===== Heatmap Plot =====

    fig, ax = plt.subplots()

    c = ax.imshow(heatmap, origin="lower", aspect="auto")

    ax.set_xticks(range(len(apartments_range)))
    ax.set_xticklabels(apartments_range)

    ax.set_yticks(range(len(houses_range)))
    ax.set_yticklabels(houses_range)

    ax.set_xlabel("Apartments")
    ax.set_ylabel("Houses")
    ax.set_title("Energy Advantage of ADP over Adaptive")

    fig.colorbar(c)

    st.pyplot(fig)

# =====================================
# VOLATILITY SENSITIVITY (RESEARCH MODE)
# =====================================

st.header("📉 Volatility Sensitivity Analysis (Research Mode)")

if st.button("Run Volatility Study"):

    st.write("Running robustness evaluation...")

    volatility_levels = [0.5, 1.0, 2.0, 3.0]

    advantages = []
    relative_advantages = []
    std_adp = []
    std_adapt = []
    ci_low = []
    ci_high = []

    for v in volatility_levels:

        config = CityConfig(
            apartments=40000,
            houses=5000,
            public=300,
            volatility=v
        )

        adaptive = AdaptiveStrategy()
        adp = ADPStrategy()

        try:
            adp.weights = np.load("adp_weights.npy")
        except:
            st.error("Train ADP first!")
            st.stop()

        energies_adapt, _ = run_monte_carlo(
            adaptive,
            config,
            simulations=500
        )

        energies_adp, _ = run_monte_carlo(
            adp,
            config,
            simulations=500
        )

        mean_adapt = np.mean(energies_adapt)
        mean_adp = np.mean(energies_adp)

        advantage = mean_adapt - mean_adp
        relative = advantage / mean_adapt

        advantages.append(advantage)
        relative_advantages.append(relative)

        std_adp.append(np.std(energies_adp))
        std_adapt.append(np.std(energies_adapt))

        # 95% CI for mean difference
        diff = energies_adapt - energies_adp
        ci = 1.96 * np.std(diff) / np.sqrt(len(diff))

        ci_low.append(advantage - ci)
        ci_high.append(advantage + ci)

    # ===== Absolute Advantage Plot =====
    fig1, ax1 = plt.subplots()

    ax1.plot(volatility_levels, advantages)
    ax1.fill_between(volatility_levels, ci_low, ci_high, alpha=0.2)

    ax1.set_xlabel("Volatility Scale")
    ax1.set_ylabel("Absolute Energy Advantage (ADP)")
    ax1.set_title("Robustness to Market Volatility")

    st.pyplot(fig1)

    # ===== Relative Advantage Plot =====
    fig2, ax2 = plt.subplots()

    ax2.plot(volatility_levels, relative_advantages)

    ax2.set_xlabel("Volatility Scale")
    ax2.set_ylabel("Relative Improvement (%)")
    ax2.set_title("Relative Energy Improvement of ADP")

    st.pyplot(fig2)

    # ===== Variance Comparison =====
    fig3, ax3 = plt.subplots()

    ax3.plot(volatility_levels, std_adapt, label="Adaptive Std")
    ax3.plot(volatility_levels, std_adp, label="ADP Std")

    ax3.set_xlabel("Volatility Scale")
    ax3.set_ylabel("Energy Std")
    ax3.set_title("Strategy Stability under Volatility")
    ax3.legend()

    st.pyplot(fig3)


# =====================================
# COMPUTATIONAL COMPLEXITY ANALYSIS
# =====================================

import time

st.header("⏱ Computational Complexity Analysis")

if st.button("Run Complexity Study"):

    st.write("Measuring runtime scaling...")

    scale_levels = [20000, 40000, 60000, 80000]

    adaptive_times = []
    adp_times = []

    for scale in scale_levels:

        config = CityConfig(
            apartments=scale,
            houses=int(scale * 0.125),
            public=300,
            volatility=1.0
        )

        adaptive = AdaptiveStrategy()
        adp = ADPStrategy()

        try:
            adp.weights = np.load("adp_weights.npy")
        except:
            st.error("Train ADP first!")
            st.stop()

        # Adaptive timing
        start = time.time()
        run_monte_carlo(adaptive, config, simulations=200)
        adaptive_time = time.time() - start
        adaptive_times.append(adaptive_time)

        # ADP timing
        start = time.time()
        run_monte_carlo(adp, config, simulations=200)
        adp_time = time.time() - start
        adp_times.append(adp_time)

    # ===== Runtime Plot =====
    fig1, ax1 = plt.subplots()

    ax1.plot(scale_levels, adaptive_times, label="Adaptive")
    ax1.plot(scale_levels, adp_times, label="ADP")

    ax1.set_xlabel("Number of Apartments")
    ax1.set_ylabel("Runtime (seconds)")
    ax1.set_title("Runtime Scaling with City Size")
    ax1.legend()

    st.pyplot(fig1)

    # ===== Runtime Ratio =====
    ratio = [a2 / a1 for a1, a2 in zip(adaptive_times, adp_times)]

    fig2, ax2 = plt.subplots()

    ax2.plot(scale_levels, ratio)

    ax2.set_xlabel("Number of Apartments")
    ax2.set_ylabel("ADP / Adaptive Runtime Ratio")
    ax2.set_title("Relative Computational Overhead")

    st.pyplot(fig2)

    # ===== Text Summary =====
    st.subheader("Complexity Summary")

    st.write("Average Adaptive runtime:", round(np.mean(adaptive_times), 3), "sec")
    st.write("Average ADP runtime:", round(np.mean(adp_times), 3), "sec")
    st.write("Average ADP overhead ratio:", round(np.mean(ratio), 3))

# =====================================
# PARETO FRONTIER ANALYSIS
# =====================================

st.header("🎯 Pareto Frontier Analysis (Energy vs Budget)")

if st.button("Run Pareto Analysis"):

    st.write("Evaluating multi-objective trade-off...")

    config = CityConfig(
        apartments=40000,
        houses=5000,
        public=300,
        volatility=1.0
    )

    adaptive = AdaptiveStrategy()
    adp = ADPStrategy()

    try:
        adp.weights = np.load("adp_weights.npy")
    except:
        st.error("Train ADP first!")
        st.stop()

    energies_adapt, budgets_adapt = run_monte_carlo(
        adaptive,
        config,
        simulations=500
    )

    energies_adp, budgets_adp = run_monte_carlo(
        adp,
        config,
        simulations=500
    )

    # ===== Scatter Plot =====
    fig, ax = plt.subplots()

    ax.scatter(
        energies_adapt,
        budgets_adapt,
        alpha=0.4,
        label="Adaptive"
    )

    ax.scatter(
        energies_adp,
        budgets_adp,
        alpha=0.4,
        label="ADP"
    )

    ax.set_xlabel("Final Energy")
    ax.set_ylabel("Final Budget")
    ax.set_title("Energy vs Budget Trade-off")
    ax.legend()

    st.pyplot(fig)

    # ===== Simple Pareto Dominance Check =====
    adp_better = 0

    for ea, ba in zip(energies_adapt, budgets_adapt):
        for eb, bb in zip(energies_adp, budgets_adp):
            if (eb <= ea and bb >= ba):
                adp_better += 1
                break

    dominance_ratio = adp_better / len(energies_adapt)

    st.subheader("Pareto Dominance Summary")
    st.write("Fraction of cases where ADP dominates Adaptive:",
             round(dominance_ratio, 3))

# =====================================
# SOCIETAL HAPPINESS MODEL
# =====================================

st.header("😊 Societal Happiness Index")

if st.button("Run Happiness Evaluation"):

    config = CityConfig(
        apartments=40000,
        houses=5000,
        public=300,
        volatility=1.0
    )

    adaptive = AdaptiveStrategy()
    adp = ADPStrategy()

    try:
        adp.weights = np.load("adp_weights.npy")
    except:
        st.error("Train ADP first!")
        st.stop()

    energies_adapt, budgets_adapt = run_monte_carlo(
        adaptive,
        config,
        simulations=500
    )

    energies_adp, budgets_adp = run_monte_carlo(
        adp,
        config,
        simulations=500
    )

    # ---- Normalization ----
    max_energy = max(
        np.max(energies_adapt),
        np.max(energies_adp)
    )

    max_budget = max(
        np.max(budgets_adapt),
        np.max(budgets_adp)
    )

    energy_norm_adapt = energies_adapt / max_energy
    energy_norm_adp = energies_adp / max_energy

    budget_norm_adapt = budgets_adapt / max_budget
    budget_norm_adp = budgets_adp / max_budget

    # Risk component
    risk_adapt = np.std(energies_adapt)
    risk_adp = np.std(energies_adp)

    max_risk = max(risk_adapt, risk_adp)

    risk_norm_adapt = risk_adapt / max_risk
    risk_norm_adp = risk_adp / max_risk

    # ---- Utility Weights ----
    w_energy = 0.5
    w_budget = 0.4
    w_risk = 0.1

    happiness_adapt = (
        w_energy * (1 - np.mean(energy_norm_adapt)) +
        w_budget * np.mean(budget_norm_adapt) -
        w_risk * risk_norm_adapt
    )

    happiness_adp = (
        w_energy * (1 - np.mean(energy_norm_adp)) +
        w_budget * np.mean(budget_norm_adp) -
        w_risk * risk_norm_adp
    )

    st.subheader("Happiness Scores")

    st.write("Adaptive Happiness:", round(happiness_adapt, 4))
    st.write("ADP Happiness:", round(happiness_adp, 4))

    # ---- Bar Plot ----
    fig, ax = plt.subplots()

    ax.bar(["Adaptive", "ADP"],
           [happiness_adapt, happiness_adp])

    ax.set_ylabel("Societal Happiness Index")
    ax.set_title("Composite Urban Utility")

    st.pyplot(fig)