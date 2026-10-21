def enhanced_second_chance(reference_string, num_frames):
    if num_frames <= 0:
        raise ValueError("Number of frames must be positive")
    memory = []
    pointer = 0
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    for page, operation in reference_string:
        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")
        # Check Page Hit
        hit = False
        for frame in memory:
            if frame[0] == page:
                frame[1] = 1
                if operation == "W":
                    frame[2] = 1
                hit = True
                break
        if hit:
            continue
        # Page Fault
        page_faults += 1
        interrupts += 1
        dirty = 1 if operation == "W" else 0
        # Empty frame available
        if len(memory) < num_frames:
            memory.append([page, 1, dirty])
            continue
        # Enhanced Second-Chance victim selection
        while True:
            victim_index = None
            # Pass 1: Search for (R=0, M=0)
            # Do not modify R bits
            for _ in range(num_frames):
                frame = memory[pointer]
                if frame[1] == 0 and frame[2] == 0:
                    victim_index = pointer
                    break
                pointer = (pointer + 1) % num_frames
            if victim_index is not None:
                break
            # Pass 2: Search for (R=0, M=1)
            # Clear R bits while scanning
            for _ in range(num_frames):
                frame = memory[pointer]
                if frame[1] == 0 and frame[2] == 1:
                    victim_index = pointer
                    break
                frame[1] = 0
                pointer = (pointer + 1) % num_frames
            if victim_index is not None:
                break
        # Write back dirty page
        if memory[victim_index][2] == 1:
            disk_writes += 1
            interrupts += 1
        # Replace victim
        memory[victim_index] = [page, 1, dirty]
        # Advance clock pointer
        pointer = (victim_index + 1) % num_frames
    return page_faults, interrupts, disk_writes


if __name__ == "__main__":

    test_reference = [
        (1, "R"),
        (2, "W"),
        (3, "R"),
        (1, "W"),
        (4, "R"),
        (5, "R"),
        (6, "R")
    ]

    faults, interrupts, writes = enhanced_second_chance(
        test_reference, 3
    )

    print("=== Enhanced Second-Chance Test ===")
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
