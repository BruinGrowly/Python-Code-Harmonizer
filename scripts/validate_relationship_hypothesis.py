#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relationship Hypothesis Validation Script

Tests the hypothesis: "Coupling coefficients can be derived from constant ratios"

This script:
1. Calculates all ratios between LJPW constants
2. Compares them to current coupling coefficients
3. Fits various relationship functions
4. Validates which model best explains the coupling structure
"""

import math
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List


# LJPW Constants (Natural Equilibrium)
class Constants:
    L = (math.sqrt(5) - 1) / 2  # 0.618034
    J = math.sqrt(2) - 1  # 0.414214
    P = math.e - 2  # 0.718282
    W = math.log(2)  # 0.693147


# Current Coupling Matrix (from ljpw_baselines.py)
COUPLING_MATRIX = {
    "LL": 1.0,
    "LJ": 1.4,
    "LP": 1.3,
    "LW": 1.5,
    "JL": 0.9,
    "JJ": 1.0,
    "JP": 0.7,
    "JW": 1.2,
    "PL": 0.6,
    "PJ": 0.8,
    "PP": 1.0,
    "PW": 0.5,
    "WL": 1.3,
    "WJ": 1.1,
    "WP": 1.0,
    "WW": 1.0,
}


def calculate_all_ratios() -> Dict[str, float]:
    """Calculate ratios between all pairs of constants"""
    dims = {"L": Constants.L, "J": Constants.J, "P": Constants.P, "W": Constants.W}
    ratios = {}

    for i in dims:
        for j in dims:
            ratios[f"{i}{j}"] = dims[i] / dims[j]

    return ratios


def extract_coupling_data() -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Extract (ratio, coupling) pairs for analysis

    Returns:
        ratios: Array of constant ratios
        couplings: Array of coupling coefficients
        labels: List of dimension pair labels
    """
    const_ratios = calculate_all_ratios()

    ratios = []
    couplings = []
    labels = []

    for key in COUPLING_MATRIX:
        ratios.append(const_ratios[key])
        couplings.append(COUPLING_MATRIX[key])
        labels.append(key)

    return np.array(ratios), np.array(couplings), labels


# ============================================================================
# Relationship Function Models
# ============================================================================


def identity_model(r, a, b):
    """κ = a*r + b (Linear relationship)"""
    return a * r + b


def power_model(r, a, n):
    """κ = a * r^n (Power law)"""
    return a * (r**n)


def reciprocal_model(r, a, b):
    """κ = a/r + b (Inverse relationship)"""
    return a / r + b


def sigmoid_model(r, a, k, r0):
    """κ = a / (1 + exp(-k*(r-r0))) (Sigmoidal saturation)"""
    return a / (1 + np.exp(-k * (r - r0)))


def hybrid_model(r, a1, a2, b):
    """κ = a1*r + a2/r + b (Combines direct and inverse)"""
    return a1 * r + a2 / r + b


def log_model(r, a, b):
    """κ = a*log(r) + b (Logarithmic relationship)"""
    return a * np.log(r) + b


# ============================================================================
# Model Fitting and Evaluation
# ============================================================================


def fit_model(model, ratios, couplings, p0=None):
    """
    Fit a relationship model to the data

    Returns:
        params: Fitted parameters
        rmse: Root mean square error
        r2: R-squared score
    """
    try:
        params, _ = curve_fit(model, ratios, couplings, p0=p0, maxfev=10000)
        predictions = model(ratios, *params)

        # Calculate metrics
        residuals = couplings - predictions
        rmse = np.sqrt(np.mean(residuals**2))
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((couplings - np.mean(couplings)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return params, rmse, r2, predictions
    except Exception as e:
        print(f"Failed to fit model: {e}")
        return None, float("inf"), 0, None


def evaluate_all_models(ratios, couplings):
    """Fit and evaluate all candidate models"""

    models = {
        "Linear (κ = a*r + b)": (identity_model, None),
        "Power Law (κ = a*r^n)": (power_model, [1.0, 1.0]),
        "Reciprocal (κ = a/r + b)": (reciprocal_model, None),
        "Sigmoid (κ = a/(1+e^(-k*(r-r0))))": (sigmoid_model, [1.0, 1.0, 1.0]),
        "Hybrid (κ = a1*r + a2/r + b)": (hybrid_model, [0.5, 0.5, 0.0]),
        "Logarithmic (κ = a*log(r) + b)": (log_model, None),
    }

    results = {}

    print("=" * 80)
    print("MODEL EVALUATION: Coupling = f(Ratio)")
    print("=" * 80)
    print()

    for name, (model, p0) in models.items():
        params, rmse, r2, predictions = fit_model(model, ratios, couplings, p0)

        if params is not None:
            results[name] = {
                "model": model,
                "params": params,
                "rmse": rmse,
                "r2": r2,
                "predictions": predictions,
            }

            print(f"{name}")
            print(f"  Parameters: {params}")
            print(f"  RMSE: {rmse:.4f}")
            print(f"  R²: {r2:.4f}")
            print()

    return results


def analyze_diagonal_vs_offdiagonal(ratios, couplings, labels):
    """Analyze if diagonal elements (LL, JJ, PP, WW) follow different pattern"""

    diagonal_mask = [label[0] == label[1] for label in labels]
    offdiagonal_mask = [not d for d in diagonal_mask]

    diag_ratios = ratios[diagonal_mask]
    diag_couplings = couplings[diagonal_mask]

    offdiag_ratios = ratios[offdiagonal_mask]
    offdiag_couplings = couplings[offdiagonal_mask]

    print("=" * 80)
    print("DIAGONAL vs OFF-DIAGONAL ANALYSIS")
    print("=" * 80)
    print()

    print("DIAGONAL ELEMENTS (self-coupling):")
    diagonal_labels = [label for label, is_diagonal in zip(labels, diagonal_mask) if is_diagonal]
    for i, label in enumerate(diagonal_labels):
        print(f"  {label}: ratio={diag_ratios[i]:.4f}, κ={diag_couplings[i]:.4f}")
    print("  All diagonal couplings = 1.0 (by definition)")
    print()

    print("OFF-DIAGONAL ELEMENTS (cross-coupling):")
    # Fit linear model to off-diagonal only
    if len(offdiag_ratios) > 0:
        params, rmse, r2, _ = fit_model(identity_model, offdiag_ratios, offdiag_couplings)
        print(f"  Best fit: κ = {params[0]:.3f}*r + {params[1]:.3f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²: {r2:.4f}")
    print()


def find_special_patterns(ratios, couplings, labels):
    """Look for special patterns in the coupling-ratio relationship"""

    print("=" * 80)
    print("SPECIAL PATTERNS ANALYSIS")
    print("=" * 80)
    print()

    # Group by source dimension
    for source in ["L", "J", "P", "W"]:
        mask = [label[0] == source for label in labels]
        source_ratios = ratios[mask]
        source_couplings = couplings[mask]
        source_labels = [label for label, include in zip(labels, mask) if include]

        print(f"Source: {source} (outgoing influence)")
        for i, label in enumerate(source_labels):
            print(
                f"  {label}: r={source_ratios[i]:.3f} → κ={source_couplings[i]:.3f} "
                f"(diff: {source_couplings[i] - source_ratios[i]:+.3f})"
            )
        print()


def visualize_results(ratios, couplings, labels, results):
    """Create visualization of relationship between ratios and coupling"""

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("Coupling Coefficient vs. Constant Ratio Analysis", fontsize=16, fontweight="bold")

    # Plot 1: Scatter with diagonal highlighted
    ax = axes[0, 0]
    diagonal = [label[0] == label[1] for label in labels]
    ax.scatter(
        ratios[~np.array(diagonal)],
        couplings[~np.array(diagonal)],
        alpha=0.6,
        s=100,
        label="Off-diagonal",
        color="blue",
    )
    ax.scatter(
        ratios[diagonal],
        couplings[diagonal],
        alpha=0.8,
        s=100,
        label="Diagonal (self)",
        color="red",
        marker="s",
    )

    # Add labels for each point
    for i, label in enumerate(labels):
        ax.annotate(
            label, (ratios[i], couplings[i]), xytext=(5, 5), textcoords="offset points", fontsize=8
        )

    ax.plot([0, 2], [0, 2], "k--", alpha=0.3, label="κ = r (identity)")
    ax.set_xlabel("Constant Ratio (Ci/Cj)", fontsize=12)
    ax.set_ylabel("Coupling Coefficient κij", fontsize=12)
    ax.set_title("Raw Data: Coupling vs. Ratio", fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot best models
    model_names = list(results.keys())[:5]
    for idx, name in enumerate(model_names):
        row = (idx + 1) // 3
        col = (idx + 1) % 3
        ax = axes[row, col]

        result = results[name]
        predictions = result["predictions"]

        # Scatter actual vs predicted
        ax.scatter(couplings, predictions, alpha=0.6, s=100)
        ax.plot([0, 2], [0, 2], "r--", alpha=0.5, label="Perfect prediction")

        # Add labels
        for i, label in enumerate(labels):
            if abs(couplings[i] - predictions[i]) > 0.2:  # Highlight large errors
                ax.annotate(
                    label,
                    (couplings[i], predictions[i]),
                    xytext=(5, 5),
                    textcoords="offset points",
                    fontsize=8,
                    color="red",
                    fontweight="bold",
                )

        ax.set_xlabel("Actual Coupling κ", fontsize=10)
        ax.set_ylabel("Predicted κ", fontsize=10)
        ax.set_title(
            f"{name}\nRMSE={result['rmse']:.3f}, R²={result['r2']:.3f}",
            fontsize=10,
            fontweight="bold",
        )
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("/workspace/coupling_ratio_analysis.png", dpi=150, bbox_inches="tight")
    print("\n✓ Visualization saved to: /workspace/coupling_ratio_analysis.png")
    plt.close()


# ============================================================================
# Main Analysis
# ============================================================================


def main():
    """Run complete relationship analysis"""

    print("\n" + "=" * 80)
    print("LJPW RELATIONSHIP HYPOTHESIS VALIDATION")
    print("Insight: 'Relationships between constants matter more than constants themselves'")
    print("=" * 80 + "\n")

    # Calculate ratios
    all_ratios = calculate_all_ratios()
    print("CONSTANT RATIOS:")
    print("-" * 40)
    dims = ["L", "J", "P", "W"]
    const_vals = {"L": Constants.L, "J": Constants.J, "P": Constants.P, "W": Constants.W}
    for d in dims:
        print(f"{d} = {const_vals[d]:.6f}")
    print()

    print("Key Ratios:")
    print(f"  L/J = {all_ratios['LJ']:.4f}")
    print(f"  L/P = {all_ratios['LP']:.4f}")
    print(f"  L/W = {all_ratios['LW']:.4f}")
    print(f"  P/J = {all_ratios['PJ']:.4f}")
    print(f"  W/J = {all_ratios['WJ']:.4f}")
    print(f"  W/P = {all_ratios['WP']:.4f}")
    print()

    # Extract data
    ratios, couplings, labels = extract_coupling_data()

    # Run analyses
    analyze_diagonal_vs_offdiagonal(ratios, couplings, labels)
    find_special_patterns(ratios, couplings, labels)
    results = evaluate_all_models(ratios, couplings)

    # Find best model
    best_model_name = min(results.keys(), key=lambda k: results[k]["rmse"])
    best_result = results[best_model_name]

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print(f"Best Model: {best_model_name}")
    print(f"  RMSE: {best_result['rmse']:.4f}")
    print(f"  R²: {best_result['r2']:.4f}")
    print(f"  Parameters: {best_result['params']}")
    print()

    if best_result["r2"] > 0.5:
        print("✓ STRONG RELATIONSHIP DETECTED")
        print("  The coupling coefficients CAN be partially derived from constant ratios.")
        print("  This supports the insight: relationships are more fundamental than absolutes.")
    elif best_result["r2"] > 0.3:
        print("~ MODERATE RELATIONSHIP DETECTED")
        print("  There is some connection between ratios and coupling,")
        print("  but additional factors influence the coupling structure.")
    else:
        print("✗ WEAK RELATIONSHIP")
        print("  Coupling coefficients appear to be independent of constant ratios.")
        print("  Additional theoretical work needed to understand coupling origins.")

    print()
    print("IMPLICATIONS:")
    if best_result["r2"] > 0.3:
        print("  • Parameter reduction possible: coupling ≈ f(ratio)")
        print("  • System exhibits scale invariance")
        print("  • Proportions more fundamental than magnitudes")
        print("  • Cross-domain applicability via ratio preservation")
    else:
        print("  • Current coupling coefficients are independently calibrated")
        print("  • May represent emergent properties beyond simple ratios")
        print("  • Further research needed to find deeper unifying principle")

    # Visualize
    visualize_results(ratios, couplings, labels, results)

    print("\n" + "=" * 80)
    print("Analysis complete. See RELATIONSHIP_ANALYSIS.md for detailed interpretation.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
