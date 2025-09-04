import cs50

while True:  # Get Height and ensure proper input
    h = cs50.get_int("Height: ")
    if h >= 1 and h <= 8:
        break

for i in range(1, h + 1):
    for j in range(h - i, 0, -1):  # Leave Neccessary space
        print(" ", end="")
    for j in range(1, i + 1):  # print left pyramid
        print("#", end="")
    print(" ", end=" ")  # leave appropriate gap
    for j in range(i, 0, -1):  # print right pyramid
        print("#", end="")
    print()
