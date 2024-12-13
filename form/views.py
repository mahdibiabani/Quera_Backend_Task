from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Form, Response
from .serializers import FormSerializer, QuestionSerializer


class FormViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view forms

    @action(detail=True, methods=['get'], url_path='questions')
    def get_questions(self, request, pk=None):
        form = self.get_object()
        questions = form.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)