import datetime


class User:

    def __init__(self, name, email, hash_password):
        self.name = ""
        self.email = ""
        self.hash_password = ""
        self.created_date = None
        self.profile_image_url = ""
        self.last_login: datetime.datetime = None
