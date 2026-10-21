from collections import deque

def fifo(reference_string, num_frames):
    if num_frames <= 0:
        raise ValueError("Number of frames must be positive")
    # Dictionary: page -> dirty bit
    memory = {}
    # FIFO replacement order
    queue = deque()
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    for page, operation in reference_string:
        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")
        # Page Hit
        if page in memory:
            # Writing makes the page dirty
            if operation == "W":
                memory[page] = 1
            continue
        # Page Fault
        page_faults += 1
        interrupts += 1
        # Memory is full
        if len(memory) >= num_frames:
            oldest_page = queue.popleft()
            # Write dirty page back to disk
            if memory[oldest_page] == 1:
                disk_writes += 1
                interrupts += 1
            del memory[oldest_page]
        # Load new page
        dirty_bit = 1 if operation == "W" else 0
        memory[page] = dirty_bit
        queue.append(page)
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

    faults, interrupts, writes = fifo(
        test_reference, 3
    )

    print("=== FIFO Test ===")
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
