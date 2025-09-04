import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Read database file into a variable
    rows = []
    with open(sys.argv[1], "r") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as txtfile:
        seq_reader = txtfile.read()

    strs = list(rows[0].keys())[1:]

    # Find longest match of each STR in DNA sequence
    output = {}
    for str in strs:
        output[str] = longest_match(seq_reader, str)

    # Check database for matches
    for person in rows:
        matches = 0
        for str in strs:
            if int(person[str]) == output[str]:
                matches += 1

        if matches == len(strs):
            print(person["name"])
            return

    print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Iterate through the sequence
    i = 0
    while i < sequence_length:
        count = 0

        # Check for a subsequence match
        while sequence[i : i + subsequence_length] == subsequence:
            count += 1
            i += subsequence_length

        longest_run = max(longest_run, count)
        i += 1

    return longest_run


if __name__ == "__main__":
    main()
