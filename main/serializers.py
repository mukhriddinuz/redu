from rest_framework import serializers
from .models import (
    User, Employee, Student, Course, Room, Days,
    Groups, Payment, Attendance, Homework, Exam, Notification
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'salary', 'bio', 'specialty', 'experience', 'percentage']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'parent_number', 'extra_parent_number', 'telegram', 'status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'duration', 'price', 'info']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity']


class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Days
        fields = ['id', 'day_name']


class GroupsSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    teacher = EmployeeSerializer()
    students = UserSerializer(many=True)
    archive_students = UserSerializer(many=True)
    room = RoomSerializer()
    days = DaysSerializer(many=True)

    class Meta:
        model = Groups
        fields = [
            'id', 'name', 'course', 'teacher', 'students', 'archive_students',
            'room', 'start_time', 'end_time', 'days', 'start_hour', 'end_hour',
            'info', 'status', 'created_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_date']


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'is_present']


class HomeworkSerializer(serializers.ModelSerializer):
    group = GroupsSerializer()
    teacher = EmployeeSerializer()

    class Meta:
        model = Homework
        fields = ['id', 'group', 'teacher', 'work', 'create_at']


class ExamSerializer(serializers.ModelSerializer):
    group = GroupsSerializer()
    exam_teacher = EmployeeSerializer(many=True)
    room = RoomSerializer()

    class Meta:
        model = Exam
        fields = ['id', 'group', 'exam_teacher', 'min_score', 'max_score', 'date', 'room']


class NotificationSerializer(serializers.ModelSerializer):
    creator = EmployeeSerializer()
    student = UserSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'creator', 'student', 'message', 'created_at']
