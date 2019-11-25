from datetime import datetime

from django.db import models

# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="City")
    desc = models.CharField(max_length=200, verbose_name="CityDesc")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="OrgName")
    desc = models.TextField(verbose_name="OrgDesc")
    tag = models.CharField(max_length=10, verbose_name="tag", default="famous")
    category = models.CharField(default="pxjg", verbose_name="category", max_length=20, choices=(("pxjg","pxjg"),("gr","gr"),("gx","gx")))
    click_nums = models.IntegerField(default=0, verbose_name="ClickNum")
    fav_nums = models.IntegerField(default=0, verbose_name="fav_nums")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="Image")
    address = models.CharField(max_length=150, verbose_name="OrgAddress")
    city = models.ForeignKey(CityDict, verbose_name="City", on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name="students")
    course_nums = models.IntegerField(default=0, verbose_name="course_nums")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "Org"
        verbose_name_plural = "Orgs"

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_course(self):
        return self.course_set.all()

    def get_course_num(self):
        return len(self.course_set.all())


    def __str__(self):
        return self.name

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="OrgName", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="TeacherName")
    work_years = models.IntegerField(default=0, verbose_name="WorkYear")
    work_company = models. CharField(max_length=50, verbose_name="Company")
    work_position = models.CharField(max_length=50, verbose_name="Position")
    points = models.CharField(max_length=50, verbose_name="points")
    fav_nums = models.IntegerField(default=0, verbose_name="fav_nums")
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name="Teacher_image", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="click_nums")
    age = models.IntegerField(default=18, verbose_name="age")

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.all().count()

    def get_course(self):
        return self.course_set.all()