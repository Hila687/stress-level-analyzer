import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from StressPipeline import StressPipeline

# -----------------------------------------------------------------------------
# Test 1: Verify full pipeline runs successfully on a real sample video
def test_pipeline_on_sample_video():
    pipeline = StressPipeline(fs=30)

    # Use a real sample video from the samples directory
    video_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "samples",
        "sample_1.mp4"
    )

    # Run full analysis
    result = pipeline.analyze(video_path)

    # --- Assertions ---
    # Should return a dictionary
    assert isinstance(result, dict)

    # Should contain all expected keys
    expected_keys = {"BPM", "stress_level", "recommendations", "status"}
    assert expected_keys.issubset(result.keys())

    # Should not report error
    assert result["status"] == "ok"

    # BPM value should be positive and realistic
    assert result["BPM"] > 0 and result["BPM"] < 250

    # stress_level must be one of the expected categories
    assert result["stress_level"] in ["low", "medium", "high"]

    # recommendations should be a non-empty list
    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0


# -----------------------------------------------------------------------------
# Test 2: Verify pipeline handles invalid or empty input gracefully
def test_pipeline_handles_invalid_input():
    pipeline = StressPipeline(fs=30)

    # Case 1: Non-existing video path
    fake_path = "samples/non_existent_video.mp4"
    result = pipeline.analyze(fake_path)

    assert isinstance(result, dict)
    assert result["status"] == "error"
    assert "No such file" in result["message"] or "cannot open" in result["message"].lower()

    # Case 2: Empty frame list (simulating video with 0 frames)
    empty_frames = []
    result = pipeline.analyze(empty_frames)

    assert isinstance(result, dict)
    assert result["status"] == "error"
    assert "no frames" in result["message"].lower()

# -----------------------------------------------------------------------------
# Test 3 (disabled for now): Validate that pipeline output matches known BPM and stress level
# This test requires a reference video with known heart rate measurements.
# Once available, uncomment and adjust expected_BPM / expected_stress_level accordingly.

"""
def test_pipeline_matches_known_values():
    pipeline = StressPipeline(fs=30)

    # Path to the calibration / reference video (with known BPM)
    video_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "samples",
        "calibration_sample.mp4"
    )

    # Expected values measured manually or with external device
    expected_BPM = 78
    expected_stress_level = "medium"

    result = pipeline.analyze(video_path)

    # Ensure pipeline runs successfully
    assert result["status"] == "ok"

    # Allow small deviation (±5 BPM)
    assert abs(result["BPM"] - expected_BPM) <= 5

    # Stress level should match expected classification
    assert result["stress_level"] == expected_stress_level
"""

# -----------------------------------------------------------------------------
# To run the tests, use the command:
# pytest tests/test_StressPipeline.py


