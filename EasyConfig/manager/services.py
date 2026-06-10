import os,requests
from .models import Project,Device,Interface

def get_project_name(user):
    try:
        connection = requests.get(os.getenv('GNS3_URL'))
        data = connection.json()
        for i in data:
            Project.objects.update_or_create(
                project_id = i['project_id'],
                defaults={
                    'name': i['name'],
                    'status' : i['status'], 
                    'user' : user
                }
            )
        return True
    except Exception as e:
        print(f'Eroarea : {e}')
        return False


def get_project_devices(project_id):
    try:
        project_obj = Project.objects.get(project_id = project_id)
        base_url = os.getenv('GNS3_URL')
        connection = requests.get(f"{base_url}/{project_id}/nodes")
        data = connection.json()
        ALLOWED_TYPES = ['dynamips', 'vpcs', 'ethernet_switch']
        for i in data:
            if i.get('node_type') not in ALLOWED_TYPES:
                continue
            device_type = 'router' if i['node_type'] == 'dynamips' else i['node_type'] 
            device_obj, created = Device.objects.update_or_create(
                device_id = i["node_id"],
                defaults={
                    'project' : project_obj,
                    'name' : i['name'],
                    'console_port' : i['console'],
                    'device_type' : device_type ,
                    'status' : i['status']
                }
            )
            for j in i['ports']:
                    interface_obj, created = Interface.objects.update_or_create(
                        name = j['name'],
                        device = device_obj,
                        defaults={}
                    )
        print("Sincronizarea a fost realizata cu succes!")
        return True
    except Exception as e:
        print(f"A aparut eroarea: {e}")
        return False