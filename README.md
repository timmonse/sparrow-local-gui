# SparrowV2 | GUI

The Sparrow GUI is a graphical user interface designed to run locally on the NVIDIA Jetson TX-2 used as an ALPR board.

# Sparrow Project Poster

![Sparrow Poster](https://i.imgur.com/fU2PXGP.jpg)

## Dependencies

The following are a list of packages/programs that are needed to use the GUI and recording/alpr features (this may not be comprehensive)

```bash
openalpr
v4l2loopback
PySimpleGUI
   opencv
   Tkinter
ffmpeg (v 4+ specifically)
imutils
createVCamera*
recordWebcam*
videoSplit2*
```
*These programs are simple bash scripts included with the repo
