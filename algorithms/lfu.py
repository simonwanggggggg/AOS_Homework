
def lfu(reference_string, num_frames):
    """
    LFU with Aging (Counter Shifting)

    Based on the textbook's suggestion:
    Shift each page's reference count
    at regular intervals.

    Rules:
    1. Every page access increases its count by 1.
    2. Every aging_interval references,
       shift all resident page counters right by 1.
    3. On replacement, evict the resident page
       with the smallest count.
    4. If counts are equal, evict the page
       that was loaded earliest.

    Returns:
        page_faults, interrupts, disk_writes
    """

    if num_frames <= 0:
        raise ValueError("num_frames must be positive")

    # =====================================
    # Aging parameter
    # =====================================

    # Experimental choice:
    # Perform aging every F references.
    aging_interval = num_frames

    # =====================================
    # Data structures
    # =====================================

    # page -> dirty bit
    memory = {}

    # page -> reference count
    frequency = {}

    # page -> time when loaded
    load_time = {}

    # =====================================
    # Statistics
    # =====================================

    page_faults = 0
    interrupts = 0
    disk_writes = 0

    aging_count = 0

    # =====================================
    # Process references
    # =====================================

    for step, (page, operation) in enumerate(
        reference_string, start=1
    ):

        if operation not in ("R", "W"):
            raise ValueError(
                "Operation must be R or W"
            )

        # ---------------------------------
        # Step 1: Periodic frequency aging
        # ---------------------------------

        # At the start of each new interval,
        # reduce the historical counts.
        if (
            step > 1
            and (step - 1) % aging_interval == 0
        ):

            for p in frequency:
                frequency[p] >>= 1

            aging_count += 1

        # ---------------------------------
        # Step 2: Page Hit
        # ---------------------------------

        if page in memory:

            frequency[page] += 1

            if operation == "W":
                memory[page] = 1

            continue

        # ---------------------------------
        # Step 3: Page Fault
        # ---------------------------------

        page_faults += 1
        interrupts += 1

        # ---------------------------------
        # Step 4: Page Replacement
        # ---------------------------------

        if len(memory) >= num_frames:

            victim = min(
                memory,
                key=lambda p: (
                    frequency[p],
                    load_time[p]
                )
            )

            # Write dirty victim to disk
            if memory[victim] == 1:
                disk_writes += 1
                interrupts += 1

            del memory[victim]
            del frequency[victim]
            del load_time[victim]

        # ---------------------------------
        # Step 5: Load new page
        # ---------------------------------

        memory[page] = (
            1 if operation == "W" else 0
        )

        frequency[page] = 1
        load_time[page] = step

    # =====================================
    # Optional debug information
    # =====================================

    if num_frames in (20, 30):

        print(
            f"[LFU with Aging] "
            f"Frames={num_frames}, "
            f"Aging Interval={aging_interval}"
        )

        print(
            f"  Aging Operations: "
            f"{aging_count}"
        )

        print(
            f"  Page Faults: "
            f"{page_faults}"
        )

        print("-" * 45)

    return page_faults, interrupts, disk_writes


if __name__ == "__main__":

    test_reference = [
        (1, "R"),
        (2, "W"),
        (3, "R"),
        (1, "R"),
        (1, "W"),
        (4, "R"),
        (2, "R")
    ]

    faults, interrupts, writes = lfu(
        test_reference, 3
    )

    print("=== LFU with Aging Test ===")
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
