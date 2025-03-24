from django import forms
from django.forms import modelformset_factory
from .models import Quiz, Question, Answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    # Będziemy używać modelformset_factory do dynamicznego dodawania odpowiedzi
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz', None)  # przekazujemy quiz do formularza
        super().__init__(*args, **kwargs)
        if quiz:
            self.quiz = quiz

    def save(self, commit=True):
        question = super().save(commit=False)
        question.quiz = self.quiz
        question.save()
        
        return question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Twoje imię'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'twój@email.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Treść Twojej wiadomości...'
            }),
        }