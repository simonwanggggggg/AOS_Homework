def mfu(reference_string, num_frames):
    if num_frames <= 0:
        raise ValueError("Number of frames must be positive")
    # Pages currently in memory: page -> dirty bit
    memory = {}
    # Frequency counter for resident pages
    frequency = {}
    # Arrival order for tie-breaking
    arrival_order = {}
    arrival_time = 0
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    for page, operation in reference_string:
        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")
        # Page Hit
        if page in memory:
            frequency[page] += 1
            if operation == "W":
                memory[page] = 1
            continue
        # Page Fault
        page_faults += 1
        interrupts += 1
        # Memory is full
        if len(memory) >= num_frames:
            # Select page with highest frequency
            # Tie-breaker: oldest resident page
            victim = max(memory,key=lambda p: (frequency[p],-arrival_order[p]))
            # Write back dirty victim
            if memory[victim] == 1:
                disk_writes += 1
                interrupts += 1
            del memory[victim]
            del frequency[victim]
            del arrival_order[victim]
        # Load new page
        memory[page] = 1 if operation == "W" else 0
        frequency[page] = 1
        arrival_order[page] = arrival_time
        arrival_time += 1
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

    faults, interrupts, writes = mfu(
        test_reference, 3
    )

    print("=== MFU Test ===")
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
