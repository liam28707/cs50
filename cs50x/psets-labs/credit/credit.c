#include <cs50.h>
#include <stdio.h>

bool CheckSum(long Cardnumber) //Defining Checksum as a function
{
    long c = Cardnumber;
    long c2 = Cardnumber; // assigning card number to another variable to perform two sets of operations on it
    int sum = 0;
    bool alt = false;

    while (c > 0) // Finding sum of alternate digits from second to last
    {
        int digit = c % 10;
        if (alt)
        {
            digit = digit * 2;
            if (digit > 9)
            {
                digit = digit % 10 + digit / 10;
            }
            sum = sum + digit;
        }
        c = c / 10;
        alt = !alt; // Make alt True and False alternately
    }

    int sum2 = 0;
    bool alt2 = true;

    while (c2 > 0) // Finding sum of alternate digits from first to second last
    {
        int digit2 = c2 % 10;
        if (alt2)
        {
            sum2 = digit2 + sum2;
        }
        c2 = c2 / 10;
        alt2 = !alt2; // Make alt True and False alternately
    }
    return (sum + sum2) % 10 == 0;
}
int main(void)
{
//Chcking if card number is valid,if so which type of card
    long Cardnumber = get_long("Number: ");
    if (CheckSum(Cardnumber))
    {
        if ((Cardnumber >= 4000000000000 && Cardnumber <= 4999999999999) ||
            (Cardnumber > 4000000000000000 && Cardnumber <= 4999999999999999))
        {
            printf("VISA\n");// Check for Visa
        }
        else if ((Cardnumber >= 340000000000000 && Cardnumber <= 349999999999999) ||
                 (Cardnumber >= 370000000000000 && Cardnumber <= 379999999999999))
        {
            printf("AMEX\n");//Check for American Express
        }
        else if (Cardnumber >= 5100000000000000 && Cardnumber <= 5599999999999999)
        {
            printf("MASTERCARD\n");//Check for Mastercard
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}