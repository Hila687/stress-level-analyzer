class StressLevelEstimator:
    def estimate(self, bpm: float) -> str:
        """
        Estimate stress level based on BPM value.

        Args:
            bpm (float): Heart rate in beats per minute.

        Returns:
            str: "High", "Medium", or "Low" stress level.
        """
        if bpm > 100:
            return "High"
        elif bpm < 80:
            return "Low"
        else:
            return "Medium"
