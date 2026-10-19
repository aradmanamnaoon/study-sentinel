"""Expected domain errors."""
class StudyError(Exception):
    """Study Sentinel error."""
class ValidationError(StudyError):
    """Invalid input contract or data."""
class AnalysisError(StudyError):
    """Analysis unavailable for supplied data."""
