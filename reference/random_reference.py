import random

def generate_random_reference(num_references=150000, max_page=1500):

    random_reference = []

    for i in range(num_references):
        page = random.randint(1, max_page)
        random_reference.append(page)

    return random_reference
