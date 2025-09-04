#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper Usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    char *Image = argv[1];

    // Open requested File
    FILE *cardptr = fopen(argv[1], "rb");
    if (cardptr == NULL)
    {
        printf("Could not open %s.\n", Image);
        return 1;
    }
    BYTE buffer[512];
    int jpegCount = 0;
    FILE *jpegPtr = NULL;
    // Iterate over the file in blocks of 512
    while (fread(buffer, sizeof(BYTE), 512, cardptr) == 512)
    {
        // Check if the current block starts with JPEG signs
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] >= 0xe0 && buffer[3] <= 0xef))
        {
            // Close previous JPEG file
            if (jpegPtr != NULL)
            {
                fclose(jpegPtr);
            }
            // Create new jpeg file
            char filename[8];
            sprintf(filename, "%03d.jpg", jpegCount);
            jpegPtr = fopen(filename, "wb");

            if (jpegPtr == NULL)
            {
                printf("Could not create %s.\n", filename);
                fclose(cardptr);
                return 1;
            }
            jpegCount++;
        }

        if (jpegPtr != NULL)
        {
            fwrite(buffer, sizeof(BYTE), 512, jpegPtr);
        }
    }
    fclose(cardptr);
    if (jpegPtr != NULL)
    {
        fclose(jpegPtr);
    }
    return 0;
}