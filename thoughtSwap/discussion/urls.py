from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Discussion pages
    path('facilitator/', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('<int:pk>/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    path('<int:pk>/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('<int:pk>/discussion', views.PastDiscussionView.as_view(), name='facilitator-discussions'),
    path('<int:pk>/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    # path('<int:pk>/groups/create', views.create_group, name='create-group'),
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),

    # path('profile/groups/', create_group_post, name='facilitator-groups'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]