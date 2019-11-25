from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
# Create your models here.
#Course Model
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="course_org", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Name")
    desc = models.CharField(max_length=300, verbose_name="Description")
    is_banner = models.BooleanField(default=False, verbose_name="Is_banner")
    detail = models.TextField(verbose_name="Detail")
    teacher = models.ForeignKey(Teacher, verbose_name="Teacher", null=True, blank=True, on_delete=models.CASCADE)
    degree = models.CharField(choices=(("1", "beginner"), ("2", "intermediate"), ("3", "advance")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="learn length(minute)")
    students = models.IntegerField(default=0, verbose_name="StudentNumber")
    fav_nums = models.IntegerField(default=0, verbose_name="Fav_nums")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="image", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="ClickNum")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Addtime")
    category = models.CharField(default="backend", max_length=20, verbose_name="CourseCategory")
    tag = models.CharField(default="", verbose_name="CourseTag", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="CourseInfo")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="TeacherTell")
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def get_zj_nums(self):
        #get lessons of the course
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="LessonName")
    learn_times = models.IntegerField(default=0, verbose_name="LearnTime")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Addtime")

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="Lesson", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="VideoName")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Addtime")
    url = models.CharField(max_length=200, verbose_name="Url", default="")
    learn_times = models.IntegerField(default=0, verbose_name="LearnTime")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Name")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="File", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Addtime")

    class Meta:
        verbose_name = "CourseResource"
        verbose_name_plural = "CourseResources"