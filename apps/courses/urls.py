__author__ = 'wdz'
__date__ = '2019/10/27 19:21'

from django.urls import path, re_path, include
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddComentsView, VideoPlayView

app_name = 'courses'
urlpatterns = [

    path('list/', CourseListView.as_view(), name="course_list"),
    path('add_comment/', AddComentsView.as_view(), name="add_comment"),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    re_path('comment/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),
    re_path('video/(?P<video_id>\d+)', VideoPlayView.as_view(), name='video_play'),






]