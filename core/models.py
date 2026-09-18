from django.db import models

class Student(models.Model):
    roll = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    semester = models.EmailField(unique=True)

    def __str__(self):
        return self.roll


class Subject(models.Model):
    name = models.CharField(max_length=50)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=35)

    def __str__(self):
        return self.name


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject'],
                name='unique_student_subject'
            )
        ]

    def __str__(self):
        return str(self.student)
