from django.contrib.auth.backends import ModelBackend
from .models import users

class checkUser(ModelBackend):
    def authenticate(self, request, user_json):
        try:
            user = users.objects.get(id=user_json["userId"])
            return user
        except users.DoesNotExist:
            user = users.objects.create(
                id = user_json["userId"],
                username = user_json["person"]["fullName"],
                email = user_json["contactInformation"]["instituteWebmailAddress"]
            )
            return user
    def get_user(self, user_id: int):
        return super().get_user(user_id)