from apps.base_testing.models import MaxScore


class MaxScoreService:
    def __init__(self, max_score: MaxScore) -> None:
        self.max_score = max_score

    def get_assessment(self, percentage_execution: float) -> int:
        if self.max_score.five >= percentage_execution > self.max_score.four:
            return 5
        elif self.max_score.four >= percentage_execution > self.max_score.three:
            return 4
        elif self.max_score.three >= percentage_execution > self.max_score.two:
            return 3
        else:
            return 2
