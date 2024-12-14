from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Form, Question, Response
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
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to submit responses

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        form = question.form  # Automatically get the form from the question
        serializer.save(form=form)

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_responses(self, request):
        """
        Submit responses to a form.

        Args:
        - form: ID of the form
        - responses: List of responses with question IDs and answers

        Returns:
        - Success or error message
        """
        form_id = request.data.get('form')
        responses = request.data.get('responses', [])

        # Validate form exists
        form = Form.objects.filter(id=form_id).first()
        if not form:
            return Response({"error": "Form not found"}, status=404)

        # Process each response
        for response_data in responses:
            question_id = response_data.get('question')
            answer = response_data.get('answer')

            # Validate that the question exists
            question = Question.objects.filter(id=question_id).first()
            if not question:
                return Response({"error": f"Question with ID {question_id} not found"}, status=404)

            # Validate answer (already done in ResponseSerializer)
            response_serializer = ResponseSerializer(data=response_data)
            if not response_serializer.is_valid():
                return Response(response_serializer.errors, status=400)

            # Save the response
            response_serializer.save()

        return Response({"message": "Responses submitted successfully"}, status=201)    