from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question, Answer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q 
from django.http import HttpResponse

def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()

    return redirect('my_quizzes')

def quiz_edit(request, quiz_id):
    if request.method == 'POST':
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

    quiz = Quiz.objects.get(id=quiz_id)

    quiz_data = []
    for question in quiz.questions.all():
        question_dict = {}
        question_dict['text'] = question.text
        question_dict['answers'] = list(question.answers.all())
        question_dict['correct'] = question.answers.filter(is_correct=True).count()
        question_dict['id'] = question.id
        
        quiz_data.append(question_dict)

    print(quiz_data)    

    return render(request, 'quiz/quiz_edit.html', {"quiz_data": quiz_data, "name": quiz.title})


def quiz_list(request):
    quizzes = list(Quiz.objects.all())
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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quiz, Question, Answer

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
            
            # Tworzenie quizu
            quiz = Quiz.objects.create(
                title=data['title'],
                description=data['description'],
                created_by=request.user
            )

            for question_index, question_text in enumerate(data['questions']):
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text
                )

                # Pobieranie odpowiedzi dla tego pytania
                question_answers = data['answers'][question_index]
                
                # Pobieranie poprawnych odpowiedzi (indeksy jako stringi, konwertujemy na int)
                correct_indices = [int(idx) for idx in data['correctAnswers'][question_index]]

                # Tworzenie odpowiedzi
                for answer_index, answer_text in enumerate(question_answers):
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=(answer_index in correct_indices)
                    )

            return JsonResponse({'status': 'success', 'message': 'Quiz created!'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return render(request, 'quiz/create_quiz.html')

def quiz_search(request):
    search_query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    # Wyszukiwanie
    if search_query:
        quizzes = Quiz.objects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).order_by('-created_at')
    else:
        quizzes = Quiz.objects.all().order_by('-created_at')

    # Paginacja
    paginator = Paginator(quizzes, 10)  # 10 quizów na stronę
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_results': paginator.count
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