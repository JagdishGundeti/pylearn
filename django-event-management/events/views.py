from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Q
import datetime

from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
    EventImage,
    EventAgenda

)
from .forms import EventForm, EventImageForm, EventAgendaForm, EventCreateMultiForm


# Event category list view
class EventCategoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventCategory
    template_name = 'events/event_category.html'
    context_object_name = 'event_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventCategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'code', 'image', 'priority', 'status']
    template_name = 'events/create_event_category.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context


class JobCategoryListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = JobCategory
    template_name = 'events/job_category.html'
    context_object_name = 'job_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context


class JobCategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = JobCategory
    fields = ['name']
    template_name = 'events/create_job_category.html'
    success_url = reverse_lazy('job-category-list')

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventCategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = EventCategory
    fields = ['name', 'code', 'image', 'priority', 'status']
    template_name = 'events/edit_event_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventCategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model =  EventCategory
    template_name = 'events/event_category_delete.html'
    success_url = reverse_lazy('event-category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class JobCategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = JobCategory
    fields = ['name']
    template_name = 'events/edit_job_category.html'
    success_url = reverse_lazy('job-category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class JobCategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model =  JobCategory
    template_name = 'events/job_category_delete.html'
    success_url = reverse_lazy('job-category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

@login_required(login_url='login')
def create_event(request):
    event_form = EventForm()
    event_image_form = EventImageForm()
    event_agenda_form = EventAgendaForm()
    catg = EventCategory.objects.all()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_image_form = EventImageForm(request.POST, request.FILES)
        event_agenda_form = EventAgendaForm(request.POST)
        if event_form.is_valid() and event_image_form.is_valid() and event_agenda_form.is_valid():
            ef = event_form.save()
            created_updated(Event, request)
            event_image_form.save(commit=False)
            event_image_form.event_form = ef
            event_image_form.save()
            
            event_agenda_form.save(commit=False)
            event_agenda_form.event_form = ef
            event_agenda_form.save()
            return redirect('event-list')
    context = {
        'form': event_form,
        'form_1': event_image_form,
        'form_2': event_agenda_form,
        'ctg': catg
    }
    return render(request, 'events/create.html', context)

class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = EventCreateMultiForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        evt = form['event'].save()
        event_image = form['event_image'].save(commit=False)
        event_image.event = evt
        event_image.save()

        event_agenda = form['event_agenda'].save(commit=False)
        event_agenda.event = evt
        event_agenda.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ctg'] = EventCategory.objects.all()
        context['user_login_name'] = self.request.user.first_name
        return context


class EventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['category', 'name', 'uid', 'description', 'scheduled_status', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
    template_name = 'events/edit_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('event-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class AddEventMemberCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventMember
    fields = ['event', 'user', 'attend_status', 'status']
    template_name = 'events/add_event_member.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        self.send_email(self.request)
        return super().form_valid(form)

    def send_email(self, request, **kwargs):
        my_data = request.POST

        first_name=self.request.user.first_name
        email_id=self.request.user.email_id
        
        # event_obj = Event.objects.filter(uid=request.POST['event'])
        event_obj = Event.objects.get(pk=request.POST['event'])

        msg = EmailMessage('Welcome '+ first_name,
            "You are added to event '" + event_obj.name + "'",
            'gmail@rajnikanth.com', [email_id])
        msg.conen_subpe = "html"
        # msg.attach_file(r+'.png')
        msg.send()
        # return redirect('join-event-list')
        # return http.HttpResponse("Post")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class JoinEventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/joinevent_list.html'
    context_object_name = 'eventmember'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class RemoveEventMemberDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/remove_event_member.html'
    success_url = reverse_lazy('join-event-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class EventUserWishListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventUserWishList
    template_name = 'events/event_user_wish_list.html'
    context_object_name = 'eventwish'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class AddEventUserWishListCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventUserWishList
    fields = ['event', 'user', 'status']
    template_name = 'events/add_event_user_wish.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class RemoveEventUserWishDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventUserWishList
    template_name = 'events/remove_event_user_wish.html'
    success_url = reverse_lazy('event-wish-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class UpdateEventStatusView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['status']
    template_name = 'events/update_event_status.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context
       


class CompleteEventList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    # template_name = 'events/complete_event_list.html'
    template_name = 'events/generic_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(status='completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['build_page_title'] = 'Complete Event List'
        context['user_login_name'] = self.request.user.first_name
        return context

class ActiveEventList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/generic_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(status='active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['build_page_title'] = 'Active Event List'
        context['user_login_name'] = self.request.user.first_name
        return context

class EventEndReachedButActive(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/generic_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(
            Q(end_date__lt = datetime.datetime.now()) & 
            Q(status='active') 
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['build_page_title'] = 'Event End Reached But Active'
        context['user_login_name'] = self.request.user.first_name
        return context


class ActiveEventOfTodayList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/generic_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(
            Q(end_date = datetime.datetime.now()) & 
            Q(status='active') 
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['build_page_title'] = 'Active Events Of Today'
        context['user_login_name'] = self.request.user.first_name
        return context

class OpenMessageNotification(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'events/generic_event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(
            Q(end_date = datetime.datetime.now()) & 
            Q(status='active') 
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['build_page_title'] = 'Active Events Of Today'
        context['user_login_name'] = self.request.user.first_name
        return context

class AbsenseUserList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/absense_user_list.html'
    context_object_name = 'absenseuser'

    def get_queryset(self):
        return EventMember.objects.filter(attend_status='absent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class CompleteEventUserList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/complete_event_user_list.html'
    context_object_name = 'completeuser'

    def get_queryset(self):
        return EventMember.objects.filter(attend_status='completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class CreateUserMark(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = UserCoin
    fields = ['user', 'gain_type', 'gain_coin', 'status']
    template_name = 'events/create_user_mark.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

class UserMarkList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = UserCoin
    template_name = 'events/user_mark_list.html'
    context_object_name = 'usermark'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_login_name'] = self.request.user.first_name
        return context

@login_required(login_url='login')
def search_event_category(request):
    if request.method == 'POST':
       data = request.POST['search']
       event_category = EventCategory.objects.filter(name__icontains=data)
       context = {
           'event_category': event_category
       }
       return render(request, 'events/event_category.html', context)
    return render(request, 'events/event_category.html')

@login_required(login_url='login')
def search_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       events = Event.objects.filter(name__icontains=data)
       context = {
           'events': events
       }
       return render(request, 'events/event_list.html', context)
    return render(request, 'events/event_list.html')
