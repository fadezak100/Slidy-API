from .models import User


class UserCommonComponents:

    def create_user(username, email, first_name, last_name, password):
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return user
