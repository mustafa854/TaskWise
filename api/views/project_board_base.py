from datetime import date, datetime
import json
import os
from uuid import uuid4
from rest_framework.views import APIView
from rest_framework.response import Response

from api import serializer
from api.serializer import BoardSerializerCreateOrUpdate, TaskSerializer
class BoardView(APIView):    
    db_path = os.path.join(os.getcwd(), "db")
    teams_path = os.path.join(db_path,"teams")
    team_member_dir = os.path.join(db_path,"team_members")
    users_path = os.path.join(db_path,"users")
    boards_path = os.path.join(db_path,"boards")
    open_board_path = os.path.join(db_path,"open_board")
    open_tasks_path = os.path.join(db_path, "tasks", "OPEN")
    in_progress_tasks_path = os.path.join(db_path, "tasks", "INPROGRESS")
    closed_tasks_path = os.path.join(db_path, "tasks", "CLOSED")
    
    def get(self, request):
      return self.list_boards(request)
    
    def post(self, request):
      if request.data.get("title") and request.data.get("user_id"):
        return self.add_task(request)
      return self.create_board(request)
    
    def patch(self, request):
      return self.close_board(request)
    
    
    def create_board(self, request: str):
      if os.path.isfile(self.open_board_path+".txt"):
        return Response({"error": "There is an already opened board! Close it to create a new one."}, status=400)
      serializer = BoardSerializerCreateOrUpdate(data=request.data)
      if serializer.is_valid(raise_exception=True):
        output = serializer.validated_data
        with open(self.teams_path+".txt", "r") as available_teams:
          json_available_team = json.load(available_teams)
          print(json_available_team)
          team_found = False
          for available_team in json_available_team:
            if available_team['id'] == str(output['team_id']):
              team_found = True
              break
          if team_found == False:
            return Response({"error":"Please select correct team to assign the board!"}, status=400)
              
        with open(self.boards_path + ".txt", "r") as closed_boards:
          json_closed_board = json.load(closed_boards)
          print(json_closed_board)
          for closed_board in json_closed_board:
            if closed_board['name'] == output['name']:
              return Response({"error":"Please enter a unique Name. The team with the given name exists."}, status=400)
          
        open_board = open(self.open_board_path+".txt", "w")
        creation_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
        output['team_id'] = str(output['team_id'])
        output['id'] = str(uuid4())
        output['creation_time'] = creation_time
        open_board.write(json.dumps(output))
      return Response({"id": output['id']})
      
    def close_board(self, request: str) -> str:
      open_tasks_count = len(os.listdir(self.open_tasks_path))
      in_progress_tasks_count = len(os.listdir(self.in_progress_tasks_path))
      if open_tasks_count + in_progress_tasks_count>0:
        return Response({"error": "Tasks are still open, close them to delete the board!"}, status=400)
      if os.path.isfile(self.open_board_path+".txt") != True:
        return Response({"error": "There is no open board! Open a board first to perform this action."}, status=400)
      
      with open(self.open_board_path + ".txt", "r") as open_board:
        current_close_board = json.load(open_board)
        # print(self.boards_path)
      current_close_board['close_time'] = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
      current_close_board['status'] = "CLOSED"
      with open(self.boards_path + ".txt") as closed_boards:
        output = json.loads(closed_boards.read())
      output.append(current_close_board)
      with open(self.boards_path + ".txt", "w") as closed_boards:
        closed_boards.write(json.dumps(output))
        
      os.remove(self.open_board_path + ".txt")
        
      return Response({}, status=201)  
      
    def add_task(self, request: str) -> str:
      if os.path.isfile(self.open_board_path+".txt") != True:
        return Response({"error": "There is no open board! Open a board first to perform this action."}, status=400)
      serializer = TaskSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        task = serializer.validated_data

        with open(self.users_path + ".txt", "r") as f:
          users_array = json.load(f)
          user_exists = False
          for existingUser in users_array:
            if existingUser['id'] == str(task['user_id']):
              user_exists = True
              break
          if user_exists == False:
            return Response({"error":"No User Found! Please select correct user Id to assign task."}, status=400)
                
        open_tasks = os.listdir(self.open_tasks_path)
        closed_tasks = os.listdir(self.closed_tasks_path)
        in_progress_tasks = os.listdir(self.in_progress_tasks_path)
        if len(open_tasks)>0:
          for open_task in open_tasks:
            with open(os.path.join(self.open_tasks_path,open_task), "r") as file:
              temp_json = json.load(file)
              if task['title'] == temp_json['title']:
                return Response({"error":"Task with the same name already exists! Please select a unique name."}, status=400)
        if len(closed_tasks)>0:
          for closed_task in closed_tasks:
            with open(os.path.join(self.closed_tasks_path,closed_task), "r") as file:
              temp_json = json.load(file)
              if task['title'] == temp_json['title']:
                return Response({"error":"Task with the same name already exists! Please select a unique name."}, status=400)
        if len(in_progress_tasks)>0:
          for in_progress_task in in_progress_tasks:
            with open(os.path.join(self.in_progress_tasks_path,in_progress_task), "r") as file:
              temp_json = json.load(file)
              if task['title'] == temp_json['title']:
                return Response({"error":"Task with the same name already exists! Please select a unique name."}, status=400)
        
        creation_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
        id = str(uuid4())
        task['user_id'] = str(task['user_id'])
        task['creation_time'] = creation_time
        task['id'] = id

        with open(os.path.join(self.open_tasks_path,task['id']) +".txt", "w") as file:
          file.write(json.dumps(task))
        
        return Response({"id": task['id']}, status=201)

    def update_task_status(self, request: str):
      pass

    def list_boards(self, request: str) -> str:
      team_id = request.data.get('id')
      with open(self.teams_path+".txt", "r") as file:
        teams = json.load(file)
      team_found = False
      for team in teams:
        if team['id'] == str(team_id):
          team_found = True
          break
      if team_found == False:
        return Response({"error":"No team with the id exists! Please enter correct Team id to list all the boards."}, status=404)
      output = []
      if os.path.isfile(self.open_board_path+".txt"):
        with open(self.open_board_path+".txt", "r") as file:
          open_board = json.load(file)
          temp = {
            "id" : open_board["id"],
            "name" : open_board["name"]
          }
          output.append()
      with open(self.boards_path+".txt", "r") as file:
        closed_boards = json.load(file)
        for board in closed_boards:
          temp = {
            "id" : board["id"],
            "name" : board["name"]
          }
          output.append(temp)
      
      return Response(output, status=200)
      
      

    def export_board(self, request: str) -> str:
      pass


class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        pass

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        pass

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        pass

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        pass

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        pass

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        pass
