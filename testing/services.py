from django.shortcuts import redirect


def redirect_not_is_teacher(request):
    if not request.user.is_teacher:
        return redirect('user:home')
