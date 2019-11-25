from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="Name")
    mobile = models.CharField(max_length=11, verbose_name="Mobile")
    course_name = models.CharField(max_length=50, verbose_name="CourseName")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="AddTime")

    class Meta:
        verbose_name = "UserAsk"
        verbose_name_plural = "UserAsks"


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name="Comments")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="AddTime")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "COmments"


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="User", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="fav_id")
    fav_type = models.IntegerField(choices=((1,"Course"),(2,"CourseOrg"),(3,"Teacher")), default=1, verbose_name="fav_type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="AddTime")

    class Meta:
        verbose_name = "UserFavorite"
        verbose_name_plural = "UserFavorites"


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="User")
    message = models.CharField(max_length=500, verbose_name="Message")
    has_read = models.BooleanField(default=False, verbose_name="HasRead")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="AddTime")

    class Meta:
        verbose_name = "UserMessage"
        verbose_name_plural = "UserMessages"


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="AddTime")

    class Meta:
        verbose_name = "UserCourse"
        verbose_name_plural = "UserCourses"