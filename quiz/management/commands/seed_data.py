from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import Category, Quiz, Question, Answer, DifficultyLevel
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample categories, quizzes, questions and answers'

    def handle(self, *args, **kwargs):
        # Create or get test user
        user, _ = User.objects.get_or_create(username='testuser')
        user.set_password('testpass123')
        user.save()

        # Create categories
        categories = [
            ('Math', 'Quizzes related to mathematics'),
            ('Science', 'Physics, chemistry, and biology questions'),
            ('History', 'Questions from world and national history'),
        ]
        category_objects = []
        for name, desc in categories:
            cat, _ = Category.objects.get_or_create(name=name, description=desc)
            category_objects.append(cat)
        self.stdout.write(self.style.SUCCESS(f'Created {len(category_objects)} categories.'))

        # Create sample quizzes
        for i in range(3):
            quiz = Quiz.objects.create(
                title=f'Sample Quiz {i+1}',
                description='This is a sample quiz description.',
                category=random.choice(category_objects),
                difficulty=random.choice([DifficultyLevel.EASY, DifficultyLevel.MEDIUM, DifficultyLevel.HARD]),
                created_by=user
            )

            for q in range(3):  # 3 questions per quiz
                question = Question.objects.create(
                    quiz=quiz,
                    text=f'Question {q+1} of {quiz.title}'
                )

                correct_answer_index = random.randint(0, 3)
                for a in range(4):  # 4 answers per question
                    Answer.objects.create(
                        question=question,
                        text=f'Answer {a+1} for Q{q+1}',
                        is_correct=(a == correct_answer_index)
                    )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
