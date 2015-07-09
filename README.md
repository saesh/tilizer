# Tilizer

A program that copies every n-th frame of a movie into a image into rows and columns. The resulting image can be printed as a poster. Resolution and dimensions can be changed within the program source.

## Dependencies

Ensure OpenCV Python bindings are installed.

## Usage

```./tilizer.py /path/to/movie```

Adjust to your likings within the file:

- ```imageWidthInCm```: desired image width in centimeters
- ```imageHeightInCm```: desired image height in centimeters
- ```dpi```: dots per inch in the final image
- ```tileWidthInCm```: the width of each frame tile in centimeters