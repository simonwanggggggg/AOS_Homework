
import random


def add_access_types(reference_string, write_ratio=0.3):
    """
    Add Read/Write operations to each page reference.

    R = Read
    W = Write

    write_ratio = probability of a write operation
    """

    if not 0 <= write_ratio <= 1:
        raise ValueError("write_ratio must be between 0 and 1")

    result = []

    for page in reference_string:

        if random.random() < write_ratio:
            operation = "W"
        else:
            operation = "R"

        result.append((page, operation))

    return result


if __name__ == "__main__":

    test_reference = [1, 2, 3, 1, 4, 2]

    result = add_access_types(test_reference)

    print("Original:", test_reference)
    print("With Read/Write:", result)
