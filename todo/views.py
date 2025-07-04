from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User # Simulate logged-in user temporary

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# ----------------------------
# 1. USER REGISTRATION VIEW
# ----------------------------
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)  # Deserialize JSON
    if serializer.is_valid():                      # Validate input
        serializer.save()                          # Save user (password is hashed)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------
# 2. USER LOGIN VIEW
# ----------------------------
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)  # Check credentials
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ----------------------------
# 3. TASK LIST VIEW (GET & POST)
# ----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])

def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    if request.method == 'GET':
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id  # auto-assign logged-in user
        serializer = TaskSerializer(data=data)  # Create a new task
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------
# 4. TASK DETAIL VIEW (GET, PUT, DELETE)
# ----------------------------
@api_view(['GET', 'PUT', 'DELETE'])

@permission_classes([IsAuthenticated])
def task_detail(request, pk):

    try:

        task = Task.objects.get(pk=pk, user=request.user)

    except Task.DoesNotExist:

        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)
