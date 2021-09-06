from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from core.models import *
from datetime import date
from .forms import *
from .decorators import *



# Create your views here.


class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/admin_home.html'
    login_url = 'core:user-login'
    redirect_field_name = 'core:user-login'

    def get_context_data(self, **kwargs):
        users = Attendance.objects.filter(approved=False)
        context = {'users': users,}
        return context


class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'
    login_url = 'core:user-login'
    redirect_field_name = 'core:user-login'

    def get_context_data(self, **kwargs):
        attendances = Attendance.objects.filter(user=self.request.user)
        context = {'attendances': attendances,}
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'core/user_register.html'
    @method_decorator(unauthenticated_user)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + email)
            return redirect('core:user-login')
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    form_class = UserLogin
    initial = {'key': 'value'}
    template_name = 'core/login.html'
    @method_decorator(unauthenticated_user)
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            if(request.user.user_type == "Admin"):
                return redirect('core:home')
            else:
                return redirect('core:user-home')

        else:
            messages.info(request, 'Username OR Password is Incorrect')
        return render(request, 'core/login.html', {'form': form})


def UserLogout(request):
    logout(request)
    return redirect('core:user-login')


class AttendanceRequestView(LoginRequiredMixin, TemplateView):
    # template_name = 'core/index.html'
    login_url = 'core:user-login'
    redirect_field_name = 'core:user-login'

    def post(self, request, *args, **kwargs):
        today = date.today()
        if Attendance.objects.filter(user=request.user, date=today).exists():
            messages.info(request, 'Request Already Sent')
            return redirect('core:user-home')
        else:
            user = Attendance.objects.create(user=request.user)
            messages.info(request, 'Request Sent Successfully')
            return redirect('core:user-home')
        return redirect('core:user-home')


class ApproveAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'core/admin_home.html'
    login_url = 'core:user-login'
    redirect_field_name = 'core:user-login'

    def get(self, request, user_id, *args, **kwargs):

        user = Attendance.objects.filter(user=user_id).update(approved=True)
        messages.info(request, 'Attendance Marked!')
        return redirect('core:home')
