from rest_framework import serializers
from .models import Project,Device,Interface


class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = ['device','name', 'ip_address', 'mask', 'gateway' , 'is_configured']
    def validate_ip_address(self,value):
        if(value == '127.0.0.1'):
            raise serializers.ValidationError("Nu se poate folosi aceasta adresa ip!")
        return value

class DeviceSerializer(serializers.ModelSerializer):
    interfaces  = InterfaceSerializer(many = True, read_only = True)
    class Meta:
        model = Device
        fields = ['device_id','project','name','console_port', 'device_type', 'status']


class ProjectSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many = True, read_only = True)

    class Meta:
        model = Project
        fields = ['project_id','name','status','user']

