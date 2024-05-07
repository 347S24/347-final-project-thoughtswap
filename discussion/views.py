from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import timezone
import random
from django.db.models.query import QuerySet
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
# from .forms import CreateGroupForm
from .forms import DiscussionModelForm, GroupModelForm, PromptModelForm, FacilitatorForm

# find discussion and render with socket 
from django.contrib.auth.forms import UserCreationForm

def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html with the data in the context variable
    print('request.user')
    print(request.user)
    return render(request, 'index.html', {"user": request.user})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        print('signup view')
        return super().get(request, *args, **kwargs)

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
            context['discussion'] = Discussion.objects.get(
                code=self.kwargs['code'])
        else:
            context['discussion'] = {'code': 0}

        form = PromptModelForm(
            initial={'content': None, 'discussion': context['discussion'].code})
        context['form'] = form
        if context['discussion'].prompt_set.last():
            context['thoughts'] = context['discussion'].prompt_set.last(
            ).thought_set.all()
        return context


class FacilitatorProfileView(LoginRequiredMixin, generic.DetailView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    template_name = 'discussion/profile/facilitator_profile.html'
    context_object_name = 'facilitator'

    def get_object(self):
        return get_object_or_404(Facilitator, pk=self.kwargs['pk'])


class FacilitatorPromptView(CreateView):
    # eventually need LoginRequiredMixin
    model = Facilitator
    form_class = PromptModelForm
    template_name = 'discussion/profile/prompt_display.html'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FacilitatorPromptView,
                        self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['facilitator'] = Facilitator.objects.get(
            pk=pk)
        form = PromptModelForm(initial={'content': None, 'discussion': None})
        context['form'] = form
        return context


class LoginPromptView(LoginView):
    print("login working?")
    template_name = 'discussion/registration/login.html'


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


class ParticipantLogin(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_login.html'


class ParticipantDiscussionView(generic.ListView):
    model = Participant
    template_name = 'discussion/participant_view.html'

    def get_context_data(self, **kwargs):
        context = super(ParticipantDiscussionView,
                        self).get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')

        if 'code' in self.kwargs:
            code = self.kwargs['code']
            print('code given and its', code)
        else:
            code = self.request.GET.get('code')

        context['discussion'] = Discussion.objects.get(
            code=code)
        if context['discussion'].prompt_set.last():
            context['thoughts'] = context['discussion'].prompt_set.last(
            ).thought_set.all()
        print('thoughts', context['thoughts'])
        # print('message recieved', context['message'], '\n\n\n\n\n\n\n\n\n')
        return context
    # paginate_by = 10


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

def register_facilitator(request):
    username = request.POST.get('username')
    # Get first and last name as well
    if request.method == 'POST':
        form = FacilitatorForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            # Validate first and last name

            # Enter first and last name 
            facilitator = Facilitator(username=username)
            
            # Add permission to facilitator (code in discord)
            facilitator.save()
            return redirect(reverse('facilitator-profile', kwargs={'pk': facilitator.pk}))

        return HttpResponse(f'Error with the form {form.errors}', status=400)

    else:
        form = FacilitatorForm()
    return render(request, 'index.html', {'form': form})
     
    
@csrf_exempt
@require_POST
def update_prompt(request):
    prompt = request.POST.get('prompt')
    pk = request.POST.get('pk')
    code = request.POST.get('code')
    context = {}
    context['prompt'] = prompt
    context['thoughts'] = prompt.thought_set.all()
    context['facilitator'] = Facilitator.objects.get(pk=pk)
    context['discussion'] = Discussion.objects.get(code=code)
    return redirect(reverse('facilitator-prompts', kwargs={'pk': pk}))
        
def create_prompt(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    if request.method == 'POST':
        form = PromptModelForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content'].strip()
            discussion = form.cleaned_data['discussion']

            prompt = Prompt(content=content, author=facilitator,
                            discussion=discussion)
            # This saves the model to the DB
            prompt.save()
            return redirect(reverse('facilitator-prompts', kwargs={'pk': pk}))
    return HttpResponse("Error creating prompt")


def save_prompt(request, pk):
    facilitator = get_object_or_404(Facilitator, pk=pk)
    if request.method == 'POST':
        form = PromptModelForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content'].strip()
            discussion = form.cleaned_data['discussion']

            prompt = Prompt(content=content, author=facilitator,
                            discussion=discussion)
            # This saves the model to the DB
            prompt.save()
            return redirect(reverse('facilitator-view', kwargs={'pk': pk, 'code': discussion.code}))
    return HttpResponse("Error creating prompt")


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
                               'content': prompt.content.strip(), 'discussion': prompt.discussion})
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
        context['group'] = get_object_or_404(Group, name=self.kwargs['name'])

        return context


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


class GroupDelete(DeleteView):
    # delete view default uses pk/slug field to look up the object
    model = Group
    template_name = 'discussion/profile/group_confirm_delete.html'

    # overrite get_object method to change how object will be looked up
    def get_object(self):
        facilitator_pk = self.kwargs['pk']
        name = self.kwargs['name']
        return get_object_or_404(Group, facilitator=facilitator_pk, name=name)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('facilitator-groups', kwargs={'pk': pk})


class ThoughtDelete(DeleteView):
    # delete view default uses pk/slug field to look up the object
    model = Thought
    template_name = 'discussion/thought_confirm_delete.html'

    # overrite get_object method to change how object will be looked up
    # def get_object(self):
    #     id = self.kwargs['id']
    #     return get_object_or_404(Thought, id=id)

    def get_context_data(self, **kwargs):
        context = super(ThoughtDelete,
                        self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['code'] = self.kwargs['code']
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        code = self.kwargs['code']
        return reverse_lazy('facilitator-view', kwargs={'pk': pk, 'code': code})


def create_discussion(request):
    context = {}
    if request.method == 'POST':
        form = DiscussionModelForm(request.POST)
        if form.is_valid():
            print('valid\n\n\n\n\n\n\n\n\n')

            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            group = form.cleaned_data['group']

            if (Discussion.objects.get(code=code, name=name, group=group)):
                    # TODO: Get correct group facilitator to put into pk
                    return redirect(reverse('facilitator-view', kwargs={'pk': 1, 'code': code}))
            else:
                discussion = Discussion(name=name, group=group, code=code)
                # This saves the model to the DB
                discussion.save()
                print("saved disc,", discussion)
                return redirect(reverse('facilitator-view', kwargs={'pk': group.facilitator.pk, 'code': code}))
        else:
            context['errors'] = form.errors
    else:
        print('no data\n\n\n\n\n\n\n\n\n')
        form = DiscussionModelForm(
            initial={'code': 0, 'name': 'Discussion 0', 'group': None})
    context['form'] = form
    return render(request, 'discussion/start_discussion.html', context=context)


def generate_username(group):
    id = str(random.randint(100000, 999999))
    # Check if it already exists in the group
    if id in group.participant_set.all().values_list('username', flat=True):
        return generate_username(group)
    return id
