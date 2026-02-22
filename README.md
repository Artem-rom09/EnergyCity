# EnergyCity
GENIUS olympiad task
# 🏙 Energy City Optimization Platform

Stochastic multi-objective optimization of urban energy policy using Approximate Dynamic Programming (ADP).

---

## 📌 Project Overview

This project models long-term energy policy decisions in a city under uncertainty.

The system simulates:
- 3 building types (apartments, houses, public buildings)
- Stochastic energy price dynamics
- Limited investment budget
- Long-term energy efficiency measures

The goal is to compare:

- **Adaptive (Greedy) Strategy**
- **ADP (Approximate Dynamic Programming) Strategy**

---

## 🧠 Research Question

Can a long-term dynamic policy outperform greedy short-term optimization under stochastic energy prices?

---

## ⚙ Model Structure

### City Model
- Energy consumption per building type
- Budget constraints
- Adoption rates of energy-saving measures

### Price Model
- Stochastic exponential growth
- Common + local shocks
- Configurable volatility scale

### Simulation
- Monte Carlo simulation (hundreds to thousands of scenarios)
- Multi-year planning horizon

---

## 📊 Implemented Research Modules

### 🏙 Energy Optimization
Baseline comparison of Adaptive vs ADP strategies.

### 🌍 Multi-City Generalization
Tests performance across different city sizes.

### 📉 Volatility Sensitivity
Evaluates robustness under increasing market uncertainty.

### ⏱ Computational Complexity
Measures runtime scaling and overhead.

### 🎯 Pareto Analysis
Energy vs Budget dominance analysis.

### 😊 Societal Happiness Index
Composite urban utility metric.

---

## 📈 Key Results

- ADP dominates Adaptive in 100% of Monte Carlo simulations
- Statistically significant improvement (p < 0.001)
- Higher risk-adjusted performance
- ~30% higher composite societal utility
- Robust under volatility changes
- Scalable to larger city sizes

---

## 🧪 Training

ADP is trained using:
- ε-greedy exploration
- Approximate value function
- Temporal-difference updates

Training convergence demonstrated via smoothed reward curve.

---

## 🚀 How to Run

### Install dependencies

```bash
pip install numpy matplotlib
