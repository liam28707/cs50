#include <cs50.h>
#include <stdio.h>

int main(void)
{
//Obtain height of pyramid b/w 1 and 8
    int h;
    do
    {
        h  = get_int("Height: ");
    }
//Prompt user to enter values only between 1 and 8
    while (h < 1 || h > 8);
//Build Pyramid
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h - i - 1; j++) //Leaves appropriate space
        {
            printf(" ");
        }

        for (int j = 0; j <= i; j++) // prints left pyramid
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j <= i; j++)  //prints right pyramid
        {
            printf("#");
        }
        printf("\n");
    }

}