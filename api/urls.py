from django.urls import path
from . import views
from .views import project_board_base, team_base, user_base


urlpatterns = [
    path('users/', user_base.UserView.as_view()),
    path('teams/', team_base.TeamView.as_view()),
    path('teams/add-user', team_base.add_users_to_team),
    path('teams/delete-user', team_base.remove_users_from_team),
    # path('users/team', user_base.UserView.as_view())
]
