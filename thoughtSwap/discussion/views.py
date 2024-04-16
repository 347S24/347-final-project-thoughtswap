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
from .forms import GroupModelForm, PromptModelForm


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
    form_class = PromptModelForm
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
        form = PromptModelForm(
            initial={'content': None, 'author': facilitator, 'discussion': None})
        context['form'] = form
        return context


class PromptDetailView(generic.DetailView):
    model = Prompt
    # Not recommended (potential security issue if more fields added)
    fields = ['content']
    template_name = 'discussion/profile/prompt_detail.html'
    # permission_required = 'catalog.change_prompt'

    def get_context_data(self, **kwargs):
        context = super(PromptDetailView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        context['prompt'] = Prompt.objects.get(
            id=self.kwargs['id'])
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


class DiscussionDetailView(generic.DetailView):
    model = Discussion
    template_name = 'discussion/profile/discussion_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetailView,
                        self).get_context_data(**kwargs)
        context['discussion'] = Discussion.objects.get(
            code=self.kwargs['code'])
        context['name'] = self.kwargs['name']
        return context


class ParticipantDiscussionView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_view.html'
    # paginate_by = 10


class ParticipantSwapView(generic.ListView):
    # eventually need LoginRequiredMixin
    model = Distribution
    # context_object_name = 'facilitator_list'
    # queryset = Facilitator.objects.all()
    template_name = 'discussion/post_swap.html'
    # paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super(PastDiscussionView,
    #                     self).get_context_data(**kwargs)
    #     context['distribution'] = Facilitator.objects.get(
    #         id=self.kwargs['swapid'])
    #     return context


class ParticipantGroupView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_groups.html'
    # paginate_by = 10


# @permission_required('discussion.can_create_groups', raise_exception=True)
class FacilitatorGroupView(generic.ListView):
    model = Facilitator
    template_name = 'discussion/profile/group_display.html'
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

# Crud things


def create_prompt(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    if request.method == 'POST':
        form = PromptModelForm(request.POST)

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


# class PromptUpdate(PermissionRequiredMixin, UpdateView):


class PromptUpdateView(UpdateView):
    model = Prompt
    # Not recommended (potential security issue if more fields added)
    fields = ['content']
    template_name = 'discussion/profile/prompt_update.html'
    # permission_required = 'catalog.change_prompt'

    def get_context_data(self, **kwargs):
        context = super(PromptUpdateView,
                        self).get_context_data(**kwargs)
        facilitator = Facilitator.objects.get(pk=self.kwargs['pk'])
        prompt = Prompt.objects.get(id=self.kwargs['id'])
        context['facilitator'] = facilitator
        context['prompt'] = prompt
        form = PromptModelForm(initial={
                               'content': prompt.content, 'author': facilitator, 'discussion': prompt.discussion})
        context['form'] = form
        return context


def PromptUpdate(request, pk, id):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    prompt = get_object_or_404(Prompt, id=id)
    print('facilitator', facilitator)
    print('prompt', prompt)
    if request.method == 'POST':
        form = PromptModelForm(request.POST, instance=prompt)

        if form.is_valid():
            form.save()
            return redirect(reverse('prompt-detail', kwargs={'pk': pk, 'id': id}))
    return HttpResponse("Error Updating Prompt")


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
                participant = Participant(
                    username=generate_username(group), group=group)
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
    template_name = 'discussion/profile/group_detail.html'

    # process context that is being passed in

    def get_context_data(self, **kwargs):
        context = super(GroupView,
                        self).get_context_data(**kwargs)
        context['facilitator'] = Facilitator.objects.get(
            pk=self.kwargs['pk'])
        # context['group'] = Group.objects.get(
        #     name=self.kwargs['name'])
        context['group'] = get_object_or_404(Group, name=self.kwargs['name'])

        return context


class GroupUpdateView(UpdateView):
    model = Group
    # Not recommended (potential security issue if more fields added)
    fields = ['name', 'size']
    template_name = 'discussion/profile/group_update.html'
    # permission_required = 'catalog.change_prompt'

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView,
                        self).get_context_data(**kwargs)
        facilitator = Facilitator.objects.get(pk=self.kwargs['pk'])
        group = Group.objects.get(name=self.kwargs['name'])
        print(group)
        context['facilitator'] = facilitator
        context['group'] = group
        form = GroupModelForm(
            initial={'facilitator': facilitator, 'name': group.name, 'size': group.size})
        context['form'] = form
        return context


def GroupUpdate(request, pk, name):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    group = get_object_or_404(Group, name=name)
    curr_size = group.size

    if request.method == 'POST':
        form = PromptModelForm(request.POST, instance=group)

        if form.is_valid():
            size = form.cleaned_data['size']
            size_diff = abs(size - curr_size)
            for _ in range(size_diff):
                participant = Participant(
                    username=generate_username(group), group=group)
                participant.save()
            form.save()
            return redirect(reverse('group-detail', kwargs={'pk': pk, 'name': name}))
    return HttpResponse("Error Updating Group")


class GroupDelete(DeleteView):
    model = Group
    template_name = 'discussion/profile/group_confirm_delete.html'
    def get_success_url(self):
        facilitator_pk = self.object.facilitator.pk
        return reverse_lazy('facilitator-groups', kwargs={'pk': facilitator_pk})
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
