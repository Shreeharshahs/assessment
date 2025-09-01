from django.db import models

# Create your models here.
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=256)
    salt = models.CharField(max_length=64)

    def __str__(self):
        return self.teacher_name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self):
        return f'{self.name} - {self.subject}'


class AuditLog(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    #old_marks = models.IntegerField()
    #new_marks = models.IntegerField()
