from django import forms
from django.forms import ModelForm
from .models import Group, Prompt, Facilitator, Discussion


class GroupModelForm(ModelForm):
    # add logged in user
    def clean_facilitator(self):
        facilitator = self.cleaned_data['facilitator']

    #     # if the name already exists in our database
    #     if facilitator not in Group.objects.all().values_list('facilitator', flat=True):
    #         raise forms.ValidationError("facilitator does not exists. Please enter another one")
        return facilitator
    
    def clean_name(self):
        name = self.cleaned_data['name']

        # if the name already exists in our database
        # if name in Group.objects.all().values_list('name', flat=True):
        #     raise forms.ValidationError("Name already exists. Please enter another one")
        return name

    def clean_size(self):
        size = self.cleaned_data['size']

        # no negative group sizes
        if size < 0:
            raise forms.ValidationError("Group size is too small")
        return size

    class Meta:
        model = Group
        fields = ['name', 'size']

class PromptModelForm(ModelForm):
    class Meta:
        model = Prompt
        fields = ['content', 'discussion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 3})
    
    # def clean_author(self):
    #     author = self.cleaned_data['author']

    #     # if the name already exists in our database
    #     if author in Facilitator.objects.all().values_list('username', flat=True):
    #         raise forms.ValidationError("Author does not exist. Please enter another one")
    #     return author
    
class DiscussionModelForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ['code', 'name', 'group']


    def clean_name(self):
        name = self.cleaned_data['name']

        # if name in Discussion.objects.all().values_list('name', flat=True):
        #     raise forms.ValidationError("name does not exist. Please enter another one")
        return name
    
    def clean_code(self):
        code = self.cleaned_data['code']

        # if the name already exists in our database
        if code in Discussion.objects.all().values_list('code', flat=True):
            print("Code already exists. Please enter another one")
        return code

    def clean_group(self):
        group = self.cleaned_data['group']

        # if the name already exists in our database
        # why does this work? It is looking for groups with the same name?
        if group in Group.objects.all().values_list('name', flat=True):
            print("Group does not exist. Please enter another one")
            raise forms.ValidationError("Group does not exist. Please enter another one")
        return group
    
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        name = cleaned_data.get('name')
        group = cleaned_data.get('group')
        print(code, name)
        print('code, name')

        if code and name:
            if Discussion.objects.filter(code=code, name=name, group=group).exists():
                raise forms.ValidationError("Discussion Exists")
            elif Discussion.objects.filter(code=code).exists():
                raise forms.ValidationError("Code Already In Use")
        return cleaned_data


# class CreateGroupForm(forms.Form):
#     group_name = forms.CharField(label='Group Name', max_length=100)
#     group_size = forms.IntegerField(label='Group Size', min_value=1, max_value=10)

#     def clean_name(self):
#         name = self.cleaned_data['group_name']

#         # if the name already exists in our database
#         if name in Group.objects.all():
#             raise forms.ValidationError("Name already exists")
#         return name

#     def clean_size(self):
#         size = self.cleaned_data['group_size']

#         # no negative group sizes
#         if size < 0:
#             raise forms.ValidationError("Group size is too small")
#         return size
