from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # Discussion pages
    # path('facilitator/', views.FacilitatorListView.as_view(), name='facilitators'),
    # path('facilitator/<int:pk>', views.FacilitatorDetailView.as_view(), name='facilitator-detail'),
    # path('<int:pk>', views.DiscussionDetailView.as_view(), name='discussion-detail'),
]