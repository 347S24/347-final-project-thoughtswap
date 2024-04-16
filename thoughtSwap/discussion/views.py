from django.views import generic
from django.shortcuts import render
from .models import Facilitator, Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView


def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

class FacilitatorDiscussionView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/facilitator_view.html'
    # paginate_by = 10

class FacilitatorProfileView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/facilitator_profile.html'
    # paginate_by = 10

class FacilitatorPromptView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/prompt_display.html'
    # paginate_by = 10

class PastDiscussionView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/discussion_display.html'
    # paginate_by = 10

class ParticipantDiscussionView(generic.ListView):
    model = Student
    template_name = 'discussion/participant_view.html'
    # paginate_by = 10

class LoginPromptView(LoginView):
    template_name = 'registration/login.html'

class ParticipantGroupView(generic.ListView):
    model = Student
    template_name = 'discussion/participant_groups.html'
    # paginate_by = 10


class FacilitatorGroupView(generic.ListView):
    model = Student
    template_name = 'discussion/profile/facilitator_groups.html'
    # paginate_by = 10