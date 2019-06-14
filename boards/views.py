from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()

    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the logged in user instead of the first

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        # TODO: redirect to created topic page
        return redirect('board_topics', pk=pk)

    return render(request, 'new_topic.html', {'board': board})
