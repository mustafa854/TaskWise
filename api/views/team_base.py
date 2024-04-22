from datetime import date, datetime
import json
import os
import uuid
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializer import TeamSerializerView, TeamSerializerCreateOrUpdate

class TeamView(APIView):
    teams_path = os.path.join(os.getcwd(), "db","teams")
    team_member_dir = os.path.join(os.getcwd(), "db","team_members")
    users_path = os.path.join(os.getcwd(), "db","users")
    
    def get(self, request, format=None):
      global teamsList
      with open(self.teams_path + ".txt") as team:
        teamsList = json.loads(team.read())
      
      print(request.data)
      if request.data.get("id"):
        return self.describe_team(request)
      else:
        return self.list_teams()
      
    def post(self, request):
      if request.data.get("id"):
        return self.add_users_to_team(request)
      return self.create_team(request)
  
    def patch(self, request):
      return self.update_team(request) 

    def delete(self, request):
      return self.remove_users_from_team(request)
  
    # create a team
    def create_team(self, request: str) -> str:
        serializer = TeamSerializerCreateOrUpdate(data=request.data)
        if serializer.is_valid(raise_exception=True):
          newTeam = serializer.validated_data
          newTeam['admin'] = str(newTeam['admin'])
          team_id = uuid.uuid4()
          creation_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
          newTeam['id'] = str(team_id)
          newTeam['creation_time'] = creation_time
          '''
          Checking if user exists or not
          '''
          
          with open(self.users_path + ".txt", "r") as f:
            users_array = json.load(f)
          user_exists = False
          for existingUser in users_array:
            if existingUser['id'] == str(newTeam['admin']):
              user_exists = True
              break
          if user_exists == False:
            return Response({"error":"No User Found. Please select correct user Id for Admin"}, status=400)
          
          with open(self.teams_path + ".txt", "r") as f:
            teamsArray = json.load(f)
          for existingTeam in teamsArray:
            if existingTeam['name'] == newTeam['name']:
              return Response({"name": [
            "Name must be unique."
        ]}, status=400)
          teamsArray.append(newTeam)
          with open(self.teams_path + ".txt", "w") as f:
            json.dump(teamsArray, f)
          # team_member_dir_name = newTeam['id'] + ".txt"
          team_member_dir_name = newTeam['id']
          team_members_dir = os.path.join(self.team_member_dir, team_member_dir_name)
          os.mkdir(team_members_dir)
          team_member_file = open(os.path.join(team_members_dir, newTeam['admin'])+".txt" , "w")
          team_member_file.write("admin")
        return Response({"id":newTeam['id']}, status=201)
                  
    # list all teams
    def list_teams(self) -> str:
        output = []
        for team in teamsList:
          output.append({
            "name" :team["name"],"description":team["description"],"admin":team["admin"],"creation_time":team["creation_time"]
          })
        return Response(output, status=200)

    # describe team
    def describe_team(self, request: str) -> str:
        teamID = request.data.get("id")
        teamFound = False
        
        
        for team in teamsList:
          print(team["id"],teamID )
          if teamID == team["id"]:
            teamFound = True
            output = {
            "name" : team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"],"admin":team["admin"]
          }
            return Response(output, status=200)
          
        if teamFound==False:
          return Response({"error":"No team Found! Please select a correct Team Id"}, status=404)

    # update team
    def update_team(self, request: str) -> str:
      update_team_id = request.data.get("id")
      update_team_name = request.data.get("team").get("name")
      update_team_description = request.data.get("team").get("description")
      update_team_admin = request.data.get("team").get("admin")
      with open(self.teams_path+".txt", "r") as f:
        teams_array = json.load(f)
      team_found = False
      
      with open(self.users_path + ".txt", "r") as f:
          users_array = json.load(f)
          team_exists = False
          for existingUser in users_array:
            if existingUser['id'] == str(update_team_admin):
              team_exists = True
              break
          if team_exists == False:
            return Response({"error":"No Admin Found. Please select correct admin Id for Admin"}, status=400)

      for existingTeam in teams_array:
        if existingTeam['name'] == update_team_name:
          return Response({"error":"Please enter a unique Name. the team with the given name exists."}, status=400)
          
        
        if existingTeam['id'] == update_team_id:
          team_found = True
          existingTeam["name"] =update_team_name
          existingTeam["description"] =update_team_description
      
      if team_found == False:
        return Response({"error":"No team Found! Please select a correct Team Id"}, status=404)
      
      with open(self.teams_path+".txt", "w") as f:
        f.write(json.dumps(teams_array))
      return Response({}, status=200)
    
    def add_users_to_team(self,request: str):
      teamID = request.data.get("id")
      usersArr = request.data.get("users")
      teams_path = os.path.join(os.getcwd(), "db","teams")
      team_members_dir = os.path.join(os.getcwd(), "db","team_members")
      users_path = os.path.join(os.getcwd(), "db","users")
      current_users_count = len(os.listdir(team_members_dir))
      add_users_count = len(usersArr)
      if add_users_count == 0:
        return Response({"error":"Please add atleast 1 user Id to assign to the current team"}, status=400)
      if current_users_count + add_users_count > 50:
        return Response({"error":"Max 50 users can be added!"}, status=400)
      with open(teams_path + ".txt") as team:
            teamsList = json.loads(team.read())
      teamFound = False   
      for team in teamsList:
        if teamID == team["id"]:
          teamFound = True
      if teamFound==False:
        return Response({"error":"No team Found! Please select a correct Team Id"}, status=404)
      
      with open(users_path+".txt", "r") as f:
        users_array = json.load(f)
        for user in usersArr:
          user_found = False
          for existingUser in users_array:
            if user == existingUser['id']:
              user_found = True
              break
          if user_found == False:
            return Response({"error":"Please select correct User Id to add them to a Team!"}, status=400)
      
      for newUser in usersArr:
        open(os.path.join(team_members_dir, teamID ,newUser)+".txt" , "w")
      
      return Response({}, status= 200)

    def remove_users_from_team(self,request: str):
      teamID = request.data.get("id")
      usersArr = request.data.get("users")
      teams_path = os.path.join(os.getcwd(), "db","teams")
      team_members_dir = os.path.join(os.getcwd(), "db","team_members")
      users_path = os.path.join(os.getcwd(), "db","users")
      current_users_count = len(os.listdir(team_members_dir))
      add_users_count = len(usersArr)
      if current_users_count == 1:
        return Response({"error":"There are no Members except Team Leader!"}, status=400)
      if add_users_count == 0:
        return Response({"error":"Please add atleast 1 user Id to remove from the current team"}, status=400)
      
      with open(teams_path + ".txt") as team:
            teamsList = json.loads(team.read())
      teamFound = False   
      
      for team in teamsList:
        if teamID == team["id"]:
          teamFoundData = team
          teamFound = True
          break
      if teamFound==False:
        return Response({"error":"No team Found! Please select a correct Team Id"}, status=404)
      
      with open(users_path+".txt", "r") as f:
        users_array = json.load(f)
        for user in usersArr:
          user_found = False
          for existingUser in users_array:
            if user == teamFoundData['admin']:
              return Response({"error":"Admins / Team Leaders can't be deleted from a Team!"}, status=400)
            if user == existingUser['id']:
              user_found = True
              break
          if user_found == False:
            return Response({"error":"Please select correct User Id to remove them from a Team!"}, status=400)
      
      for newUser in usersArr:
        os.remove(os.path.join(team_members_dir, teamID ,newUser)+".txt")
      
      return Response({}, status= 200)
            




# def list_team_users(self, request: str):
#         """
#         :param request: A json string with the team identifier
#         {
#           "id" : "<team_id>"
#         }

#         :return:
#         [
#           {
#             "id" : "<user_id>",
#             "name" : "<user_name>",
#             "display_name" : "<display name>"
#           }
#         ]
#         """
#         pass

  

class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        pass

    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        pass

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass
    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        pass

