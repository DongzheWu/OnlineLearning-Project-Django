import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.emial_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from .models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
import  logging
from .models import Banner
logger = logging.getLogger(__name__)
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect('/')
        return render(request, 'login.html', {})
    def post(self, request):
        if request.session.get('is_login', None):
            return render('index.html')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['is_login'] = True
                    request.session['user_name'] = user_name
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"The user has not been activated yet !"})
            else:
                return render(request, 'login.html', {'msg': 'Wrong username or password'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class  RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email = user_name):
                return render(request, "register.html", {"register_form":register_form, "msg":"The email existed"})

            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            user_message = UserMessage()
            user_message.user = user_profile.id

            user_message.message = "Welcome to OnlieStudy"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":forget_form})

class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "The password is not the same"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'user_info'
        return render(request, 'usercenter-info.html', {
            'current_page': current_page,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        res = dict()
        if image_form.is_valid():
            image_form.save()
            res['status'] = 'success'
        else:
            res['status'] = 'fail'
        return HttpResponse(json.dumps(res), content_type='application/json')

class UpdataPwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg": "The password are not the same!"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "The email address already existed"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "the code is wrong"}', content_type='application/json')

class MycourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        current_page = 'mycourse'
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
            'current_page': current_page,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        current_page = 'myfav_org'
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
            'current_page': current_page,
        })

class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        current_page = 'myfav_org'
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
            'current_page': current_page,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        current_page = 'myfav_org'
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
            'current_page': current_page,
        })

class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'mymessage'
        all_message = UserMessage.objects.filter(user=request.user.id)

        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages": messages,
            'current_page': current_page,
        })

class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter()[:8]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'course_orgs': course_orgs,
        })

        return render(request, 'index.html', {})

def page_not_found(request, exception):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response



def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

