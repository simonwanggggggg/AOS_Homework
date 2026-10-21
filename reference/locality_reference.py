import random

def generate_locality_reference(num_references=150000, max_page=1500):

    locality_reference = []
    procedure_lengths = []
    procedure_ranges = []

    # Procedure length: 1/200 to 1/100 of total references
    min_length = num_references // 200
    max_length = num_references // 100

    while len(locality_reference) < num_references:

        # Generate random procedure length
        procedure_length = random.randint(min_length, max_length)

        # Select 20 consecutive pages
        start_page = random.randint(1, max_page - 19)

        # Limit the total number of references
        remaining = num_references - len(locality_reference)
        procedure_length = min(procedure_length, remaining)

        # Generate page references
        for i in range(procedure_length):
            page = random.randint(start_page, start_page + 19)
            locality_reference.append(page)

        procedure_lengths.append(procedure_length)
        procedure_ranges.append((start_page, start_page + 19))

    return locality_reference, procedure_lengths, procedure_ranges

