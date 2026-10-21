import random

def generate_custom_reference(
    num_references=150000,
    max_page=1500,
    hot_pages=20,
    hot_probability=0.8,
    seed=None
):
    """
    Generate a Hotspot + Noise Reference String.
    Hotspot:
        Frequently access pages 1 to hot_pages.
    Noise:
        Occasionally access pages hot_pages+1 to max_page.
    Returns:
        List of page numbers.
    """
    # Validate parameters
    if num_references <= 0:
        raise ValueError("num_references must be positive")
    if not 1 <= hot_pages < max_page:
        raise ValueError("hot_pages must be between 1 and max_page-1")
    if not 0 <= hot_probability <= 1:
        raise ValueError("hot_probability must be between 0 and 1")
    # Use an independent random generator when seed is given
    rng = random.Random(seed) if seed is not None else random
    reference_string = []
    for _ in range(num_references):
        # Hotspot access
        if rng.random() < hot_probability:
            page = rng.randint(1, hot_pages)
        # Noise access
        else:
            page = rng.randint(hot_pages + 1, max_page)
        reference_string.append(page)
    return reference_string


if __name__ == "__main__":

    reference = generate_custom_reference(
        num_references=150000,
        max_page=1500,
        hot_pages=20,
        hot_probability=0.8,
        seed=42
    )

    hot_count = sum(1 for page in reference if 1 <= page <= 2)

    noise_count = len(reference) - hot_count

    print("=== Hotspot + Noise Reference String ===")

    print("Total references:", len(reference))
    print("First 20 pages:", reference[:20])

    print("Hotspot references:", hot_count)
    print("Noise references:", noise_count)

    print("Hotspot ratio:",f"{hot_count / len(reference) * 100:.2f}%")

    print("Noise ratio:",f"{noise_count / len(reference) * 100:.2f}%")

    print("Minimum page:", min(reference))
    print("Maximum page:", max(reference))

    # Verify homework requirements
    assert len(reference) >= 150000
    assert all(1 <= page <= 1500 for page in reference)
