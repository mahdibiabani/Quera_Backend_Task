from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Form, Question, Response
from .serializers import FormSerializer, ResponseSerializer, QuestionSerializer


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
    

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to submit responses

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        form = question.form  # Automatically get the form from the question
        serializer.save(form=form)

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_responses(self, request):
        # Get form and responses from the request
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