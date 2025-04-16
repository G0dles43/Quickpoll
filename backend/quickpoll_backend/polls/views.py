from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote
from .serializers import PollSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_polls(request):
    user = request.user
    polls  = Poll.objects.filter(author=user)
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)