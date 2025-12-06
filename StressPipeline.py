import os
import json
from VideoProcessor import VideoProcessor
from SignalExtractor import SignalExtractor
from HeartRateAnalyzer import HeartRateAnalyzer
from StressLevelEstimator import StressLevelEstimator


class StressPipeline:
    def __init__(self, fs=30):
        self.signal_extractor = SignalExtractor(fs=fs)
        self.hr_analyzer = HeartRateAnalyzer(fs=fs)
        self.stress_estimator = StressLevelEstimator()

        # Load recommendations JSON once at startup
        json_path = os.path.join(os.path.dirname(__file__), "ResultFormatter.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.recommendations = json.load(f)

    def analyze(self, video_input):
        """
        Full pipeline:
        1. Validate input
        2. Load frames (via VideoProcessor or direct frames)
        3. Extract and filter rPPG signal
        4. Compute BPM
        5. Classify stress level
        6. Return recommendations
        """

        try:
            # ---------------------------------------------------------
            # Step 0: Validate input path
            if isinstance(video_input, str):
                if not os.path.isfile(video_input):
                    return {
                        "status": "error",
                        "message": f"No such file: {video_input}"
                    }

                video_processor = VideoProcessor(video_input)
                frames = video_processor.process()

            else:
                # Input is already a list of frames
                frames = video_input

            # ---------------------------------------------------------
            # Step 1: Validate frames list
            if not frames or len(frames) == 0:
                return {
                    "status": "error",
                    "message": "No frames available for processing."
                }

            # ---------------------------------------------------------
            # Step 2: Extract rPPG signal
            rppg_signal = self.signal_extractor.extract_rppg(frames)

            # ---------------------------------------------------------
            # Step 3: Compute BPM (❤️ using the correct method name!)
            bpm = self.hr_analyzer.compute_bpm(rppg_signal)

            # ---------------------------------------------------------
            # Step 4: Estimate stress level
            stress_level = self.stress_estimator.estimate(bpm)

            # Normalize key for JSON lookup
            stress_key = stress_level.lower().strip()


            # ---------------------------------------------------------
            # Step 5: Build final response
            rec = self.recommendations.get(stress_level, {})

            return {
                "BPM": round(bpm, 2),
                "stress_level": rec.get("stress level", stress_level).lower(),
                "recommendations": rec.get("recommendations", []),
                "status": "ok"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
