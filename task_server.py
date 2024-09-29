import grpc
import task_pb2
import task_pb2_grpc

from concurrent import futures

from pydantic import BaseModel

class GetUser(BaseModel):
    id: int

class TaskServicer(task_pb2_grpc.TaskService):
    def __init__(self):
        self.db = [
                {"id": 1, "title":"task1", "description":"furst_task", "status":"assigned"},
                ]

    def CreateTask(self, request, context):
        title = request.title
        description = request.description
        last_id = self.db[-1]["id"]

        self.db.append({"id": last_id + 1, "title": title, "description": description, "status": "assigned"})
        
        return task_pb2.TaskCreateResponse(**self.db[-1])

    def GetTask(self, request: GetUser, context):
        id = request.id

        for task in self.db:
            if task["id"] == id:
                response_task = task
                return task_pb2.TaskCreateResponse(**response_task)
        return task_pb2.TaskErrorResponse(type="Not Found", detail="Task not Found")


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskServiceServicer_to_server(TaskServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
