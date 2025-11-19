#!/usr/bin/env python3
"""
LJPW v4.0 Dynamic Model Demo
============================

This script demonstrates the new non-linear dynamic capabilities of the LJPW v4.0 model.
It simulates a "Reckless Power" scenario where high Power without Wisdom leads to a collapse in Justice.
"""

import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path to import harmonizer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harmonizer.ljpw_baselines import DynamicLJPWv3, ReferencePoints


def run_demo():
    print("=" * 60)
    print("LJPW v4.0 Dynamic Model Demo")
    print("=" * 60)
    print("Scenario: 'Reckless Power' Collapse")
    print("Description: A system starts with high Power but low Wisdom.")
    print("Prediction: Power will erode Justice once it crosses the threshold.")
    print("-" * 60)

    # Initialize simulator with v4.0 calibrated parameters
    simulator = DynamicLJPWv3()

    # Initial State: High Power (0.9), Low Wisdom (0.2), Low Love (0.2), Moderate Justice (0.5)
    initial_state = (0.2, 0.5, 0.9, 0.2)

    print(f"Initial State:")
    print(f"  Love:    {initial_state[0]:.2f}")
    print(f"  Justice: {initial_state[1]:.2f}")
    print(f"  Power:   {initial_state[2]:.2f} (High!)")
    print(f"  Wisdom:  {initial_state[3]:.2f} (Low!)")
    print()

    # Run simulation
    duration = 50
    dt = 0.05
    print(f"Simulating for {duration} time units (dt={dt})...")
    history = simulator.simulate(initial_state, duration=duration, dt=dt)

    # Get final state
    final_L = history["L"][-1]
    final_J = history["J"][-1]
    final_P = history["P"][-1]
    final_W = history["W"][-1]

    print("-" * 60)
    print(f"Final State:")
    print(f"  Love:    {final_L:.2f}")
    print(f"  Justice: {final_J:.2f} (Collapsed?)")
    print(f"  Power:   {final_P:.2f}")
    print(f"  Wisdom:  {final_W:.2f}")
    print("-" * 60)

    # Check for collapse
    if final_J < 0.3:
        print("RESULT: Justice Collapse CONFIRMED.")
        print("The high Power, unchecked by Wisdom, eroded Justice as predicted.")
    else:
        print("RESULT: Justice remained stable.")

    print("\nDisplaying trajectory plot...")
    # simulator.plot_simulation(history) # This blocks, so we manually plot and save

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(history["t"], history["L"], label="Love (L)", color="crimson", lw=2)
    ax.plot(history["t"], history["J"], label="Justice (J)", color="royalblue", lw=2)
    ax.plot(history["t"], history["P"], label="Power (P)", color="darkgreen", lw=2)
    ax.plot(history["t"], history["W"], label="Wisdom (W)", color="purple", lw=2)

    NE = ReferencePoints.NATURAL_EQUILIBRIUM
    for i, val in enumerate(NE):
        ax.axhline(
            y=val,
            color=["crimson", "royalblue", "darkgreen", "purple"][i],
            linestyle="--",
            alpha=0.3,
        )

    ax.set_title("LJPW v3.0 System Evolution (Non-Linear, RK4)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Dimension Value")
    ax.set_ylim(0, 1.2)
    ax.legend()

    output_path = "ljpw_v4_demo_plot.png"
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    run_demo()
