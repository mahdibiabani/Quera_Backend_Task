from django.db import models

class Form(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Question(models.Model):
    QUESTION_TYPES = [
        ('short_answer', 'Short Answer'),
        ('complete_answer', 'Complete Answer'),
        ('email', 'Email'),
        ('numeric_answer', 'Numeric Answer'),
    ]

    DEFAULT_FORCE_LIMITS = {
        'short_answer': 200,         # Force limit for short answers
        'complete_answer': 5000,    # Force limit for complete answers
        'email': 254,               # Max valid email length
        'numeric_answer': 20,       # Reasonable limit for numeric answers
    }

    form = models.ForeignKey(Form, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.question_type    

