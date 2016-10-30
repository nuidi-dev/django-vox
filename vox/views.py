from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import BooleanField, Case, When
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout

from .models import Topic, Post, Category
from .serializers import TopicSerializer, PostSerializer
from .forms import TopicForm, PostForm
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('topic_list'))
        else:
            return render(request, 'vox/login_wrong.html')

    return render(request, 'vox/login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('topic_list'))

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic_list'))
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, 'vox/register.html', {'form': form})

class TopicView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['post_form'] = PostForm()
        context['user_liked'] = 'false'
        if self.request.user.is_authenticated:
            if self.get_object().has_user_liked(self.request.user.id):
                context['user_liked'] = 'true'
        return context

    queryset = Topic.objects.all()#.select_related('category')

class TopicList(TemplateView):

    template_name='vox/topic_list.html'

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        if 'slug' in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs['slug'])
            context['category_id'] = category.id
            context['category_name'] = category.name

        context['create_form'] = TopicForm()

        return context

class TopicNewest(TopicList):
    def get_context_data(self, **kwargs):
        context = super(TopicNewest, self).get_context_data(**kwargs)
        context['category_id'] = 'new'
        context['category_name'] = 'Newest topics'
        return context

class TopicActive(TopicList):
    def get_context_data(self, **kwargs):
        context = super(TopicActive, self).get_context_data(**kwargs)
        context['category_id'] = 'active'
        context['category_name'] = 'Active topics'
        return context

class TopicAPI(APIView):

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            created_obj = serializer.data
            created_obj['like'] = False
            created_obj['likes_num'] = 0
            return Response(created_obj, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        topics = Topic.objects_likes.all().select_related('last_post')

        # Fetch only topics in category (if GET parameter /cat/ provided)
        if 'cat' in request.query_params and request.query_params['cat'] != '':
            cat = request.query_params['cat']
            if cat == 'new':
                topics = topics.order_by('-id')
            elif cat == 'active':
                topics = topics.filter(last_post__isnull=False).order_by('-last_post__created')
            else:
                topics = topics.filter(category__id=request.query_params['cat']).order_by('-id')

        if request.user.is_authenticated:

            # Add like_flag if user liked it.
            user_id = request.user.id
            topics = topics.extra(select={'liked': "CASE WHEN EXISTS (SELECT user_id FROM vox_topic_likes WHERE vox_topic_likes.topic_id = vox_topic.id AND vox_topic_likes.user_id = {}) THEN 'true' ELSE 'false' END".format(user_id,)})

        serializer = TopicSerializer(topics, many=True)

        return Response(serializer.data)

class TopicVoteAPI(APIView):
    def post(self, request, format=None):

        result = None

        if 'lid' in request.data:

            t = get_object_or_404(Topic, pk=request.data['lid'])

            try:
                if not t.is_owner(request.user.id):
                    result = t.like(request.user.id)
                else:
                    return Response('You can\'t vote on topics that you created.', status=status.HTTP_403_FORBIDDEN)

            except IntegrityError:
                return Response('You must log in first!', status=status.HTTP_403_FORBIDDEN)

        return Response(result)

class PostAPI(APIView):

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            created_obj = serializer.data
            created_obj['likes_num'] = 0
            return Response(created_obj, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        posts = Post.objects_likes.all()

        if 'topic' in request.query_params and request.query_params['topic'] != '':
            posts = posts.filter(topic=request.query_params['topic'])

        if request.user.is_authenticated:
            posts = posts.extra(select={'liked': "CASE WHEN EXISTS (SELECT user_id FROM vox_post_likes WHERE vox_post_likes.post_id = vox_post.id AND vox_post_likes.user_id = {}) THEN 'true' ELSE 'false' END".format(request.user.id,)})

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostVoteAPI(APIView):
    def post(self, request, format=None):

        result = None

        if 'lid' in request.data:

            post = get_object_or_404(Post, pk=request.data['lid'])

            try:
                if not post.is_owner(request.user.id):
                    result = post.like(request.user.id)
                else:
                    return Response('You can\'t vote on posts that you created.', status=status.HTTP_403_FORBIDDEN)

            except IntegrityError:
                return Response('You must log in first!', status=status.HTTP_403_FORBIDDEN)

        return Response(result)
