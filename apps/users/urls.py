from django.urls import path, include, re_path


from .views import UserInfoView, UploadImageView, UpdataPwdView, SendEmailCodeView, MyMessageView
from .views import UpdateEmailView, MycourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView
app_name = 'users'
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    path('update/pwd/', UpdataPwdView.as_view(), name="update_pwd"),

    # send emial verify code
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),

    path('mycourse/', MycourseView.as_view(), name="mycourse"),
    path('myfav/org', MyFavOrgView.as_view(), name="myfav_org"),
    path('myfav/teacher', MyFavTeacherView.as_view(), name="myfav_teacher"),
    path('myfav/course', MyFavCourseView.as_view(), name="myfav_course"),
    path('mymessage/', MyMessageView.as_view(), name="mymessage")
]