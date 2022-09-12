from rest_framework import serializers

from django.contrib.auth.models import (
    User,
    Group,
)
from api.models import (
    app_settings,
    UserProfile,
    UserProfileFiles,
)


class GroupsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        read_only_fields = ('id',)
        fields = ['id', 'name']#"__all__"



class UsersProfileFilesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfileFiles
        read_only_fields = ('id',)
        fields = ['id', 'user_files']#"__all__"



class UsersProfileSerializer(serializers.HyperlinkedModelSerializer):
    #ser_files = UsersProfileFilesSerializer(many=True)

    class Meta:
        model = UserProfile
        read_only_fields = ('id',)
        fields = ["id", "first_name", "middle_name", "last_name"]#"__all__"



class UsersSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupsSerializer(many=True)

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = ['id', 'username', 'email', 'is_staff', 'groups']#"__all__"
