
from itertools import combinations
from random import sample

TREATS = [
    "cheese",
    "yoghurt",
    "peanut butter",
    "scrambled egg",
    "papadam",
    "Tyrell's chip",
    "dentastix",
    "nature's gift kangaroo",
    "dentalife",
    "ultimates chicken",
    "ultimates lamb",
    "ultimates beef",
    "greenies",
    "vitapet fish tenders",
    "vitapet chicken tenders",
    "vitapet bacon strips",
    "bowwow beef roo rolls",
    "bowwow oinkers",
    "vip chuckers",
    "liver pieces",
]

def main():
    n_days = 10
    n_per_morning = 5
    n_per_night = 5

    pairs = iter(sample(
        list(combinations(TREATS, 2)),
        n_days * (n_per_morning + n_per_night)
    ))

    for date in range(4, 14):
        header = f'{date}th of July'

        print(header)
        print(len(header) * '=')

        print()
        print('MORNING')
        
        for n in range(n_per_morning):
            left, right = next(pairs)
            print(f"{left} vs {right}")

        print()
        print('NIGHT')
        
        for n in range(n_per_morning):
            left, right = next(pairs)
            print(f"{left} vs {right}")
        
        print()
    

if __name__ == "__main__":
    main()