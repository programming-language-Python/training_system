from apps.testing.models import SolvingTesting
from apps.user.mixins import StudentSolvingTestingListMixin


class StudentSolvingTestingListView(StudentSolvingTestingListMixin):
    model = SolvingTesting
