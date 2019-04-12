from .models import Member
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, CreateView
from .forms import MemberActivationForm, MemberCreationForm

class MemberActivationView(FormView):
    form_class = MemberActivationForm
    success_url = '/'
    template_name = 'activation.html'
    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), **{'user': self.get_object()}}

    def get_object(self):
        return get_object_or_404(Member, user__username=self.kwargs['username'])

class MemberCreationView(CreateView):
    form_class = MemberCreationForm
    template_name = 'signup.html'
    def get_success_url(self):
        return reverse('users:activation', args=[self.request.POST['username']])
