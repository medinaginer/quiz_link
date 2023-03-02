from django.shortcuts import render, redirect
from .models import QuizModel, Quiz, User
from .forms import QuizModelForm, CreateQuizForm, SearchForm
from django.http import HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied

def check_quiz_owner(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.owner != request.user:
        raise PermissionDenied


def home (request):
    return render(request,'home.html')

#authentication functionalites:
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after they register
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


#Quiz functionalites
@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.owner = request.user  # set the owner to the current user
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = CreateQuizForm()
    return render(request, 'create_quiz.html', {'form': form})

def quiz_search(request):
    form = SearchForm(request.GET)
    query = form['query'].value()
    quizzes = Quiz.objects.filter(name__icontains=query)
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(owner=request.user)
    form = SearchForm()
    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'form': form})



def view_quiz(request, quiz_id):
    check_quiz_owner(request, quiz_id)
    quiz = Quiz.objects.get(id=quiz_id)
    context = {'quiz': quiz}
    return render(request, 'view_quiz.html', context)

def delete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    check_quiz_owner(request,quiz.id)
    check_quiz_owner(request, quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    context = {'quiz': quiz}
    return render(request, 'delete_quiz.html', context)

###Questions Functionalites

def update_question(request, question_id):
    question = QuizModel.objects.get(id=question_id)
    check_quiz_owner(request, question.quiz_id)
    if request.method == 'POST':
        question.question = request.POST.get('question', '')
        question.option1 = request.POST.get('option1', '')
        question.option2 = request.POST.get('option2', '')
        question.option3 = request.POST.get('option3', '')
        question.option4 = request.POST.get('option4', '')
        question.ans = request.POST.get('ans', '')
        question.save()
        return redirect('view_quiz', quiz_id=question.quiz.id)
    return render(request, 'update_question.html', {'question': question})

def delete_question(request, question_id):
    question = QuizModel.objects.get(id=question_id)
    check_quiz_owner(request, question.quiz.id)
    if request.method == 'POST':
        question.delete()
        return redirect('view_quiz', quiz_id=question.quiz.id)
    return HttpResponseNotAllowed(['POST'])


def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    check_quiz_owner(request,quiz.id)
    if request.method == 'POST':
        form = QuizModelForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_questions', quiz_id=quiz_id)
    else:
        form = QuizModelForm()
    return render(request, 'AddQuestion.html', {'quiz': quiz, 'form': form})

##End of the questions functionalites

## Share fucntionality 
@login_required
def share_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        quiz.shared_with.add(user)
        quiz.save()
        return redirect('view_quiz', quiz_id=quiz_id)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'share_quiz.html', {'users': users, 'quiz': quiz})

@login_required
def shared_with_me(request):
    shared_quizzes = Quiz.objects.filter(shared_with=request.user)
    return render(request, 'shared_with_me.html', {'shared_quizzes': shared_quizzes})


##Launch and Score

def launch_quiz(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if not quiz:
        return redirect('view_quiz', quiz_id=quiz_id)
    questions = QuizModel.objects.filter(quiz=quiz)
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'launch_quiz.html', context)

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            return redirect('quizzes')
        questions = QuizModel.objects.filter(quiz=quiz)
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            if q.ans == request.POST.get(q.question):
                score += 1
                correct += 1
            else:
                wrong += 1
        percentage = (correct*100)/total
        rounded_percentage = round(percentage, 2)

        context = {
            'correct': correct,
            'wrong': wrong,
            'total': total,
            'percentage': rounded_percentage 
        }
        return render(request, 'result.html', context)
    else:
        return redirect('view_quiz', quiz_id=quiz_id)