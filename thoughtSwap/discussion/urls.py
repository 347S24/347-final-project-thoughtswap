from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Discussion pages
    path('facilitator/<int:pk>/<str:group_name>', views.FacilitatorDiscussionView.as_view(), name='facilitator-w-group-view'),
    path('facilitator/<int:pk>', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('<int:pk>/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    path('<int:pk>/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('<int:pk>/prompt', views.create_prompt, name='create-prompt'),
    path('<int:pk>/discussion', views.PastDiscussionView.as_view(), name='facilitator-discussions'),
    path('<int:pk>/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    path('<int:pk>/create-group', views.create_group, name='create-group'),
    path('<int:pk>/<str:name>', views.GroupView.as_view(), name='view-group'),
    path('<int:pk>/<str:name>/<int:code>', views.DiscussionDetailView.as_view(), name='view-responses'),
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    path('participant/swap', views.ParticipantSwapView.as_view(), name='participant-swap-view'),
    # path('participant/swap<int:swapid>', views.ParticipantDiscussionView.as_view(), name='participant-view'),

    # path('profile/groups/', create_group_post, name='facilitator-groups'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]