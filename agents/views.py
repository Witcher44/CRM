import random
from django.views import generic
from django.views.generic import TemplateView, ListView , DetailView ,CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent, Lead
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin

# Create your views here.
class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agents_list.html"
    
    def get_queryset(self):
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agents_create.html"
    form_class    = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agents-list")

    def form_valid(self, form):
        user = form.save(commit= False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0,10000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation = self.request.user.userprofile
           
            
        )
        send_mail(
            subject = "You are giSHEETALven the opportunity to become and agent",
            message = "You are added as an agent in GDCRM. Please login and continue the great work",
            from_email = "admin@test.com",
            recipient_list = [user.email]

        )
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agents_detail.html'
    def get_queryset(self):
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agents_update.html"
    form_class    = AgentModelForm

   
    
    def get_queryset(self):
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


    def get_success_url(self):
        return reverse("agents:agents-list")
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(AgentUpdateView, self).form_valid(form)
    

    



class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agents_delete.html'
    
    def get_success_url(self):
        return reverse("agents:agents-list")

    def get_queryset(self):
        organisation  = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
