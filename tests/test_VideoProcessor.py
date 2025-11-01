# tests/test_VideoProcessor_samples.py
from pathlib import Path
import pytest
import numpy as np
import cv2 as cv
from VideoProcessor import VideoProcessor


def _discover_sample_videos():
    """
    Discover video files inside the 'samples' directory (relative to project root).
    Supported extensions: mp4, avi, mov, mkv.
    """
    tests_dir = Path(__file__).resolve().parent
    project_root = tests_dir.parent
    samples_dir = project_root / "samples"

    exts = ("*.mp4", "*.avi", "*.mov", "*.mkv")
    files = []
    if samples_dir.exists():
        for pat in exts:
            files.extend(samples_dir.glob(pat))
    return [str(p) for p in files]


SAMPLE_VIDEOS = _discover_sample_videos()

# Skip all tests if no videos found
pytestmark = pytest.mark.skipif(
    not SAMPLE_VIDEOS,
    reason="No sample videos found in ./samples directory"
)


@pytest.mark.parametrize("video_path", SAMPLE_VIDEOS, ids=lambda p: Path(p).name)
def test_video_opens(video_path):
    """Ensure that the video file can be opened and has a valid FPS."""
    vp = VideoProcessor(video_path)
    fps = vp.framePerSec()
    assert fps and fps > 0, f"Invalid FPS for {video_path}"


@pytest.mark.parametrize("video_path", SAMPLE_VIDEOS, ids=lambda p: Path(p).name)
def test_process_returns_frames(video_path):
    """Ensure that process() returns a non-empty list of face frames."""
    vp = VideoProcessor(video_path)
    frames = vp.process()
    assert isinstance(frames, list), "process() must return a list"
    assert len(frames) > 0, f"No face crops returned for {video_path}"
    assert all(isinstance(f, np.ndarray) and f.size > 0 for f in frames), \
        "All items must be non-empty numpy arrays"


@pytest.mark.parametrize("video_path", SAMPLE_VIDEOS, ids=lambda p: Path(p).name)
def test_faces_detected_in_first_frame_or_two(video_path):
    """
    Smoke test: verify that at least one face is detected in the first or second frame.
    This quickly checks that the Haar cascade works on this specific file.
    """
    cap = cv.VideoCapture(video_path)
    ok1, frame1 = cap.read()
    ok2, frame2 = cap.read()
    cap.release()

    assert ok1 or ok2, f"Could not read first frames from {video_path}"

    vp = VideoProcessor(video_path)
    if ok1:
        faces1 = vp.face_detector(frame1)
        if len(faces1) > 0:
            assert True
            return
    if ok2:
        faces2 = vp.face_detector(frame2)
        if len(faces2) > 0:
            assert True
            return

    pytest.fail(f"No faces detected in first frames of {video_path}")
