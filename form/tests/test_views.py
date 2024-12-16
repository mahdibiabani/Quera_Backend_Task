from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from form.models import Form, Question, Response

class FormViewSetTests(APITestCase):
    def setUp(self):
        self.form = Form.objects.create(title="Sample Form")
        self.question1 = Question.objects.create(
            form=self.form,
            text="What is your name?",
            question_type="short_answer",
            required=True
        )
        self.question2 = Question.objects.create(
            form=self.form,
            text="What is your age?",
            question_type="numeric_answer",
            required=True,
            number_type="integer",
            min_value=0,
            max_value=120
        )

    def test_list_forms(self):
        url = reverse('form-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_form(self):
        url = reverse('form-detail', args=[self.form.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.form.title)

   

