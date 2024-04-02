from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Discussion pages
    path('facilitator/', views.FacilitatorDiscussionView.as_view(), name='facilitator-view'),
    path('facilitator/profile', views.FacilitatorProfileView.as_view(), name='facilitator-profile'),
    path('facilitator/profile/prompts', views.FacilitatorPromptView.as_view(), name='facilitator-prompts'),
    path('facilitator/profile/discussion', views.FacilitatorPromptView.as_view(), name='facilitator-discussions'),
    path('participant/', views.ParticipantDiscussionView.as_view(), name='participant-view'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]