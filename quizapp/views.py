
from unicodedata import category
from django.shortcuts import render,redirect
from quizapp.models import QuizCategory,QuestionModel,Performace
from django.http import HttpResponse
# Create your views here.




def true_W(correct_ans, attempt_ans):
    true = 0
    wrong = 0
    for i in attempt_ans:
        for j in correct_ans:
            if i in correct_ans:
                if attempt_ans[i] == correct_ans[j]:
                    true += 1
    context = {'true': true, "wrong": len(attempt_ans.keys()) - true}
    return context


def findUserAns(requestData):
    qu_id = list(requestData.keys())
    ans_id = list(requestData.values())
    answersheet = dict(zip(qu_id, ans_id))
    if "csrfmiddlewaretoken" in answersheet:
        answersheet.pop("csrfmiddlewaretoken")
    return answersheet


def CorrectAnswer(queryset):
    ques = []
    ans = []
    for i in queryset:
        ques.append(str(i.id))
        ans.append(i.answer)
    correct_ans_sheet = dict(zip(ques, ans))
    return correct_ans_sheet



def view_courses(request):
    course = QuizCategory.objects.all()
    print(course)
    d1={'course':course}
    resp = render(request,'quizapp/course.html',context=d1)
    return resp


def view_quiz(request,cat_id):
    category = QuizCategory.objects.get(id=cat_id)
    question=QuestionModel.objects.filter(category=category)
    d1={'data':question,'category':category}
    correctAns = CorrectAnswer(question)
    if request.method == "POST":
        userAns = findUserAns(request.POST)
        total_ques = len(correctAns.keys())
        total_attempt = len(userAns.keys())

        final = true_W(correctAns, userAns)
    
        point = final["true"] * question[0].category.point
        Performace.objects.create(user=request.user, quize_type=question[0].category,
                                         total_que=total_ques, attempt_que=total_attempt,
                                         points=point, true_que=final["true"],
                                         wrong_que=final["wrong"], result=True)
        #
        return redirect("/quizapp/result")
    return render(request, "quizapp/quiz.html", {"que_data": question, "quize_category": category})


    # resp = render(request,'quizapp/quiz.html',context=d1)
    return resp


def showPerformance(request):
    if request.user.is_authenticated:
        user_performance = Performace.objects.filter(user=request.user).last()
        out_of = user_performance.total_que * user_performance.quize_type.point
        return render(request, "quizapp/result.html", {"performance": user_performance, "out_of": out_of})
    return HttpResponse(
        "<center><br><br><br><br> User must be Authenticated!!<br>Click here...<a href='/login'>Login</a>")

