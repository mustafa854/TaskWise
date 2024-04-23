from django.urls import path
from .views import project_board_base, team_base, user_base

urlpatterns = [
    path('users/', user_base.UserView.as_view()),
    path('users/teams', user_base.get_user_teams),
    path('teams/', team_base.TeamView.as_view()),
    path('teams/users', team_base.list_team_users),
    path('boards/', project_board_base.BoardView.as_view()),
  
]
