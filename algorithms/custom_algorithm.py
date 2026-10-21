
from collections import deque, Counter


def custom_algorithm(reference_string, num_frames):
    """
    Frame-Adaptive Window LFU (FAW-LFU)

    Window size = num_frames

    Each reference: (page, operation)
    Returns:
        page_faults, interrupts, disk_writes
    """

    if num_frames <= 0:
        raise ValueError("num_frames must be positive")

    # Adaptive window size
    window_size = num_frames + 200

    # Recent reference history
    history = deque()

    # Page frequency within the window
    frequency = Counter()

    # Resident pages: page -> dirty bit
    memory = {}

    page_faults = 0
    interrupts = 0
    disk_writes = 0

    for page, operation in reference_string:

        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")

        # Step 1: Record the current reference
        history.append(page)
        frequency[page] += 1

        # Step 2: Remove expired reference
        if len(history) > window_size:
            old_page = history.popleft()
            frequency[old_page] -= 1

            if frequency[old_page] == 0:
                del frequency[old_page]

        # Step 3: Page Hit
        if page in memory:

            if operation == "W":
                memory[page] = 1

            continue

        # Step 4: Page Fault
        page_faults += 1
        interrupts += 1

        # Step 5: Replace least frequently used page
        if len(memory) >= num_frames:

            # Tie-breaker: oldest resident page
            victim = min(
                memory,
                key=lambda p: frequency.get(p, 0)
            )

            # Write back dirty page
            if memory[victim] == 1:
                disk_writes += 1
                interrupts += 1

            del memory[victim]

        # Step 6: Load requested page
        memory[page] = 1 if operation == "W" else 0

    return page_faults, interrupts, disk_writes


if __name__ == "__main__":

    test_reference = [
        (1, "R"),
        (2, "W"),
        (1, "W"),
        (3, "R"),
        (1, "R"),
        (2, "R"),
        (4, "R")
    ]

    faults, interrupts, writes = custom_algorithm(
        test_reference, 3
    )

    print("=== FAW-LFU Test ===")
    print("Window Size:", 2 * 3 + 50)
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
