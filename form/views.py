from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Form, Question, FormResponse
from .serializers import FormSerializer, ResponseSerializer, QuestionSerializer


class FormViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving and listing forms.

    Provides:
    - GET /forms/ -> List all forms
    - GET /forms/{id}/ -> Retrieve a specific form
    - GET /forms/{id}/questions/ -> Retrieve all questions for a specific form
    """
     
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view forms

    @action(detail=True, methods=['get'], url_path='questions')
    def get_questions(self, request, pk=None):
        """
        Retrieve all questions for a specific form.

        Args:
        - pk: ID of the form

        Returns:
        - List of questions for the form
        """
        form = self.get_object()
        questions = form.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    

class ResponseViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling responses to forms.

    Provides:
    - POST /responses/ -> Create a new response
    - GET /responses/{id}/ -> Retrieve a specific response
    """
    queryset = FormResponse.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to submit responses

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        form = question.form  # Automatically get the form from the question
        serializer.save(form=form)
  