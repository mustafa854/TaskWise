from datetime import date, datetime
import json
import os
import shutil
from uuid import uuid4
from rest_framework.views import APIView
from rest_framework.response import Response

from api import serializer
from api.serializer import BoardSerializerCreateOrUpdate, TaskSerializer, TaskUpdateSerializer
class BoardView(APIView):    
    db_path = os.path.join(os.getcwd(), "db")
    out_directory = os.path.join(os.getcwd(), "out")
    teams_path = os.path.join(db_path,"teams")
    team_member_dir = os.path.join(db_path,"team_members")
    users_path = os.path.join(db_path,"users")
    boards_path = os.path.join(db_path,"boards")
    open_board_path = os.path.join(db_path,"open_board")
    open_tasks_path = os.path.join(db_path, "tasks", "OPEN")
    in_progress_tasks_path = os.path.join(db_path, "tasks", "INPROGRESS")
    closed_tasks_path = os.path.join(db_path, "tasks", "CLOSED")
    tasks_path = os.path.join(db_path, "tasks")
    
    def get(self, request):
      return self.list_boards(request)
    
    def post(self, request):
      if request.data.get("id"):
        return self.export_board(request)
      if request.data.get("title") and request.data.get("user_id"):
        return self.add_task(request)
      return self.create_board(request)
    
    def patch(self, request):
      if request.data.get("id"):
        if request.data.get("status"):
          return self.update_task_status(request)
        return self.close_board(request)
      else:
        return Response({"error": "Please enter a Board ID to close the board, or enter Task ID with status to update Task Status."}, status=400)  
    
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
              return Response({"error":"Please enter a unique Name. The Board with the given name exists."}, status=400)
          
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
      if current_close_board['id'] != str(request.data.get('id')):
        return Response({"error": "Please enter the correct board id to close the board! "}, 404)
      current_close_board['close_time'] = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
      current_close_board['status'] = "CLOSED"
      with open(self.boards_path + ".txt") as closed_boards:
        output = json.loads(closed_boards.read())
      output.append(current_close_board)
      with open(self.boards_path + ".txt", "w") as closed_boards:
        closed_boards.write(json.dumps(output))
      
      closed_tasks = os.listdir(self.closed_tasks_path)
      os.mkdir(os.path.join(os.path.join(os.getcwd(), "db"), "tasks", "COMPLETED",current_close_board['id'] ))
      if len(closed_tasks)>0:
        for task in closed_tasks:
          src = os.path.join(os.getcwd(), "db", "tasks", "CLOSED",task )
          print(src)
          dest = os.path.join(os.getcwd(), "db", "tasks", "COMPLETED", current_close_board['id'],task )
          print(dest)
          shutil.move(src,dest)
          
        
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
        serializer = TaskUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          task = serializer.validated_data
          task['id'] = str(task['id'] )
          if task['status'] == "IN_PROGRESS":
            task['status'] = "INPROGRESS"
        open_tasks = os.listdir(self.open_tasks_path)
        closed_tasks = os.listdir(self.closed_tasks_path)
        in_progress_tasks = os.listdir(self.in_progress_tasks_path)
        task_found = False
        task_details = {}
        
        if len(open_tasks)>0:
          for open_task in open_tasks:
            with open(os.path.join(self.open_tasks_path,open_task), "r") as file:
              temp_json = json.load(file)
              if task['id'] == temp_json['id']:
                task_found = True
                task_details = temp_json
                old_task_status = "OPEN"
                break
        if len(closed_tasks)>0 and task_found!=True:
          for closed_task in closed_tasks:
            with open(os.path.join(self.closed_tasks_path,closed_task), "r") as file:
              temp_json = json.load(file)
              if task['id'] == temp_json['id']:
                task_found = True
                task_details = temp_json
                old_task_status = "CLOSED"
                break
        if len(in_progress_tasks)>0  and task_found!=True:
          for in_progress_task in in_progress_tasks:
            with open(os.path.join(self.in_progress_tasks_path,in_progress_task), "r") as file:
              temp_json = json.load(file)
              if task['id'] == temp_json['id']:
                task_found = True
                task_details = temp_json
                old_task_status = "INPROGRESS"
                break
        if task_found == False:
          return Response({"error":"Enter correct Task Id to update the status!"}, status=404)
        
        if old_task_status == task['status']:
          return Response({"error":"The task is of the same status, choose another choice to change the staus of the task."}, status=400)
        
        with open(os.path.join(self.tasks_path, task['status'], task_details['id'])+".txt", "w") as new_task:
          new_task.write(json.dumps(task_details))
        
        os.remove(os.path.join(self.tasks_path, old_task_status, task['id'])+".txt")
        
        return Response({}, status=201)

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
          open_board = json.load(file.read())
          temp = {
            "id" : open_board["id"],
            "name" : open_board["name"]
          }
          output.append()
      with open(self.boards_path+".txt", "r") as file:
        closed_boards = json.load(file.read())
        for board in closed_boards:
          temp = {
            "id" : board["id"],
            "name" : board["name"]
          }
          output.append(temp)
      
      return Response(output, status=200)
      
      

    def export_board(self, request: str) -> str:
      # check board id in open and closed/boards.txt, if not found then return error
      board_id = str(request.data.get('id'))
      board_found = False
      output = {}
      board_status = "?"
      if os.path.isfile(self.open_board_path+".txt") == True:
        with open(self.open_board_path + ".txt", "r") as file:
           open_board = json.loads(file.read())
           if open_board['id'] == board_id:
             board_found =True
             board_status = "OPEN"
             output['board_id'] = open_board['id']
             output['board_name'] = open_board['name']
             output['team_id'] = open_board['team_id']
             with open(self.teams_path+".txt", "r") as file:
               data = json.load(file)
               for d in data:
                 if d["id"] == output['team_id']:
                   output['team_name'] = d['name']
                   break
             
             output['creation_time'] = open_board['creation_time']
             
        
      if board_status == "OPEN":
        open_tasks = []
        open_tasks_dir = os.listdir(self.open_tasks_path)
        for task in open_tasks_dir:
          with open(os.path.join(self.tasks_path,"OPEN", task), "r") as File:
            open_tasks.append(json.load(File))
        closed_tasks = []
        closed_taks_dir = os.listdir(self.closed_tasks_path)
        for task in closed_taks_dir:
          with open(os.path.join(self.tasks_path,"CLOSED", task), "r") as File:
            closed_tasks.append(json.load(File))
        in_progress_tasks = []
        in_progress_tasks_dir = os.listdir(self.in_progress_tasks_path)
        for task in in_progress_tasks_dir:
          with open(os.path.join(self.tasks_path,"INPROGRESS", task), "r") as File:
            in_progress_tasks.append(json.load(File))  
        
        current_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)+":"+str(datetime.now().microsecond)
        filename = "".join( x for x in "OPEN_"+current_time if (x.isalnum() or x in "._- "))
        with open(self.out_directory + "\\"+filename+".txt", "w") as file:
          output_file = ""
          for x in output.keys():
            output_file += '\n|------------------|------------------------------------------------------------------|'
            output_file += '\n| '+x + (16-len(x))*' '+ " |"+" "+ output.get(x) +(64-len(output.get(x)))*" " +" |"
          
          output_file += '\n|------------------|------------------------------------------------------------------|'
          output_file +='\n\n\nStatus: Open'
          for i, ele in enumerate(open_tasks):
            output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            output_file += '\n| #'+str(i+1)+"  | " + ele['title']+(89-len(output.get(x)))*" " +" |"
            output_file += '\n|Start'+"| " + ele['creation_time']+(77-len(ele['creation_time']))*" " +" |"
          output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
          
          output_file +='\n\n\nStatus: In Progress'
          for j, ele in enumerate(in_progress_tasks):
            output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            output_file += '\n| #'+str(j+1)+"  | " + ele['title']+(89-len(output.get(x)))*" " +" |"
            output_file += '\n|Start'+"| " +  ele['creation_time']+(77-len(ele['creation_time']))*" " +" |"
          output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
          
          output_file +='\n\n\nStatus: Closed'
          for k, ele in enumerate(closed_tasks):
            output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            output_file += '\n| #'+str(k+1)+"  | " + ele['title']+(89-len(output.get(x)))*" " +" |"
            output_file += '\n|Start'+"| " +  ele['creation_time']+(77-len(ele['creation_time']))*" " +" |"
          output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            
         
          
          file.write(output_file)
          
        return Response({"message":"Check Output Folder"}, status=201)
        
      if board_found == False:
         with open(self.boards_path + ".txt", "r") as file:
           closed_boards = json.loads(file.read())
           for board in closed_boards:
            if board['id'] == board_id:
              board_found = True
              board_status = "CLOSED"
              output['board_id'] = board['id']
              output['board_name'] = board['name']
              output['team_id'] = board['team_id']
              output['creation_time'] = board['creation_time']
              output['close_time'] = board['close_time']
              with open(self.teams_path+".txt", "r") as file:
                data = json.load(file)
                for d in data:
                  if d["id"] == output['team_id']:
                    output['team_name'] = d['name']
                    break
      if board_status == "CLOSED":
        completed_tasks = []
        completed_tasks_dir = os.listdir(os.path.join(os.getcwd(),"db", "tasks", "COMPLETED", output['board_id']))
        if len(completed_tasks_dir)>0:
          for task in completed_tasks_dir:
            with open(os.path.join(self.tasks_path,"COMPLETED", output['board_id'], task), "r") as File:
              completed_tasks.append(json.loads(File.read()))
        current_time = str(date.today()) +" " +str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)+":"+str(datetime.now().microsecond)
        filename = "".join( x for x in "CLOSED_"+current_time if (x.isalnum() or x in "._- "))
        with open(self.out_directory + "\\"+filename+".txt", "w") as file:
          output_file = ""
          for x in output.keys():
            output_file += '\n|------------------|------------------------------------------------------------------|'
            output_file += '\n| '+x + (16-len(x))*' '+ " |"+" "+ output.get(x) +(64-len(output.get(x)))*" " +" |"
          
          output_file += '\n|------------------|------------------------------------------------------------------|'
          
          output_file +='\n\n\nStatus: Closed'
          for k, ele in enumerate(completed_tasks):
            output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            output_file += '\n| #'+str(k+1)+"  | " + ele['title']+(89-len(output.get(x)))*" " +" |"
            output_file += '\n|Start'+"| " +  ele['creation_time']+(77-len(ele['creation_time']))*" " +" |"
          output_file += '\n|@@@@@|@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|'
            
          file.write(output_file)
          
        return Response({"message":"Check Output Folder"}, status=201)
                    
      if board_found == False:
        return Response({"error":"Select correct board ID to export the board"}, status=404)       
      

