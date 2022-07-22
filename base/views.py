from datetime import datetime
from pydoc import describe
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from base.models import Course, Participant
from base.forms import ParticipantForm, CourseCreationForm
from django.db.models import Q 


DEFAULT_DATE = datetime(1970,1,1,00,00,00)


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return redirect('home')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        return redirect('home')

    context = {'page': page}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')

    return render(request, 'login.html', context={'form': form})


class HomeView(ListView):
    template_name = 'base/home.html'
    model = Course
    context_object_name = 'courses'
    
    def get_queryset(self):
        course_title_q = self.request.GET.get('course_title_q') if self.request.GET.get('course_title_q') else ''
        course_starts_q = self.request.GET.get('course_starts_q') if self.request.GET.get('course_starts_q') else DEFAULT_DATE
        
        return self.model.objects.filter(
            Q(title__icontains=course_title_q) &
            Q(start_date__gte=course_starts_q)
        ) 
        
       

class CourseView(DetailView, FormView):
    model = Course
    form_class = ParticipantForm
    template_name = 'base/course.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['contact_form'] = ParticipantForm()
        
        return context

    def post(self, request, *args, **kwargs):
        participant, created = Participant.objects.get_or_create(
            user=request.user,
            course=self.get_object(),
            contact_email = request.POST.get('contact_email')
        )
            
        return redirect('home')
    
    
class CreateCourseView(FormView):
    form_class = CourseCreationForm
    template_name = 'base/create-course.html'
    success_url = 'home'
    
    def post(self, request, *args, **kwargs):
        
        course, created = Course.objects.get_or_create(
            title = request.POST.get('title'),
            description=request.POST.get('description'),
            host = request.user,
            start_date = request.POST.get('start_date'),
            end_date = request.POST.get('end_date')
        )

        return redirect('home')