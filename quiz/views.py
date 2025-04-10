import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Quiz, Question, Answer, DifficultyLevel, Category, Notification
from .forms import ContactForm

@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'quiz/notifications.html', {'notifications': notifications})

def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.created_by != request.user:
        return HttpResponseServerError("No permissions.")

    quiz.delete()

    return redirect('my_quizzes')

def quiz_edit(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.created_by != request.user:
        return HttpResponseServerError("No permissions.")

    if request.method == 'POST':

        category_id = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        if category_id:
            quiz.category = Category.objects.get(id=category_id)
        if difficulty in DifficultyLevel.values:
            quiz.difficulty = difficulty
        quiz.save()

        answers = {}
        for key, value in request.POST.items():
            splitted_key = key.split('-')

            if splitted_key[0] == 'q':
                Question.objects.filter(id=splitted_key[1]).update(text=value)

            if splitted_key[0] == 'a':
                answer = Answer.objects.get(id=splitted_key[1])
                answer.text = value
                answers[splitted_key[1]] = answer

            if splitted_key[0] == 'c':
                if value == "off":
                    answers[splitted_key[1]].is_correct = False
                elif value == "on":
                    answers[splitted_key[1]].is_correct = True

        for answer in answers.values():
            answer.save()

        return redirect('quiz_detail', pk=quiz_id)

    quiz_data = []
    for question in quiz.questions.all():
        question_dict = {}
        question_dict['text'] = question.text
        question_dict['answers'] = list(question.answers.all())
        question_dict['correct'] = question.answers.filter(is_correct=True).count()
        question_dict['id'] = question.id
        
        quiz_data.append(question_dict)

    categories = Category.objects.all()
    difficulties = DifficultyLevel.choices

    return render(request, 'quiz/quiz_edit.html', {
    "quiz_data": quiz_data,
    "name": quiz.title,
    "quiz": quiz,
    "categories": categories,
    "difficulties": difficulties,
    })


def quiz_list(request):
    quizzes = list(Quiz.objects.order_by('-created_at')[:9])
    for quiz in quizzes:
        quiz.duration = quiz.questions.count() * 1.5
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, pk):  
    quiz = get_object_or_404(Quiz, pk=pk)  
    score = None  

    quiz_data = []
    for question in quiz.questions.all():
        question_dict = {}
        question_dict['text'] = question.text
        question_dict['answers'] = list(question.answers.all())
        question_dict['correct'] = question.answers.filter(is_correct=True).count()
        question_dict['id'] = question.id
        
        quiz_data.append(question_dict)

    print(quiz_data)

    if request.method == 'POST':  
        score = 0  
        
        solved_quiz_data = {}
        for question in quiz.questions.all():
            solved_question = {}
            solved_question['correct'] =False

            selected_answers = request.POST.getlist(f'question_{question.id}')  
            correct_answers = question.answers.filter(is_correct=True).values_list('id', flat=True)

            if set(map(int, selected_answers)) == set(correct_answers):
                score += 1
                solved_question['correct'] = True

            solved_question['user_answers'] = list(map(int, selected_answers)) 
            solved_question['correct_answers'] = list(correct_answers)
            solved_quiz_data[question.id] = solved_question
            result = next((item for item in quiz_data if item['id'] == question.id), None)
            result['user_answer'] = solved_question
        
        print(quiz_data)
        # print(solved_quiz_data)

        
        return render(request, 'quiz/quiz_solved.html', {
            'solved_quiz_data': solved_quiz_data,
            'quiz_data': quiz_data,
            'score': score
        })

    return render(request, 'quiz/quiz_detail.html', {  
        'quiz': quiz,
        'questions': quiz_data
    })  

@login_required
def my_quizzes(request):
    quizzes = Quiz.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'quizzes': quizzes,
        'total_quizzes': quizzes.count()
    }
    return render(request, 'quiz/my_quizzes.html', context)

@csrf_exempt
@login_required
def create_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            category_id = data.get('category_id')
            difficulty = data.get('difficulty')

            category = Category.objects.get(id=category_id)

            if difficulty not in DifficultyLevel.values:
                return JsonResponse({'status': 'error', 'message': 'Invalid difficulty level'}, status=400)

            quiz = Quiz.objects.create(
                title=data['title'],
                description=data['description'],
                category=category,
                difficulty=difficulty,
                created_by=request.user
            )

            for question_index, question_text in enumerate(data['questions']):
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text
                )

                question_answers = data['answers'][question_index]
                correct_indices = [int(idx) for idx in data['correctAnswers'][question_index]]

                for answer_index, answer_text in enumerate(question_answers):
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=(answer_index in correct_indices)
                    )

            return JsonResponse({'status': 'success', 'message': 'Quiz created!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # GET method — render template with categories
    categories = Category.objects.all()
    return render(request, 'quiz/create_quiz.html', {'categories': categories})

def quiz_search(request):
    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category')
    selected_difficulty = request.GET.get('difficulty')
    page_number = request.GET.get('page', 1)

    quizzes = Quiz.objects.all()

    # Filtrowanie po tytule/opisie
    if search_query:
        quizzes = quizzes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filtrowanie po kategorii
    if selected_category and selected_category.isdigit():
        quizzes = quizzes.filter(category_id=selected_category)

    # Filtrowanie po trudności
    if selected_difficulty in dict(DifficultyLevel.choices).keys():
        quizzes = quizzes.filter(difficulty=selected_difficulty)

    quizzes = quizzes.order_by('-created_at')

    paginator = Paginator(quizzes, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_difficulty': selected_difficulty,
        'categories': Category.objects.all(),
        'difficulties': DifficultyLevel.choices,
        'total_results': paginator.count,
    }
    return render(request, 'quiz/quiz_search.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Po udanej rejestracji przekierowanie do logowania
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()  # Czyścimy formularz po udanym zapisie
            return render(request, 'quiz/contact.html', {'form': form, 'success': True})
    else:
        form = ContactForm()
    
    return render(request, 'quiz/contact.html', {'form': form})
    
def custom_404(request, exception=None):
    return render(request, 'quiz/404.html', status=404)

def custom_500(request):
    return render(request, 'quiz/500.html', status=500)