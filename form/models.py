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


    NUMBER_TYPES = [
        ('integer', 'Integer'),
        ('float', 'Float'),
    ]


    form = models.ForeignKey(Form, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    required = models.BooleanField(default=False)
    max_length = models.PositiveIntegerField(null=True, blank=True)


    # Fields for numeric questions
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    number_type = models.CharField(
        max_length=10,
        choices=NUMBER_TYPES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.question_type    
    

    def save(self, *args, **kwargs):
        # Apply logic based on question type
        if self.question_type in ['short_answer', 'complete_answer', 'email']:

            # Get the force limit for the question type
            force_limit = self.DEFAULT_FORCE_LIMITS.get(self.question_type)

            # Ensure max_length does not exceed the force limit
            if self.max_length is None:
                self.max_length = force_limit  # Set to default if not provided
            elif self.max_length > force_limit:
                raise ValueError(
                    f"max_length for {self.question_type} cannot exceed {force_limit} characters."
                )

        elif self.question_type == 'numeric_answer':
            # Ensure numeric questions explicitly define constraints
            if not self.number_type:
                raise ValueError("number_type must be specified for numeric questions (e.g., 'integer' or 'float').")

            if self.min_value is None or self.max_value is None:
                raise ValueError("Both min_value and max_value must be specified for numeric questions.")

            # Ensure min_value is not greater than max_value
            if self.min_value > self.max_value:
                raise ValueError("min_value cannot be greater than max_value.")


        super().save(*args, **kwargs)





