from datetime import date, datetime
import json
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializer import UserSerializer

class UserView(APIView):
  users_path = os.path.join(os.getcwd(), "db","users")
  
  def checkDbFiles(self):
    pass
  
  def get(self, request, format=None):
    global usersList
    with open(self.users_path + ".txt") as user:
      usersList = json.loads(user.read())
    
    if request.data.get("id"):
      return self.describe_user(request)
    else:
      return self.list_users()
    
  def post(self, request):
    return self.create_user(request)
  
  def patch(self, request):
    return self.update_user(request) 
  
  def create_user(self, request: str) -> str:
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      newUser = serializer.validated_data
      user_id = uuid.uuid4()
      creation_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
      newUser['id'] = str(user_id)
      newUser['creation_time'] = creation_time
      
      with open(self.users_path + ".txt", "r") as f:
        users_array = json.load(f)
      for existingUser in users_array:
        if existingUser['name'] == newUser['name']:
          return Response({"name": [
        "Name must be unique."
    ]}, status=400)
      users_array.append(newUser)
      with open(self.users_path + ".txt", "w") as f:
        json.dump(users_array, f)
    return Response({"id":newUser['id']}, status=201)
  
  def list_users(self) -> str:
    output = []
    for user in usersList:
      output.append({
        "name" :user["name"],"display_name":user["display_name"],"creation_time":user["creation_time"]
      })
    return Response(output, status=200)
  
  def describe_user(self, request: str) -> str:
    userID = request.data.get("id")
    for user in usersList:
      if userID in user["id"]:
        output = {
        "name" :user["name"],
        "display_name":user["display_name"],
        "creation_time":user["creation_time"]
      }
        return Response(output, status=200)
    else:
      return Response({"error":"No User Found"}, status=400)
    
  def update_user(self, request: str) -> str:
    update_user_id = request.data.get("id")
    update_user_name = request.data.get("user").get("name")
    update_user_display_name = request.data.get("user").get("display_name")
    with open(self.users_path+".txt", "r") as f:
      users_array = json.load(f)
    user_found = False
    for existingUser in users_array:
      if existingUser['id'] == update_user_id:
        user_found = True
        existingUser["name"] =update_user_name
        existingUser["display_name"] =update_user_display_name
    
    if user_found == False:
      return Response({"error":"No User Found"}, status=400)
    
    with open(self.users_path+".txt", "w") as f:
      f.write(json.dumps(users_array))
    return Response({}, status=200)
    

  # def get_user_teams(self, request: str) -> str:
  #   pass

class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        pass

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        pass

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        pass

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

