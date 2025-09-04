#include <stdio.h>
#include <cs50.h>
int get_startingsize(void);
int get_endingsize(int s);


int main(void)
{
    int s = get_startingsize();
    int e = get_endingsize(s);
// starting time = 0
    int n = 0;
// calculating time
    while (s < e)
    {
        s = s + (s / 3) - (s / 4);
        n++;

    }
// printing time taken
    printf("Years: %i", n);
    printf("\n");
}

// Starting Size(s)
int get_startingsize(void)
{
    int s;
    do
    {
        s = get_int("Starting Size: ");
    }
    while (s < 9);
    return s;
}

// Ending Size(e)
int get_endingsize(int s)
{
    int e;
    do
    {
        e = get_int("Ending size: ");
    }
    while (e < s);
    return e;
}





