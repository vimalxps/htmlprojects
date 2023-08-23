from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from. models import Task

from django.views.generic import ListView

from django.views.generic.detail import DetailView

from django.views.generic.edit import UpdateView

from django.views.generic.edit import DeleteView

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')



class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'uv'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetails',kwargs={'pk':self.object.id})

class TaskDetailView(DetailView):
    model=Task
    template_name = 'details.html'
    context_object_name = 'obj'

class Tasklistview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'dtask'


# Create your views here.
def home(request):
    dtask = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')

        task=Task(name=name,priority=priority,date=date)
        task.save()

    return render(request,'home.html',{'dtask':dtask})
# def details(request):
#
#     return render(request,'details.html',)

def delete(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=TodoForm(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})