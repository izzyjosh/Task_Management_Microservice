import grpc
import task_pb2
import task_pb2_grpc

class TaskConsumer:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = task_pb2_grpc.TaskServiceStub(self.channel)

    def create_task(self, title: str, description: str):

        request = task_pb2.TaskCreateRequest(title=title, description=description)

        response = self.stub.CreateTask(request)
        return response

    def get_task(self, id: int):
        request = task_pb2.TaskGetRequest(id=id)

        response2 = self.stub.GetTask(request)
        return response2

task_consumer = TaskConsumer()


# create task
response = task_consumer.create_task("task2", "second task")
print(response)

print("Get Task")

response2 = task_consumer.get_task(20)
print(response2)

