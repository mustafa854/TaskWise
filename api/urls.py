from django.urls import path
from . import views
from .views import project_board_base, team_base, user_base


urlpatterns = [
    path('users/', user_base.UserView.as_view()),
    path('teams/', team_base.TeamView.as_view()),
    
    # path('users/team', user_base.UserView.as_view())
]
