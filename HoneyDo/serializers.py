from rest_framework import serializers
from .models import Task, List, Group, Profile, Reminder, Category
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'list_set')


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('pk', 'title', 'description', 'notes', 'list_image', 'group_set', 'category', 'task_set')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'title', 'users', 'lists')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'user', 'first_name', 'last_name', 'email', 'bio', 'image', 'private')


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ('pk', 'description', 'task', 'user', 'notification_date')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'title', 'description', 'completion_status', 'due_date', 'notes', 'user', 'list', 'difficulty')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password'}, validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True, 'min_length': 6},
            'password2': {'write_only': True, 'min_length': 6}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email', 'group_set')


class Guest1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')


class Guest2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')


class Guest3Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')


class Guest4Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')
