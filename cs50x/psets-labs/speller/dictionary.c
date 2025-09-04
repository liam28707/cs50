// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;
int word_count = 0;

// Choose number of buckets in hash table
const unsigned int N = (1000 * 1000);

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Creating copies of words inorder to see if it is in the dictionary
    int len = strlen(word);
    char word1[len + 1];
    strcpy(word1, word);
    int hash_index = hash(word);
    if (table[hash_index] == NULL)
    {
        return false;
    }
    // Comparing the nodes through values in the hash table
    node *cursor = table[hash_index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word1) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_index = 0;
    // Series of if and else compares an hashes words based on first four letters
    if (word[0] != '\0')
    {
        char c1 = (unsigned int)(toupper(word[0]) - 'A');

        if (word[1] != '\0')
        {
            char c2 = (unsigned int)(toupper(word[1]) - 'A');

            if (word[2] != '\0')
            {
                char c3 = (unsigned int)(toupper(word[2]) - 'A');

                if (word[3] != '\0')
                {
                    char c4 = (unsigned int)(toupper(word[3]) - 'A');
                    hash_index = ((unsigned int)(((c1 * 26 + c2) * 26 + c3) * 26) + c4);
                }
                else
                {
                    hash_index = ((unsigned int)((c1 * 26 + c2) * 26) + c3);
                }
            }
            else
            {
                hash_index = ((unsigned int)(c1 * 26) + c2);
            }
        }
        else
        {
            hash_index = (unsigned int) c1;
        }
    }

    return hash_index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Opens dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Could not load\n");
        return false;
    }
    // Creates buffer memory of BYTE Size 46 to store words in the dictionary
    char buffer[46];
    while (fscanf(dict, "%s", buffer) == 1)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(dict);
            return 1;
        }
        strcpy(n->word, buffer);
        n->next = NULL;
        unsigned int hash_index = hash(n->word);
        table[hash_index] = n;
        word_count++; // counts words
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *temp = table[i]->next;
            free(table[i]);
            table[i] = temp;
        }
    }
    return true;
}
