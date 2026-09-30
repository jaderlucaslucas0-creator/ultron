from datetime import datetime
class TaskService:
 def __init__(self):self.tasks=[]
 def add(self,name,when):
  item={'name':name,'when':when,'created_at':datetime.now().isoformat(),'status':'scheduled'};self.tasks.append(item);return item
 def list(self):return self.tasks
tasks=TaskService()
