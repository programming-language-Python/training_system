from apps.testing_by_code.models import SolvingTesting
from apps.user.mixins import StudentSolvingTestingListMixin


class StudentSolvingTestingByCodeListView(StudentSolvingTestingListMixin):
    model = SolvingTesting
