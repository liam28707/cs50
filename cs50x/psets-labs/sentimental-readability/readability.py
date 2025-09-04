from cs50 import get_string


def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    readability = calculate_readability(letters, words, sentences)
    if readability < 0:
        print("Before Grade 1")
    elif readability > 16:
        print("Grade 16+")
    else:
        print("Grade", readability)


def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    print(letters)
    return letters


def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i].isspace():
            words += 1
    print(words)
    return words


def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] in ".?!":
            sentences += 1
    print(sentences)
    return sentences


def calculate_readability(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    readability = 0.0588 * L - 0.296 * S - 15.8
    print(readability)
    return round(readability)


main()
