import random
from django.db.models.query import QuerySet
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
from .forms import DiscussionModelForm, GroupModelForm, PromptModelForm


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

        if 'code' in self.kwargs:
            context['discussion'] = Discussion(code=self.kwargs['code'])
        else:
            context['discussion'] = {'code': 0}
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
        form = PromptModelForm(initial={'content': None, 'discussion': None})
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


def DiscussionDetailView(request, pk, code, name):
    facilitator = Facilitator.objects.get(pk=pk)
    group = Group.objects.get(facilitator=facilitator, name=name)
    disc = Discussion.objects.get(group=group, code=code)
    context = {
        'facilitator': facilitator,
        'discussion': disc,
    }
    return render(request, 'discussion/profile/discussion_detail.html', context=context)
    # template_name = 'discussion/profile/discussion_detail.html'
    # queryset =

    # def get_queryset(self):
    #     print("HELLO???\n\n\n\n\n\n\n\n\n")
    #     self.facilitator = Facilitator.objects.get(pk=self.kwargs['pk'])
    #     if ('code' in self.kwargs and 'name' in self.kwargs):
    #         group = Group.objects.get(facilitator=self.facilitator, name=self.kwargs['name'])
    #         self.discussion = Discussion.objects.filter(group=group, code=self.kwargs['code'])
    #     else:
    #         self.discussion = Discussion.objects.all()
    #     print('disc', self.discussion)
    #     return self.discussion

    # def get_context_data(self, **kwargs):
    #     print("running context data\n\n\n\n\n\n\n\n\n")
    #     context = super(DiscussionDetailView,
    #                     self).get_context_data(**kwargs)
    #     context['facilitator'] = self.facilitator

    #     context['discussion'] = self.discussion
    #     print('\n\n\n\n\n\n\n')
    #     print('group', context['group'])
    #     print('code', self.kwargs['code'])
    #     print('\n\n\n\n\n\n\n')
    #     return context


class ParticipantDiscussionView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_view.html'

    def get_context_data(self, **kwargs):
        context = super(ParticipantDiscussionView,
                        self).get_context_data(**kwargs)
        context['discussion'] = Discussion.objects.get(
            code=self.kwargs['code'])
        return context
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
                               'content': prompt.content, 'discussion': prompt.discussion})
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

class PromptDelete(DeleteView):
    model = Prompt
    template_name = 'discussion/profile/prompt_confirm_delete.html'

    def get_success_url(self):
        facilitator_pk = self.kwargs['facilitator_pk']
        return reverse_lazy('facilitator-prompts', kwargs={'pk': facilitator_pk})


def create_group(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    # print(facilitator)
    if request.method == 'POST':
        form = GroupModelForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
        # facilitator = form.cleaned_data['facilitator']

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


# class GroupUpdateView(UpdateView):
#     model = Group
#     # Not recommended (potential security issue if more fields added)
#     fields = ['name', 'size']
#     template_name = 'discussion/profile/group_update.html'
#     # permission_required = 'catalog.change_prompt'

#     def get_context_data(self, **kwargs):
#         context = super(GroupUpdateView,
#                         self).get_context_data(**kwargs)
#         facilitator = Facilitator.objects.get(pk=self.kwargs['pk'])
#         group = Group.objects.get(name=self.kwargs['name'])
#         print(group)
#         context['facilitator'] = facilitator
#         context['group'] = group
#         form = GroupModelForm(
#             initial={'facilitator': facilitator, 'name': group.name, 'size': group.size})
#         context['form'] = form
#         return context

def GroupUpdateView(request, pk, name):
    facilitator = Facilitator.objects.get(pk=pk)
    group = Group.objects.get(facilitator=facilitator, name=name)
    form = GroupModelForm(initial={'name': group.name, 'size': group.size})

    context = {
        'facilitator': facilitator,
        'group': group,
        'form': form,
    }
    return render(request, 'discussion/profile/group_update.html', context=context)


def GroupUpdate(request, pk, name):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    group = get_object_or_404(Group, facilitator=facilitator, name=name)
    curr_size = group.size
    print(group)
    if request.method == 'POST':
        form = GroupModelForm(request.POST, instance=group)
        print('form\n\n\n\n\n\n\n\n\n')
        if form.is_valid():
            size = form.cleaned_data['size']
            size_diff = abs(size - curr_size)
            print('size diff', size_diff)
            for _ in range(size_diff):
                participant = Participant(
                    username=generate_username(group), group=group)
                participant.save()
            form.save()
            return redirect(reverse('view-group', kwargs={'pk': pk, 'name': name}))
    return HttpResponse("Error Updating Group")


class GroupDelete(DeleteView,):
    model = Group
    template_name = 'discussion/profile/group_confirm_delete.html'

    def get_success_url(self):
        facilitator_pk = self.object.facilitator.pk
        return reverse_lazy('view-group', kwargs={'pk': facilitator_pk})
    
# other methods
# generates a numerical random username


def CreateDiscussionView():
    form = DiscussionModelForm(
        initial={'code': 0, 'name': 'Discussion 0', 'group': None})
    context['form'] = form

    return redirect(reverse('facilitator-view', kwargs={'pk': pk}))


def create_discussion(request):
    if request.method == 'POST':
        print('posted\n\n\n\n\n\n\n\n\n')

        form = DiscussionModelForm(request.POST)

        if form.is_valid():
            print('valid\n\n\n\n\n\n\n\n\n')

            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            group = form.cleaned_data['group']

            discussion = Discussion(name=name, group=group, code=code)
            # This saves the model to the DB
            discussion.save()
            # if form.cleaned_data['group'] is None:
            #     return redirect(reverse('facilitator-view', kwargs={'pk': group.facilitator.pk}))
            # else:
            return redirect(reverse('facilitator-view', kwargs={'pk': group.facilitator.pk, 'code': discussion.code}))
    else:
        print('no data\n\n\n\n\n\n\n\n\n')
        form = DiscussionModelForm(initial={'code': 0, 'name': 'Discussion 0', 'group': None})
        context = {'form': form,}
        return render(request, 'discussion/start_discussion.html', context=context)
    return HttpResponse("Error creating Discussion")
    # else:
    #     redirect(reverse('login-view'))


def generate_username(group):
    id = str(random.randint(100000, 999999))
    # Check if it already exists in the group
    if id in group.participant_set.all().values_list('username', flat=True):
        return generate_username(group)
    return id
