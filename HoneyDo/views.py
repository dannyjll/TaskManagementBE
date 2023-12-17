from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getCategory(request, pk):
    """
    Retrieve, update or delete a category instance.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def reminder_list(request):
    if request.method == 'GET':
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = ReminderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getReminder(request, pk):
    """
    Retrieve, update or delete a reminder instance.
    """
    try:
        reminder = Reminder.objects.get(pk=pk)
    except Reminder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReminderSerializer(reminder, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReminderSerializer(reminder, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getProfile(request, pk):
    """
    Retrieve, update or delete a profile instance.
    """
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getProfileFromUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if request.method == 'GET':
            profile = Profile.objects.get(user=user.pk)
            serializer = ProfileSerializer(profile, context={'request': request}, many=False)
            return Response({'data': serializer.data})
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=500)

@api_view(['GET', 'POST'])
def group_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def my_group_list(request):
    user = request.user
    if request.method == 'GET':
        groups = user.group_set.all()
        serializer = GroupSerializer(groups, context={'request': request}, many=True)
        return Response({'data': serializer.data})


@api_view(['GET', 'PUT', 'DELETE'])
def getGroup(request, pk):
    """
    Retrieve, update or delete a group instance.
    """
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getListsFromGroup(request, pk):
    try:
        group = Group.objects.get(pk=pk)
        if request.method == 'GET':
            lists = List.objects.filter(pk__in=group.lists.all())
            serializer = ListSerializer(lists, context={'request': request}, many=True)
            return Response({'data': serializer.data})
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=500)


@api_view(['GET'])
def getUsersFromGroup(request, pk):
    try:
        group = Group.objects.get(pk=pk)
        if request.method == 'GET':
            users = User.objects.filter(pk__in=group.users.all())
            serializer = UserSerializer(users, context={'request': request}, many=True)
            return Response({'data': serializer.data})
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=500)

@api_view(['GET'])
def getUserFromProfilePK(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
        if request.method == 'GET':
            user = profile.user
            serializer = UserSerializer(user, context={'request': request})
            return Response({'data': serializer.data})
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": "Internal Server Error"}, status=500)

@api_view(['GET', 'POST'])
def list_list(request):
    if request.method == 'GET':
        lists = List.objects.all()
        serializer = ListSerializer(lists, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def my_list_list(request):
    user = request.user
    if request.method == 'GET':
        lists = List.objects.filter(group__in=user.group_set.all()).distinct()
        serializer = ListSerializer(lists, context={'request': request}, many=True)
        return Response({'data': serializer.data})


@api_view(['GET', 'PUT', 'DELETE'])
def getList(request, pk):
    """
    Retrieve, update or delete a list instance.
    """
    try:
        list = List.objects.get(pk=pk)
    except List.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ListSerializer(list, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ListSerializer(list, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def my_tasks(request):
    if request.method == 'GET':
        task = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(task, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def getTask(request, pk):
    """
    Retrieve, update or delete a task instance.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getTaskFromList(request, pk):
    """
    Retrieve, update or delete a task instance.
    """
    list = List.objects.get(pk=pk)

    if request.method == 'GET':
        tasks = Task.objects.filter(pk__in=list.task_set.all())
        serializer = TaskSerializer(tasks, context={'request': request}, many=True)
        return Response({'data': serializer.data})

@api_view(['GET'])
def getUsersFromList(request, pk):
    """
    Retrieve users from boards
    """
    list_instance = List.objects.get(pk=pk)
    groups = Group.objects.filter(lists=list_instance)
    print(f"Groups: {groups.query}")

    # Retrieve users belonging to the groups
    group_users = User.objects.filter(groups__in=groups).distinct()
    print(f"Users: {group_users.query}")

    if request.method == 'GET':
        serializer = UserSerializer(group_users, context={'request': request}, many=True)
        return Response({'data': serializer.data})

@api_view(['GET', 'POST'])
def my_task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
def my_profile(request):
    if request.method == 'GET':
        profile = Profile.objects.filter(user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getUser(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def getAllUsers(request):
    """
    Retreive all users
    """
    try:
        users = User.objects.all()
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getUserFromPK(request, pk):
    """
    Retrieve a user from their PK.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getGuest1(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def getGuest2(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def getGuest3(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def getGuest4(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


def contactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ["admin@honeydo.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("success")
    return render(request, "email.html", {"form": form})


def successView(request):
    return HttpResponse("Thank you for contacting HoneyDo!! Due to an unusual level of activity, responses are "
                        "delayed. We anticipate responding to your message within three business days. In the "
                        "meantime, please feel free to explore the features that HoneyDo has to offer :D")
