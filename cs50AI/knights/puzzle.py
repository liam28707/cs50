from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # Either a Knight Or a Knave
    Not(And(AKnight, AKnave)),  # Cannot be both
    Implication(
        AKnight, And(AKnave, AKnight)
    ),  # If a Knight tehn the statement is true as a knight only tells the truth
    Implication(
        AKnave, Not(And(AKnave, AKnight))
    ),  # If a Knave then the statement is false as a  Knave only tells lies
)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # Has to be either a Knight or Knave (A)
    Not(And(AKnight, AKnave)),  # Cannot be both (A)
    Or(BKnight, BKnave),  # Has to be either a Knight or Knave (B)
    Not(And(BKnight, BKnave)),  # Cannot be both (B)
    Implication(
        AKnight, And(AKnave, BKnave)
    ),  # If A is a Knight then Both A & B are Knaves as a Knigth only  tells the truth
    Implication(
        AKnave, Not(And(AKnave, BKnave))
    ),  # If A is a Knave then Both A & B aren't Knaves as a Knave only tells a lie
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # Has to be either a Knight or Knave (A)
    Not(And(AKnight, AKnave)),  # Cannot be both (A)
    Or(BKnight, BKnave),  # Has to be either a Knight or Knave (B)
    Not(And(BKnight, BKnave)),  # Cannot be both (B)

    # A Said they both are the same
    Implication(
        AKnight, And(AKnight, BKnight)
    ),  # If A is a Knight then both B & A must be Knights as they are the same
    Implication(
        AKnave, Not(And(AKnave, BKnave))
    ),  # If A is a Knave then B is a Knight as they are the same kind but a Knave tells Lies

    # B said they are both different
    Implication(
        BKnight, And(BKnight, AKnave)
    ),  # If B is a Knight then A must be a Knave as they are different kinds
    Implication(BKnave, Not(And(BKnave, AKnight))),
        # If B is a Knave then A cant be a Knight as a Knave lies so they must be the same and not different
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # Has to be either a Knight or Knave (A)
    Not(And(AKnight, AKnave)),  # Cannot be both (A)

    Or(BKnight, BKnave),  # Has to be either a Knight or Knave (B)
    Not(And(BKnight, BKnave)),  # Cannot be both (B)

    Or(CKnight, CKnave),  # Has to be either a Knight or Knave (C)
    Not(And(CKnight, CKnave)),  # Cannot be both (C)

    # A says I am a Knight or A Knave but you dont Know which
    Or(And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))), # If A is a Knight
       And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))), # If A is a Knave
       ),
    Not(And(
        And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))), # Opposite of previous lines used to show that one of these needs to be false and the other true
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),


    # B says that A is a Knave
    Implication(BKnight,And(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave)))), # If B is a Knight
    Implication(BKnave,Not(And(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave))))), # If B is a Knave

    #C says that A is a Knight
    Implication(CKnight,AKnight), #If C is a Knight
    Implication(CKnave,Not(AKnight)), #If C is a Knight   (Error: Put Knave instead of Knight which altered output)

    # B says that C is a Knave
    Implication(BKnight,CKnave), #If B is a Knight
    Implication(BKnave,Not(CKnave)) #If B is Knave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
