from cs50 import get_int


def main():
    cardnumber = input("Number: ")

    n = str(cardnumber)
    m = len(n)

    if CheckSum(cardnumber):
        if n[0] == "4" and (m == 13 or m == 16):
            print("VISA\n")  # Check for Visa
        elif n[0] == "3" and (n[1] == "4" or n[1] == "7") and m == 15:
            print("AMEX\n")  # Check for AMEX
        elif n[0] == "5" and (n[1] in "12345") and m == 16:
            print("MASTERCARD\n")  # Check FOr MASTERCARD
        else:
            print("INVALID\n")
    else:
        print("INVALID\n")


# FUNCTIONS
def CheckSum(cardnumber):
    cdnum = str(
        cardnumber
    )  # Converting String to int to extract alternate digits through indices
    list_cddig = []
    cddig = cdnum[-2::-2]  # Accessing digits second to last
    for j in range(len(cddig)):
        list_cddig.append(int(cddig[j]))
    cddig1 = ""
    for i in list_cddig:  # Multiplying digits by 2
        dig = i * 2
        cddig1 += str(dig)
    cddig = int(cddig1)
    sum1 = sum_of_digits(cddig)
    cddig2 = int(cdnum[-1::-2])
    sum2 = sum_of_digits(cddig2)
    sumt = sum1 + sum2
    if sumt % 10 == 0:  # Seeing if Cardnumber is valid or not
        return True
    else:
        return False


def sum_of_digits(number):  # Function to find sum of numbers
    sum = 0
    while number > 0:
        digit = number % 10
        sum += digit
        number = number // 10
    return sum


main()
