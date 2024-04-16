from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    
    # Discussion pages
    path('facilitator/<int:pk>/<str:group_name>', views.FacilitatorDiscussionView.as_view(), name='facilitator-w-group-view'),
    path('facilitator/<int:pk>', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    
    # Facilitator profile links
    path('<int:pk>/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    
    # Prompt CRUD/View
    path('<int:pk>/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('<int:pk>/view-prompt/<int:id>', views.PromptDetailView.as_view(), name='prompt-detail'),
    path('<int:pk>/prompt/create', views.create_prompt, name='create-prompt'),
    path('<int:pk>/change-prompt/<int:id>', views.PromptUpdateView.as_view(), name='change-prompt'),
    path('<int:pk>/update-prompt/<int:id>', views.PromptUpdate, name='update-prompt'),
    
    # Group CRUD/View
    path('<int:pk>/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    path('<int:pk>/group/create', views.create_group, name='create-group'),
    path('<int:pk>/view-group/<str:name>', views.GroupView.as_view(), name='view-group'),
    path('<int:pk>/change-group/<str:name>', views.GroupUpdateView.as_view(), name='change-group'),
    # path('<int:pk>/update-group/<str:name>', views.GroupUpdate, name='update-group'),
    path('<int:pk>/update-group', views.GroupUpdate.as_view(), name='update-group'),
    path('<int:pk>/delete-group', views.GroupDelete.as_view(), name='delete-group'),
    
    # Discussion CRUD/View
    path('<int:pk>/discussion', views.PastDiscussionView.as_view(), name='facilitator-discussions'),
    path('<int:pk>/view-discussion/<str:name>/<int:code>', views.DiscussionDetailView.as_view(), name='view-responses'),
    
    # Swap CRUD/View
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    path('participant/swap', views.ParticipantSwapView.as_view(), name='participant-swap-view'),
    # path('participant/swap<int:swapid>', views.ParticipantDiscussionView.as_view(), name='participant-view'),

    # path('profile/groups/', create_group_post, name='facilitator-groups'),
    path('profile/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    path('groups/', views.ParticipantGroupView.as_view(), name='groups'),
     # Login Pages
    path('accounts/login', views.LoginPromptView.as_view(), name='login-view'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]