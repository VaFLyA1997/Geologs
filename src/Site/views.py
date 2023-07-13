from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Forum, VotingOption, Comment, Profile, News, Docs
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Sum, Count
from django.http.response import FileResponse
from django.contrib.auth.decorators import login_required

User = get_user_model()
def forum(request):
    forums = Forum.objects.all().order_by('-date')
    forum_comments_count = []  # Создайте список для хранения количества комментариев в каждой теме
    for forum in forums:
        comments_count = Comment.objects.filter(forum=forum).count()  # Получите количество комментариев в каждой теме
        forum_comments_count.append(comments_count)  # Добавьте количество комментариев в список
    forum_data = zip(forums, forum_comments_count)
    return render(request, 'forum.html', {"forum_data": forum_data})


# def profile(request, id):
#     profile = Profile.objects.get(pk = id)
#     return render(request, 'profile.html', {"profile" : profile})


@login_required(login_url='index', redirect_field_name=None)
def profile(request, id):
    if not request.user.is_authenticated:
        news = News.objects.filter(announcement = True).order_by('-date')[:3]
        return render(request, 'index.html', {"news" : news, 'range': range(3)})
    else:
        profile = get_object_or_404(Profile, id=id)
        if request.user != profile:
            return redirect('profile', id=request.user.id)
        return render(request, 'profile.html', {'profile': profile})

def home(request):
    news = News.objects.filter(announcement = True).order_by('-date')[:3]
    return render(request, 'index.html', {"news" : news, 'range': range(3)})

def news(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {"news" : news})

def newsSingle(request, pk):
    news = News.objects.get(pk=pk)
    return render(request, 'single-news.html', {"news" : news})

def docs(request):
    docs = Docs.objects.all().order_by('-date')
    return render(request, 'documents.html', {"docs" : docs})

def filter_documents(request):
    selected_category = request.GET.get('category')
    if selected_category == 'all':
        docs = Docs.objects.all().order_by('-date')
    else:
        docs = Docs.objects.filter(category=selected_category).order_by('-date')
    context = {'docs': docs}
    docs_list_html = render_to_string('docs_list.html', context)
    return HttpResponse(docs_list_html)


def contacts(request):
    # docs = Docs.objects.all().order_by('-date')
    return render(request, 'contacts.html')


@csrf_exempt
def handle_login(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            login(request, user)
            # return redirect('/profile/' + str(user.id))
            return JsonResponse({'success': True,  'user_id': user.id})
        else:
            return JsonResponse({'success': False})
    else:
        return render(request, 'login.html')


def single_forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    comments = Comment.objects.filter(forum=forum)  # Получить все комментарии связанные с форумом
    voting_options = forum.voting_options.all()

    if request.method == 'POST':
        text = request.POST.get('text')
        if request.user.is_authenticated:
            profile = User.objects.get(username=request.user.username)
            comment = Comment.objects.create(forum=forum, user=profile, text=text, date=timezone.now())
            comment.save()

    total_votes = VotingOption.objects.filter(forum=forum).annotate(num_voters=Count('voters')).aggregate(Sum('num_voters'))['num_voters__sum']
    print(total_votes)
    if total_votes:
        for option in voting_options:
            option_percentage = option.voters.all().count() / total_votes * 100
            gradient = f'background: linear-gradient(to right, #b1ce76 {option_percentage}%, #fff {option_percentage}%);'
            option.gradient = gradient
    # voting_options = voting.options.values_list('option_text', flat=True)
    context = {
        'forum': forum,
        'comments': comments,
        'voting_options': voting_options,
    }
    # print(comments[0].user.avatar.url)
    return HttpResponse(render(request, 'single-forum.html', context))

def voted_users(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    voters = forum.voting_options.values('voters__first_name', 'voters__last_name', 'voters__avatar').distinct().order_by('voters__last_name')
    context = {
        'forum': forum,
        'voters': voters
    }
    return render(request, 'voted.html', context)




# def vote(request):
#     if request.method == 'POST':
#         option_id = request.POST.get('vote')
        
#         if option_id:
#             option = VotingOption.objects.get(pk=option_id)
            
#             if request.user.is_authenticated:
#                 user = request.user
                
#                 with transaction.atomic():
#                     # Удаление предыдущего выбора пользователя
#                     user_previous_votes = VotingOption.objects.filter(voters=user)
#                     for previous_vote in user_previous_votes:
#                         previous_vote.voters.clear()
                    
#                     # Добавление нового выбора пользователя
#                     option.voters.add(user)
                
#                 votes_count = option.voters.count()
                
#                 response_data = {
#                     'votes_count': votes_count,
#                 }
                    
#                 return JsonResponse(response_data)
#             else:
#                 return HttpResponseBadRequest('User is not authenticated.')
    
#     return redirect('forum')


# def vote(request):
#     if request.method == 'POST':
#         option_id = request.POST.get('vote')
        
#         if option_id:
#             option = VotingOption.objects.get(pk=option_id)
            
#             if request.user.is_authenticated:
#                 user = request.user
#                 forum_id = request.POST.get('forum_id')  # Получаем идентификатор темы формы

#                 with transaction.atomic():
#                     # Удаление предыдущего выбора пользователя
#                     user_previous_votes = VotingOption.objects\
#                         .filter(voters=user, forum_id=forum_id)  # Фильтруем по идентификатору темы формы
#                     for previous_vote in user_previous_votes:
#                         previous_vote.voters.remove(user)
                    
#                     # Добавление нового выбора пользователя
#                     option.voters.add(user)
            
#                 votes_count = option.voters.count()
                
#                 # Обновление вариантов голосования для указанной темы формы
#                 voting_options = VotingOption.objects.filter(forum_id=forum_id)
#                 form_html = render_to_string('voting_options.html', {'voting_options': voting_options})
                
#                 response_data = {
#                     'votes_count': votes_count,
#                     'form_html': form_html
#                 }
                    
#                 return JsonResponse(response_data)
#             else:
#                 return HttpResponseBadRequest('User is not authenticated.')
    
#     return redirect('forum')


def vote(request):
    if request.method == 'POST':
        option_id = request.POST.get('vote')
        
        if option_id:
            option = VotingOption.objects.get(pk=option_id)
            
            if request.user.is_authenticated:
                user = request.user
                forum_id = request.POST.get('forum_id')

                with transaction.atomic():
                    user_previous_votes = VotingOption.objects.filter(voters=user, forum_id=forum_id)
                    for previous_vote in user_previous_votes:
                        previous_vote.voters.remove(user)
                    
                    option.voters.add(user)
            
                voting_options = VotingOption.objects.filter(forum_id=forum_id)

                total_votes = voting_options.annotate(num_voters=Count('voters')).aggregate(Sum('num_voters'))['num_voters__sum']
                print(total_votes)
                if total_votes:
                    for option in voting_options:
                        option_percentage = option.voters.count() / total_votes * 100
                        gradient = f'background: linear-gradient(to right, #b1ce76 {option_percentage}%, #fff {option_percentage}%);'
                        option.gradient = gradient
                
                form_html = render_to_string('voting_options.html', {'voting_options': voting_options, 'total_votes': total_votes})
                
                response_data = {
                    'total_votes': total_votes,
                    'form_html': form_html
                }
                    
                return JsonResponse(response_data)
            else:
                return HttpResponseBadRequest('User is not authenticated.')
    
    return redirect('forum')


def download(request, pk):
    obj = Docs.objects.get(pk=pk)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response