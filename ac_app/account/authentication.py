from django.contrib.auth import get_user_model

Profile = get_user_model()


class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = Profile.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except Profile.DoesNotExist:
            try:
                user = Profile.objects.get(username=username)
                if user.check_password(password):
                    return user
            except Profile.DoesNotExist:
                return None
        except Profile.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
