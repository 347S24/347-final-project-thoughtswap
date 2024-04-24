from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # Channel pages
    # path('chat', views.chat, name='chat'),
    path("room/<str:room_name>/", views.room, name="room"),

    # Discussion pages
    path('create-discussion', views.create_discussion, name='create-discussion'),
    # path('make-discussion', views.create_discussion, name='make-discussion'),
    path('facilitator/<int:pk>/<int:code>', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    # path('facilitator/<int:pk>', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('<int:code>', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    
    # Facilitator profile links
    path('<int:pk>/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    
    # Prompt CRUD/View
    path('<int:pk>/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('<int:pk>/view-prompt/<int:id>', views.PromptDetailView.as_view(), name='prompt-detail'),
    path('<int:pk>/prompt/create', views.create_prompt, name='create-prompt'),
    path('<int:pk>/change-prompt/<int:id>', views.PromptUpdateView.as_view(), name='change-prompt'),
    path('<int:pk>/update-prompt/<int:id>', views.PromptUpdate, name='update-prompt'),
    path('<int:facilitator_pk>/<int:pk>/prompt-delete/', views.PromptDelete.as_view(), name='prompt-delete'),
    path('<int:pk>/save-prompt', views.save_prompt, name='save-prompt'),
    
    # Group CRUD/View
    path('<int:pk>/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    path('<int:pk>/group/create', views.create_group, name='create-group'),
    path('<int:pk>/view-group/<str:name>', views.GroupView.as_view(), name='view-group'),
    path('<int:pk>/change-group/<str:name>', views.GroupUpdateView, name='change-group'),
    # path('<int:pk>/update-group/<str:name>', views.GroupUpdate, name='update-group'),
    path('<int:pk>/update-group/<str:name>', views.GroupUpdate, name='update-group'),
    path('<int:pk>/delete-group/<str:name>', views.GroupDelete.as_view(), name='delete-group'),
    
    # Discussion CRUD/View
    path('<int:pk>/discussion', views.PastDiscussionView.as_view(), name='facilitator-discussions'),
    path('<int:pk>/view-discussion/<str:name>/<int:code>', views.DiscussionDetailView, name='view-responses'),
    
    # Thought CRUD/View
    # path('<int:pk>/<int:code>/delete-thought/<int:id>', views.ThoughtDelete.as_view(), name='delete-thought'),
    path('<int:pk>/<int:code>/delete-thought', views.ThoughtDelete.as_view(), name='delete-thought'),
    
    # Swap CRUD/View
    path('participant/swap', views.ParticipantSwapView.as_view(), name='participant-swap-view'),
    # path('participant/swap<int:swapid>', views.ParticipantDiscussionView.as_view(), name='participant-view'),

    # Login Pages
    path('accounts/login', views.index, name='login-view'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]