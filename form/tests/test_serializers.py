from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from form.models import Form, Question, FormResponse
from form.serializers import FormSerializer, QuestionSerializer, ResponseSerializer


class QuestionSerializerTest(APITestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Test Form")

    def test_question_serializer_valid(self):
        question = Question(
            form=self.form,
            text="What is your name?",
            question_type="short_answer",
            required=True,
            max_length=100
        )
        serializer = QuestionSerializer(question)
        self.assertEqual(serializer.data['text'], question.text)
        self.assertEqual(serializer.data['question_type'], question.question_type)
        self.assertEqual(serializer.data['required'], question.required)



class FormSerializerTest(APITestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Test Form")
        self.question = Question.objects.create(
            form=self.form,
            text="What is your name?",
            question_type="short_answer",
            required=True,
            max_length=100
        )

    def test_form_serializer_valid(self):
        serializer = FormSerializer(self.form)
        self.assertEqual(serializer.data['title'], self.form.title)
        self.assertEqual(len(serializer.data['questions']), 1)  # Check that questions are included


class ResponseSerializerTest(APITestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Feedback Form")
        self.question = Question.objects.create(
            form=self.form,
            text="How old are you?",
            question_type="numeric_answer",
            required=True,
            min_value=18,
            max_value=100,
            number_type="integer"
        )

    def test_response_serializer_valid(self):
        data = {
            'question': self.question.id,  # Use the question's ID here
            'form': self.form.id,
            'answer': "25"
        }
        serializer = ResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['answer'], "25")

    def test_response_serializer_required_question(self):
        data = {
            'question': self.question.id,
            'form': self.form.id,
            'answer': ""
        }
        serializer = ResponseSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_response_serializer_numeric_answer_invalid(self):
        data = {
            'question': self.question.id,
            'form': self.form.id,
            'answer': "10"  # Below min_value
        }
        serializer = ResponseSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_response_serializer_numeric_answer_valid(self):
        data = {
            'question': self.question.id,
            'form': self.form.id,
            'answer': "30"  # Within the range
        }
        serializer = ResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_response_serializer_invalid_answer_type(self):
        data = {
            'question': self.question.id,
            'form': self.form.id,
            'answer': "25.5"  # Invalid if the question expects an integer
        }
        serializer = ResponseSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_response_serializer_text_answer_length(self):
        question = Question.objects.create(
            form=self.form,
            text="What is your email?",
            question_type="email",
            required=True,
            max_length=50
        )
        data = {
            'question': question.id,
            'form': self.form.id,
            'answer': "a" * 51  # Exceeds max_length
        }
        serializer = ResponseSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_response_serializer_text_answer_valid(self):
        question = Question.objects.create(
            form=self.form,
            text="What is your email?",
            question_type="email",
            required=True,
            max_length=50
        )
        data = {
            'question': question.id,
            'form': self.form.id,
            'answer': "test@example.com"
        }
        serializer = ResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
