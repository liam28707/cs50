#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

// Stating various functions used
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calc_readability(string text, int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words =  count_words(text);
    int sentences = count_sentences(text);
    int readability = calc_readability(text, letters, words, sentences);
    if (readability < 0)// Printing Before Grade 1
    {
        printf("Before Grade 1\n");
    }
    else if (readability > 16)// Beyond Grade 16
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", readability); // Prining readability
    }
}

int count_letters(string text) // COunting numbre of letters
{
    int letters = 0;
    int i;
    for (i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }


    }
    return letters;
}

int count_words(string text) // Counting number of words
{
    int words = 1;
    int i;
    for (i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)//COunting number of sentences
{
    int sentences = 0;
    int i;
    for (i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }

    }
    return sentences;
}

int calc_readability(string text, int letters, int words, int sentences) //Calculating readability
{
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;
    int readability = round(0.0588 * L - 0.296 * S - 15.8);
    return readability;

}