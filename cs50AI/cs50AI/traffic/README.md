# Convolutional Neural Network Optimzation and Testing

## Convolutional and Pooling Layers

Using 2 Convolutional and Pooling layers instead of 1 improved accuracy, minimised loss and reduced runtime per epoch. However adding a third layer resulted in a drop in accuracy

## Filters and Kernel Sizes
Using 64 Filters and 3x3 Kernel Sizes , resulted in not a significant improvment in accuracy with longer runtimes. Using 32 Filters and 5x5 didnt show any significant changes either.

## Pooling Size
Using a larger pooling size resulted in a change in accuracy along with increased loss

## Hidden Layers & Sizes
Increasing or Decreasing Neuron Count from 128 in a single layer proved to be detrimental to accuracy. However increasing the the number of hidden layers to 2 with 128 neurons each resulted in increase of accuracy with minimised loss

## Final
2 Convolutional and Pooling Layers, with 32 Filters and 3x3 Kernels. Pooling size of 2x2.
Used 2 Hidden Layers with 128 Neurons each
