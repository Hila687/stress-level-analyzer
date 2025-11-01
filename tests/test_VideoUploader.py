# --- Add project root to Python path so tests can import project modules ---
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# --- Standard imports ---
import os
import io
import tempfile
import pytest
from werkzeug.datastructures import FileStorage
from VideoUploader import VideoUploader

# -----------------------------------------------------------------------------
# Fixture: provides a fresh VideoUploader instance for each test
# pytest automatically calls this function whenever a test requests 'uploader'
@pytest.fixture
def uploader(tmp_path):
    uploader = VideoUploader()
    # Use pytest's temporary directory as upload folder to avoid polluting project files
    uploader.UPLOAD_FOLDER = tmp_path  
    return uploader

# -----------------------------------------------------------------------------
# Test 1: verify that a valid video file is saved correctly
def test_save_valid_video(uploader):
    # Create a fake FileStorage object simulating an uploaded video
    fake_file = FileStorage(
        stream=io.BytesIO(b"fake video data"),
        filename="test.mp4",
        content_type="video/mp4"
    )
    # Save the file using our uploader
    path = uploader.save_video(fake_file)
    # Assert the file actually exists on disk
    assert os.path.exists(path)
    # Assert the file name keeps the correct extension
    assert path.endswith(".mp4")

# -----------------------------------------------------------------------------
# Test 2: verify that invalid file extensions are rejected
def test_reject_invalid_extension(uploader):
    fake_file = FileStorage(
        stream=io.BytesIO(b"data"),
        filename="test.txt",
        content_type="text/plain"
    )
    # Expect a ValueError when trying to save a non-video file
    with pytest.raises(ValueError):
        uploader.save_video(fake_file)

# -----------------------------------------------------------------------------
# Test 3: verify that upload folder is created automatically if missing
def test_folder_created_automatically(tmp_path):
    uploader = VideoUploader()
    # Set upload folder to a subfolder that does not exist yet
    uploader.UPLOAD_FOLDER = tmp_path / "nonexistent"
    fake_file = FileStorage(
        stream=io.BytesIO(b"data"),
        filename="test.mov",
        content_type="video/quicktime"
    )
    uploader.save_video(fake_file)
    # Assert that the folder now exists
    assert os.path.exists(uploader.UPLOAD_FOLDER)

# -----------------------------------------------------------------------------
# Test 4: verify that deleting a video file removes it from disk
def test_delete_video(uploader):
    fake_file = FileStorage(
        stream=io.BytesIO(b"some data"),
        filename="delete.mp4",
        content_type="video/mp4"
    )
    # Save and then delete the file
    path = uploader.save_video(fake_file)
    uploader.delete_video(path)
    # Assert that the file was successfully removed
    assert not os.path.exists(path)
