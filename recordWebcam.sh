#!/bin/bash
ffmpeg -y -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video2 ~/Sparrow_Master/output/video.avi
