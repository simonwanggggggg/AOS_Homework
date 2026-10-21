import random

# ========================================
# Reference String Generators
# ========================================
from reference.random_reference import generate_random_reference
from reference.locality_reference import generate_locality_reference
from reference.custom_reference import generate_custom_reference
from reference.access_generator import add_access_types

# ========================================
# Page Replacement Algorithms
# ========================================
from algorithms.fifo import fifo
from algorithms.mfu import mfu
from algorithms.enhanced_second_chance import enhanced_second_chance
from algorithms.lfu import lfu
from algorithms.custom_algorithm import custom_algorithm
from algorithms.custom_algorithm_v2 import custom_algorithm_v2


# ========================================
# Performance Visualization
# ========================================
from plot_results import plot_results


# ========================================
# Homework Settings
# ========================================
NUM_REFERENCES = 150000
MAX_PAGE = 1500
FRAME_SIZES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def main():

    # Fixed random seed
    random.seed(42)

    # ====================================
    # Step 1: Generate Reference Strings
    # ====================================
    print("=== Generating Reference Strings ===")

    random_ref = generate_random_reference(
        NUM_REFERENCES, MAX_PAGE
    )

    locality_ref, lengths, ranges = generate_locality_reference(
        NUM_REFERENCES, MAX_PAGE
    )

    custom_ref = generate_custom_reference(
        NUM_REFERENCES, MAX_PAGE
    )

    references = {
        "Random": add_access_types(random_ref),
        "Locality": add_access_types(locality_ref),
        "Custom": add_access_types(custom_ref)
    }

    for name, ref in references.items():
        print(f"\n{name} Reference String")
        print("Total references:", len(ref))
        print("First 20 pages:", ref[:20])

    print("\nFirst 10 Procedure Details:")

    for i in range(min(10, len(lengths))):
        print(
            f"Procedure {i+1}: "
            f"Length = {lengths[i]}, "
            f"Page Range = {ranges[i]}"
        )

    # ====================================
    # Step 2: Evaluate Algorithms
    # ====================================
    algorithms = {
        "FIFO": fifo,
        "MFU": mfu,
        "Enhanced Second-Chance": enhanced_second_chance,
        #"LFU": lfu,
        #"Custom Algorithm": custom_algorithm,
        "Custom Algorithm V2": custom_algorithm_v2
    }

    results = {}

    print("\n=== Performance Evaluation ===")

    for ref_name, reference_string in references.items():

        results[ref_name] = {}

        for algo_name, algorithm in algorithms.items():

            results[ref_name][algo_name] = []

            for frames in FRAME_SIZES:

                page_faults, interrupts, disk_writes = algorithm(
                    reference_string, frames
                )

                results[ref_name][algo_name].append({
                    "frames": frames,
                    "page_faults": page_faults,
                    "interrupts": interrupts,
                    "disk_writes": disk_writes
                })

                print(
                    f"{ref_name:8} | "
                    f"{algo_name:23} | "
                    f"Frames: {frames:3} | "
                    f"Faults: {page_faults:6} | "
                    f"Interrupts: {interrupts:6} | "
                    f"Disk Writes: {disk_writes:6}"
                )

    # ====================================
    # Step 3: Generate Charts
    # ====================================
    print("\n=== Generating Charts ===")

    plot_results(results)

    print("\nAll experiments completed!")


if __name__ == "__main__":
    main()
