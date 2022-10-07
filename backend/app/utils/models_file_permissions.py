def CreatePathFor_upload_users_username_files(instance, filename):
    file_path = instance.user_files.path.replace(filename, '') + '\\users\\' + instance.user_profile.user.username + '\\files\\' + filename
    return file_path

def CreatePathFor_upload_users_username_avatars(instance, filename):
    file_path = instance.profile_avatar.path.replace(filename, '') + '\\users\\' + instance.user.username + '\\avatars\\' + filename
    return file_path
