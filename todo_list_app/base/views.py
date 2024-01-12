from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from csp.decorators import csp_exempt
from django.shortcuts import render
from django.conf import settings
import os

# def custom_error_400(request, exception):
    # return render(request, 'base/400.html', status=400)

# def custom_error_403(request, exception):
    # return render(request, 'base/403.html', status=403)

# def custom_error_404(request, exception):
    # return render(request, 'base/404.html', status=404)

# def custom_error_500(request):
    # return render(request, 'base/500.html', status=500)


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
        
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
   
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    


def css_view(request):
    # Path to your CSS file
    css_file_path = os.path.join(settings.BASE_DIR, 'base', 'static', 'style.css')

    # Read CSS content from the file
    with open(css_file_path, 'r') as css_file:
        css_content = css_file.read()

    # Create an HttpResponse with the correct Content-Type header
    response = HttpResponse(css_content, content_type='text/css')

    # Set the X-Content-Type-Options header to prevent MIME-sniffing
    response['X-Content-Type-Options'] = 'nosniff'

    return response
    
@csp_exempt
def my_view(request):
    response = HttpResponse("Hello, world!")

    response.set_cookie('my_cookie', 'cookie_value', httponly=True)

    # Modify the Content-Security-Policy header to include fonts.googleapis.com
    csp_header = "default-src 'self'; font-src 'self';"
    response["Content-Security-Policy"] = csp_header

    return response