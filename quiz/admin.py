from django.contrib import admin
from .models import Quiz, Question, Answer, ContactMessage

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ContactMessage)