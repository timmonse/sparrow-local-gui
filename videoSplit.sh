#!/bin/bash
gst-launch-1.0 v4l2src device=/dev/video1 ! tee name=t ! queue ! v4l2sink device=/dev/video2
