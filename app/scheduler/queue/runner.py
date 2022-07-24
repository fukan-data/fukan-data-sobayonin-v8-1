from scheduler.models import Task

task = Task.objects.filter(name='太郎').first()



