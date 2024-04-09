from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Facilitator, Participant, Group, Discussion, Prompt, Thought, Distribution, DistributedThought
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# from .forms import CreateGroupForm
from .forms import GroupModelForm


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

    def get_context_data(self, **kwargs):
        context = super(FacilitatorProfileView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(pk=self.kwargs['pk'])
        return context

class FacilitatorPromptView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/prompt_display.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FacilitatorPromptView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        return context

class PastDiscussionView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/discussion_display.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PastDiscussionView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        return context


class ParticipantDiscussionView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_view.html'
    # paginate_by = 10


class ParticipantGroupView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_groups.html'
    # paginate_by = 10


# @permission_required('discussion.can_create_groups', raise_exception=True)
class FacilitatorGroupView(generic.ListView):
    model = Participant
    template_name = 'discussion/profile/facilitator_groups.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FacilitatorGroupView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        return context

    # create group form on profile page
    def create_group(request, pk):
        facilitator = get_object_or_404(Facilitator, pk=pk)
        print(facilitator)
        if request.method == 'POST':
            form = GroupModelForm(request.POST)

            if form.is_valid():
                group_name = form.cleaned_data['group_name']
                group_size = form.cleaned_data['group_size']

            group = Group(name=group_name, size=group_size,
                        facilitator=facilitator)
            group.save()

            print("saved group", group)
        else:
            form = GroupModelForm(
                initial={'facilitator': facilitator, 'size': 0, 'name': 'Group Name'})

        context = {
            'form': form,
            'group': group,
        }
        return render(request, 'discussion/profile/facilitator_groups.html', context)

# def edit_group_post(request, name):
#     group = Group.objects.get(name=name)
#     if request.method == 'POST':
#         group_size = request.POST.get('group_size')

#         group = Group(name=group_name, size=group_size)
#         group.save()

#         print("saved group", group)
