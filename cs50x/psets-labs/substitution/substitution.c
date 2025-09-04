#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string ciphertext(string plaintext, string key); // Encryption function
int main(int argc, string argv[])
{
    if (argc != 2) // Key cant have numbers or be blank
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    string key = argv[1];
    int len = strlen(key);
    if (len != 26) // Key must have 26 characters
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    for (int i = 0; i < 26; i++) // Key cant have numbers
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabetic characters\n");
            return 1;
        }
    }

    for (int i = 0; i < 25; i++) // Key cant have duplicate characters
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (tolower(key[i]) == tolower(key[j]))
            {
                printf("Key must not contain duplicate characters\n");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: "); // Print ciphered Text
    string encryption = ciphertext(plaintext, key);
    printf("ciphertext: %s\n", encryption);

    return 0;
}
string ciphertext(string plaintext, string key) // Defining Function

{
    char map[26];
    for (int i = 0; i < 26; i++) //
    {
        if (islower(key[i]))
        {
            map[i] = tolower(key[i]); // Array of lower case characters
        }
        else
        {
            map[i] = toupper(key[i]); // Array of upper case characters
        }
    }
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char char_of_text = plaintext[i]; // COnverting text into characters
        if (isalpha(char_of_text))
        {
            if (islower(char_of_text)) // Converting Lowercase to Lowercase only
            {
                int index = char_of_text - 'a';
                plaintext[i] = tolower(map[index]);
            }
            else // Converting Uppercase to uppercase only
            {
                int index = char_of_text - 'A';
                plaintext[i] = toupper(map[index]);
            }
        }
    }
    return plaintext;
}