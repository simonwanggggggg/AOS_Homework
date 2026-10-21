from collections import deque, Counter
def custom_algorithm_v2(reference_string, num_frames):
    """
    DACR: Dirty-Aware Cost-adaptive Replacement
    Replacement decision considers:
    1. Recent access frequency
    2. Recency of page access
    3. Dirty bit
    4. Recent disk write pressure
    """
    if num_frames <= 0:
        raise ValueError("num_frames must be positive")
    # Parameters
    window_size = 2 * num_frames
    ## Recent eviction outcomes used to estimate
    ## disk write pressure
    pressure_window = max(20, 4 * num_frames)
    ## Maximum allowable difference in reuse score
    ## between a candidate and the lowest-score page
    candidate_margin = 0.25
    # Data structures
    ## Resident pages: page -> dirty bit
    memory = {}
    ## Last access time of each resident page
    last_used = {}
    ## Recent reference history
    history = deque()
    frequency = Counter()
    ## Recent eviction outcomes:
    ## 1 = dirty page evicted
    ## 0 = clean page evicted
    eviction_history = deque(maxlen=pressure_window)
    # Statistics
    page_faults = 0
    interrupts = 0
    disk_writes = 0
    replacement_count = 0
    changed_victim_count = 0
    clean_evictions = 0
    dirty_evictions = 0
    # Process reference string
    for step, (page, operation) in enumerate(reference_string, start=1):
        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")
        ## Step 1: Update reference history
        history.append(page)
        frequency[page] += 1
        if len(history) > window_size:
            old_page = history.popleft()
            frequency[old_page] -= 1
            if frequency[old_page] == 0:
                del frequency[old_page]
        ## Step 2: Page hit
        if page in memory:
            last_used[page] = step
            if operation == "W":
                memory[page] = 1
            continue
        ## Step 3: Page fault
        page_faults += 1
        interrupts += 1
        ## Step 4: Replacement
        if len(memory) >= num_frames:
            replacement_count += 1
            resident_pages = list(memory.keys())
            ### Highest resident frequency for
            ### normalization
            max_frequency = max(frequency.get(p, 0) for p in resident_pages)
            max_frequency = max(1, max_frequency)
            ### Calculate page reuse scores
            reuse_scores = {}
            for p in resident_pages:
                #### Frequency score: 0 ~ 1
                freq_score = frequency.get(p, 0) / max_frequency
                #### Recency score
                age = step - last_used[p]
                recency_score = 1.0 / (1.0 + age / num_frames)
                #### Combined reuse score
                #### Prioritize frequency over recency
                reuse_scores[p] = 0.65 * freq_score + 0.35 * recency_score
            ### Baseline victim: lowest predicted reuse value
            normal_victim = min(resident_pages,key=lambda p: (reuse_scores[p],last_used[p]))
            minimum_score = reuse_scores[normal_victim]
            ### Candidate protection
            #### Only pages with sufficiently low
            #### reuse scores are eligible
            candidates = [
                p for p in resident_pages
                if reuse_scores[p] <= minimum_score + candidate_margin
            ]
            ### Estimate disk write pressure
            if eviction_history:
                write_pressure = sum(eviction_history) / len(eviction_history)
            else:
                write_pressure = 0.0
            #### Higher write pressure means stronger penalty for dirty pages
            dirty_penalty = 0.15 + 0.55 * write_pressure
            ### Dirty-aware victim selection
            victim = min(candidates,key=lambda p: (reuse_scores[p] + dirty_penalty * memory[p], last_used[p]))
            if victim != normal_victim:
                changed_victim_count += 1
            ### Evict selected page
            was_dirty = memory[victim]
            if was_dirty == 1:
                disk_writes += 1
                interrupts += 1
                dirty_evictions += 1
            else:
                clean_evictions += 1
            ### Update recent write pressure
            eviction_history.append(was_dirty)
            del memory[victim]
            del last_used[victim]
        ## Step 5: Load the requested page
        memory[page] = 1 if operation == "W" else 0
        last_used[page] = step
    return page_faults, interrupts, disk_writes

if __name__ == "__main__":

    test_reference = [
        (5, "R"),
        (8, "R"),
        (3, "R"),
        (5, "W"),
        (5, "W"),
        (4, "R"),
        (5, "W")
    ]

    faults, interrupts, writes = (
        custom_algorithm_v2(test_reference, 3)
    )

    print("=== DACR Test ===")
    print("Page Faults:", faults)
    print("Interrupts:", interrupts)
    print("Disk Writes:", writes)
