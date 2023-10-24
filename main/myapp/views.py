from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from .forms import TaskForm
# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    template_name = 'task_list.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        return context

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')
    
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterPage, self).get(*args, **kwargs)
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_form2.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
      
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

@login_required  
def all_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks':tasks})

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, complete = True)
    return render(request, 'task_list.html', {'tasks':tasks})

@login_required
def pending_tasks(request):
    tasks = Task.objects.filter(user=request.user, complete=False)
    return render(request, 'task_list.html', {'tasks':tasks})