# socket-video-streamer
OpenCV + socket to stream video

## Setup

* Required: Python 3.8

```shell script
cd socket-video-streamer
pipenv install
```

* In `sender.py`, change the value of `PATH_TO_VIDEO_FILE` to either:
    * a string to a video file;
    * an integer corresponding to your video capture device (webcam?).

## Usage

> First, start the receiver **then** the sender.

```python
pipenv run python receiver.py
```


```python
pipenv run python sender.py
```