# portal/middleware.py

from django.utils.deprecation import MiddlewareMixin
from .session_store import get_teacher_id_from_token
from .models import Teacher

class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('session_token')
        teacher_id = get_teacher_id_from_token(token)
        if teacher_id:
            try:
                request.teacher = Teacher.objects.get(id=teacher_id)
            except Teacher.DoesNotExist:
                request.teacher = None
        else:
            request.teacher = None
