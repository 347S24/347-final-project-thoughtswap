from django.db import models
from django.urls import reverse
# relationship help
# can only have one: ForeignKey, OneToOneField
# foot/M side has the foreign key

# Create your models here.

# A Facilitator is able to create groups and start discussions


# make a block comment for each model
class Facilitator(models.Model):
    """Model representing a facilitator."""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(
        max_length=100, unique=True, null=False, blank=False, default='username')
    # discussion = models.ForeignKey(
    #     'Discussion', on_delete=models.SET_NULL, null=True, blank=True)
    # prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this facilitator."""
        return reverse('facilitator-profile', args=[str(self.id)])
    
    # def get_fac_discussion_url(self):
    #     """Returns the url to access a detail record for this facilitator."""
    #     return reverse('facilitator-discussions', args=[str(self.id)])
    
    # def get_fac_prompt_url(self):
    #     """Returns the url to access a detail record for this facilitator."""
    #     return reverse('facilitator-prompts', args=[str(self.id)])
    
    # def get_fac_group_url(self):
    #     """Returns the url to access a detail record for this facilitator."""
    #     return reverse('facilitator-groups', args=[str(self.id)])
    
    class Meta:
        permissions = (("can_create_groups", "Create Groups"),)
# A Participant is able to join groups and participate in discussions


class Participant(models.Model):
    """Model representing a participant."""
    username = models.CharField(
        max_length=100, null=False, blank=False)  # This is the anonymous username given to the participant
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.username}'

    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this participant."""
    #     return reverse('facilitator-detail', args=[str(self.id)])

# A facilitator may create a group which holds participants and discussions


class Group(models.Model):
    """Model representing a group."""
    facilitator = models.ForeignKey(
        'Facilitator', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False, blank=False, default='Group')
    size = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this group."""
        return reverse('view-group', args=[str(self.id)])

# Thoughts are responses to prompts
class Thought(models.Model):
    content = models.TextField(max_length=1000, help_text='Enter a response')
    prompt = models.ForeignKey('Prompt', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.content

    # def get_absolute_url(self):
        # return reverse('prompt-detail', args=[str(self.id)])

# A prompt is a question or statement that is the focus of a discussion
# A prompt has many thoughts and distributions


class Prompt(models.Model):
    content = models.TextField(
        max_length=1000, help_text='Enter a prompt for the discussion', blank=False, null=False)
    # author = models.TextField(max_length=50)
    discussion = models.ForeignKey(
        'Discussion', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey('Facilitator', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.content}'

# A discussion is a collection of thoughts and prompts
# A discussion may have one group, and many prompts


class Discussion(models.Model):
    """Model representing a discussion."""
    code = models.CharField(max_length=200)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)
    # prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.code

    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this discussion."""
    #     return reverse('discussion-detail', args=[str(self.id)])

# A distribution is a the swapping of the thoughts
# A distribution has one prompt associated with it, and has many 'distributed thoughts' as well


class Distribution(models.Model):
    """Model representing a distribution."""
    id = models.AutoField(primary_key=True)
    prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # thoughts = models.ManyToManyField(Thought)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.prompt}'

# Distributed thoughts associate a user with a new thought


class DistributedThought(models.Model):
    """Model representing a distribution."""
    thought = models.ForeignKey(
        'Thought', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        'Participant', on_delete=models.SET_NULL, null=True)
    distribution = models.ForeignKey(
        'Distribution', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.participant} got {self.thought}'
