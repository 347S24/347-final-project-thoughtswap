from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Discussion pages
    path('facilitator/', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('facilitator/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    path('profile/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('profile/discussion', views.PastDiscussionView.as_view(), name='facilitator-discussions'),
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    path('profile/groups/', views.FacilitatorGroupView.as_view(), name='facilitator-groups'),
    path('groups/', views.ParticipantGroupView.as_view(), name='groups'),
     # Login Pages
    path('accounts/login', views.LoginPromptView.as_view(), name='login-view'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]