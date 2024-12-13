from rest_framework import serializers
from .models import Form, Question, Response


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'required', 'max_length', 'min_value', 'max_value', 'number_type']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'created_at', 'questions']


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'form', 'question', 'answer']  # Include all fields
        read_only_fields = ['form']  # Make `form` field read-only

    def validate(self, data):
        question = data['question']
        answer = data['answer']

        # Validate required questions
        if question.required and not answer:
            raise serializers.ValidationError(f"The question '{question.text}' is required.")

        # Validate based on question type
        if question.question_type == 'numeric_answer':
            try:
                value = float(answer)
                if question.min_value is not None and value < question.min_value:
                    raise serializers.ValidationError(f"Answer must be at least {question.min_value}.")
                if question.max_value is not None and value > question.max_value:
                    raise serializers.ValidationError(f"Answer must be at most {question.max_value}.")
                if question.number_type == 'integer' and not value.is_integer():
                    raise serializers.ValidationError("Answer must be an integer.")
            except ValueError:
                raise serializers.ValidationError("Answer must be a valid number.")

        elif question.question_type in ['short_answer', 'complete_answer', 'email']:
            if len(answer) > question.max_length:
                raise serializers.ValidationError(f"Answer cannot exceed {question.max_length} characters.")

        return data       