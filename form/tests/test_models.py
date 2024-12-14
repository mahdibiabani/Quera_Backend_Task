from django.test import TestCase
from django.core.exceptions import ValidationError
from form.models import Form, Question, Response



class FormModelTest(TestCase):
    def test_form_creation(self):
        form = Form.objects.create(title="Test Form")
        self.assertEqual(form.title, "Test Form")
        self.assertIsNotNone(form.created_at)  # Ensure created_at is auto-populated


class QuestionModelTest(TestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Test Form")

    def test_question_creation(self):
        question = Question.objects.create(
            form=self.form,
            text="What is your name?",
            question_type="short_answer",
            required=True,
            max_length=100
        )
        self.assertEqual(question.text, "What is your name?")
        self.assertTrue(question.required)
        self.assertEqual(question.max_length, 100)

    def test_max_length_validation(self):
        question = Question(
            form=self.form,
            text="Short answer question",
            question_type="short_answer",
            max_length=300  # Exceeds default limit
        )
        with self.assertRaises(ValidationError) as context:
            question.full_clean()

        self.assertIn(
            "max_length for short_answer cannot exceed 200 characters.",
            str(context.exception)
        )

    def test_numeric_question_validation(self):
        question = Question(
            form=self.form,
            text="Enter a number",
            question_type="numeric_answer",
            min_value=10,
            max_value=5,  # Invalid: min_value > max_value
            number_type="integer"
        )
        with self.assertRaises(ValidationError) as context:
            question.full_clean()

        self.assertIn("min_value cannot be greater than max_value", str(context.exception))

    def test_missing_number_type_for_numeric_answer(self):
        question = Question(
            form=self.form,
            text="Enter a number",
            question_type="numeric_answer",
            min_value=1,
            max_value=10
        )
        with self.assertRaises(ValidationError) as context:
            question.full_clean()

        self.assertIn("number_type must be specified", str(context.exception))

    def test_valid_numeric_question(self):
        question = Question.objects.create(
            form=self.form,
            text="Enter an integer",
            question_type="numeric_answer",
            min_value=1,
            max_value=100,
            number_type="integer"
        )
        self.assertEqual(question.number_type, "integer")
        self.assertEqual(question.min_value, 1)
        self.assertEqual(question.max_value, 100)

    def test_default_max_length_for_email(self):
        question = Question(
            form=self.form,
            text="What is your email?",
            question_type="email",
        )
        question.full_clean()  # Should set default max_length
        self.assertEqual(question.max_length, Question.DEFAULT_FORCE_LIMITS['email'])


class ResponseModelTest(TestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Feedback Form")
        self.question = Question.objects.create(
            form=self.form,
            text="Enter your name",
            question_type="short_answer",
            max_length=100
        )

    def test_response_creation(self):
        response = Response.objects.create(
            question=self.question,
            form=self.form,
            answer="John Doe"
        )
        self.assertEqual(response.answer, "John Doe")
        self.assertEqual(response.form, self.form)
        self.assertEqual(response.question, self.question)
