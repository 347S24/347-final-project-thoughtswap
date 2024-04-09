from django.db import models
from django.urls import reverse

# Create your models here.
class Facilitator(models.Model):
    """Model representing a facilitator."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    discussions = models.ForeignKey('Discussion', on_delete=models.RESTRICT, null=True)
    prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this facilitator."""
        return reverse('facilitator-detail', args=[str(self.id)])
    
class Student(models.Model):
    """Model representing a student."""
    username = models.CharField(max_length=100) # This is the anonymous username given to the student 
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.username}'
    
    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this student."""
    #     return reverse('facilitator-detail', args=[str(self.id)])

class Prompt(models.Model):
    title = models.TextField(max_length=1000, help_text='Enter a the prompt of the discussion')
    author = models.TextField(max_length=50)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.title}'
    
class Discussion(models.Model):
    """Model representing a discussion."""
    code = models.CharField(max_length=200)
    prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True)
    participants = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this discussion."""
        return reverse('discussion-detail', args=[str(self.id)])

class Thought(models.Model):
    content = models.TextField(max_length=1000, help_text='Enter a response')
    prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('prompt-detail', args=[str(self.id)])
    
