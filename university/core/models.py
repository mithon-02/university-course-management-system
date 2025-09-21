# core/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=120)
    enrollment_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=120)
    hire_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.department})"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=250)
    credits = models.PositiveSmallIntegerField(default=3)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.title}"


class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('', 'Not graded'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True, default='')

    class Meta:
        unique_together = ('student', 'course')  # prevents duplicate student-course pairs
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.name} in {self.course.course_code}"

    def clean(self):
        # extra safety: ensure unique at validation time (useful when not relying on DB errors)
        if Enrollment.objects.exclude(pk=self.pk).filter(student=self.student, course=self.course).exists():
            raise ValidationError("This student is already enrolled in this course.")
