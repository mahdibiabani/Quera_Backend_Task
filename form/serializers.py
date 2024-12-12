from rest_framework import serializers
from .models import Form, Question, Response


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'required', 'max_length', 'min_value', 'max_value', 'number_type']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True, source='questions')

    class Meta:
        model = Form
        fields = ['id', 'title', 'created_at', 'questions']


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'form', 'question', 'answer']        