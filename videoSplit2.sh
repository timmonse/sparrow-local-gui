#!/bin/bash
ffmpeg -f v4l2 -input_format mjpeg -framerate 30 -video_size 1280x720 -i /dev/video1 -pix_fmt yuyv422 -f v4l2 /dev/video2
