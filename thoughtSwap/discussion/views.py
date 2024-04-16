import random
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Facilitator, Participant, Group, Discussion, Prompt, Thought, Distribution, DistributedThought
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required
# from .forms import CreateGroupForm
from .forms import GroupModelForm, CreatePromptForm


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

    def get_context_data(self, **kwargs):
        context = super(FacilitatorDiscussionView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        
        if 'group_name' in self.kwargs:
            context['group'] = Group.objects.get(
                name=self.kwargs['group_name'])
        else:
            context['group'] = None
        return context


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


class FacilitatorPromptView(CreateView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    form_class = CreatePromptForm
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/profile/prompt_display.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FacilitatorPromptView,
                        self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['facilitator'] = Facilitator.objects.get(
            pk=pk)
        facilitator = get_object_or_404(Facilitator, pk=pk)
        form = CreatePromptForm(
            initial={'content': None, 'author': facilitator, 'discussion': None})
        context['form'] = form
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
    model = Facilitator
    template_name = 'discussion/profile/facilitator_groups.html'
    # success_url = '/discussion/groups/'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FacilitatorGroupView,
                        self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['facilitator'] = Facilitator.objects.get(
            pk=pk)
        facilitator = get_object_or_404(Facilitator, pk=pk)
        form = GroupModelForm(
            initial={'facilitator': facilitator, 'size': 0, 'name': f"{pk}'s Group"})
        context['form'] = form
        return context


def create_group(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    print(facilitator)
    if request.method == 'POST':
        form = GroupModelForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']


            group = Group(name=name, size=size,
                          facilitator=facilitator)
            # This saves the model to the DB
            group.save()
            for _ in range(size):
                participant = Participant(username=generate_username(group), group=group)
                participant.save()

            return redirect(reverse('view-group', kwargs={'pk': pk, 'name': group.name}))
    return HttpResponse("Error creating group: Group with that name already exists")
    # else:
    #     form = GroupModelForm(
    #         initial={'facilitator': facilitator, 'size': 0, 'name': 'Group Name'})

    # context = {
    #     'facilitator': facilitator,
    #     'form': form,
    #     'group': group,
    # }


class GroupView(CreateView):
    # create group form on profile page
    model = Facilitator
    form_class = GroupModelForm
    template_name = 'discussion/profile/group_view.html'

    # process context that is being passed in

    def get_context_data(self, **kwargs):
        context = super(GroupView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        context['group'] = Group.objects.get(
            name=self.kwargs['name'])

        return context


def create_prompt(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    if request.method == 'POST':
        form = CreatePromptForm(request.POST)

        if form.is_valid():
            facilitator = form.cleaned_data['author']
            content = form.cleaned_data['content']
            discussion = form.cleaned_data['discussion']

            prompt = Prompt(content=content, author=facilitator,
                            discussion=discussion)
            # This saves the model to the DB
            prompt.save()
            return redirect(reverse('facilitator-prompts', kwargs={'pk': pk}))
    return HttpResponse("Error creating prompt")

class GroupUpdate(UpdateView):
    model = Group
    # Not recommended (potential security issue if more fields added)
    fields = 'name, size'
    # permission_required = 'catalog.change_author'

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('<int:pk>/groups/')
    template_name ='discussion/profile/group_confirm_delete.html'
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete-group", kwargs={"pk": self.object.pk})
            )
    # # success_url = 
    # permission_required = 'catalog.delete_author'

    # def form_valid(self, form):
    #     try:
    #         self.object.delete()
    #         return HttpResponseRedirect(self.success_url)
    #     except Exception as e:
    #         return HttpResponseRedirect(
    #             reverse("author-delete", kwargs={"pk": self.object.pk})
    #         )

# other methods
# generates a numerical random username
def generate_username(group):
    id = str(random.randint(100000, 999999))
    # Check if it already exists in the group
    if id in group.participant_set.all().values_list('username', flat=True):
        return generate_username(group)
    return id