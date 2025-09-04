#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average_value = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
            int gray_value = round(average_value);
            image[i][j].rgbtBlue = gray_value;
            image[i][j].rgbtRed = gray_value;
            image[i][j].rgbtGreen = gray_value;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE new = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = new;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            int pixels = 0;
            for (int h = i - 1; h < i + 2; h++)
            {
                for (int w = j - 1; w < j + 2; w++)
                {
                    if (h >= 0 && h < height && w >= 0 && w < width)
                    {
                        sumRed += image[h][w].rgbtRed;
                        sumGreen += image[h][w].rgbtGreen;
                        sumBlue += image[h][w].rgbtBlue;
                        pixels++;
                    }
                }
            }
            temp[i][j].rgbtRed = round((float) sumRed / pixels);
            temp[i][j].rgbtGreen = round((float) sumGreen / pixels);
            temp[i][j].rgbtBlue = round((float) sumBlue / pixels);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Gx_red = 0, Gy_red = 0, Gx_green = 0, Gy_green = 0, Gx_blue = 0, Gy_blue = 0;
            for (int h = -1; h <= 1; h++)
            {
                for (int w = -1; w <= 1; w++)
                {
                    int row = i + h;
                    int col = j + w;

                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        Gx_red += Gx[h + 1][w + 1] * image[row][col].rgbtRed;
                        Gy_red += Gy[h + 1][w + 1] * image[row][col].rgbtRed;

                        Gx_green += Gx[h + 1][w + 1] * image[row][col].rgbtGreen;
                        Gy_green += Gy[h + 1][w + 1] * image[row][col].rgbtGreen;

                        Gx_blue += Gx[h + 1][w + 1] * image[row][col].rgbtBlue;
                        Gy_blue += Gy[h + 1][w + 1] * image[row][col].rgbtBlue;
                    }
                }
            }
            int red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            int green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            int blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));

            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            temp[i][j].rgbtRed = red;
            temp[i][j].rgbtGreen = green;
            temp[i][j].rgbtBlue = blue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}