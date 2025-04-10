from django.db import models
from django.contrib.auth.models import User
from django.db import models

class DifficultyLevel(models.TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quizzes'
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.MEDIUM,
        verbose_name="Difficulty Level"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='quizzes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class Notification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    text = models.TextField(verbose_name="Notification")
    created_at = models.DateTimeField(auto_now_add=True)

    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Imię")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Wiadomość")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data wysłania")
    is_processed = models.BooleanField(default=False, verbose_name="Przetworzone")

    class Meta:
        verbose_name = "Wiadomość kontaktowa"
        verbose_name_plural = "Wiadomości kontaktowe"
        ordering = ['-created_at']

    def __str__(self):
        return f"Wiadomość od {self.name} ({self.email})"