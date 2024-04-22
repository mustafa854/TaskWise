import os


class StartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("Django server is starting!")
        print("Creating Db and Output Files!")
        out_path = os.path.join(os.getcwd(), "out")
        db_path = os.path.join(os.getcwd(), "db")
        tasks_path = os.path.join(os.getcwd(), "db", "tasks")
        closed_tasks_path = os.path.join(os.getcwd(), "db", "tasks","CLOSED")
        completed_tasks_path = os.path.join(os.getcwd(), "db", "tasks","COMPLETED")
        inprogress_tasks_path = os.path.join(os.getcwd(), "db", "tasks","INPROGRESS")
        open_tasks_path = os.path.join(os.getcwd(), "db", "tasks","OPEN")
        team_members_path = os.path.join(os.getcwd(), "db", "team_members")
        boards_path = os.path.join(os.getcwd(), "db", "boards")+".txt"
        teams_path = os.path.join(os.getcwd(), "db", "teams")+".txt"
        users_path = os.path.join(os.getcwd(), "db", "users")+".txt"
        dir_paths_array = [out_path, db_path, tasks_path, closed_tasks_path, completed_tasks_path,inprogress_tasks_path,open_tasks_path, team_members_path ]
        files_path_arrray = [boards_path, teams_path, users_path]
        
        for dir_path in dir_paths_array:
            if os.path.exists(dir_path) != True:
                os.mkdir(dir_path)
                print(dir_path + " Created!")
        
        for file_path in files_path_arrray:
            if os.path.exists(file_path) != True:
                with open(file_path, "w") as file:
                    file.write("[]")
                print(file_path + " Created!")

        
        print("Db and Output Files creation completed!")

        
        

    def __call__(self, request):
        response = self.get_response(request)
        return response
