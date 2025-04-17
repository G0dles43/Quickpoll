from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def polls_list_or_create(request):
    if request.method == 'GET':
        polls = Poll.objects.filter(author=request.user)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = PollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def poll_detail_update_delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, author=request.user)

    if request.method == 'GET':
        serializer = PollSerializer(poll)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def choices_list_or_create(request, poll_id):
    if request.method == 'GET':
        choices = Choice.objects.filter(poll__id=poll_id)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['poll'] = poll_id
        serializer = ChoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def choice_detail_update_delete(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)

    if request.method == 'GET':
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vote CRUD
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def votes_list_or_create(request, poll_id):
    if request.method == 'GET':
        votes = Vote.objects.filter(poll__id=poll_id)
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['voter'] = request.user.id
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def vote_detail_delete(request, vote_id):
    vote = get_object_or_404(Vote, id=vote_id, voter=request.user)

    if request.method == 'GET':
        serializer = VoteSerializer(vote)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)