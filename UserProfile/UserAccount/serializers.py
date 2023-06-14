from rest_framework import serializers
from .models import *

class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields=fields = ['name','email','bio','file_upload']
