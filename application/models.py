from flask_login import UserMixin


class User(UserMixin):
     def __init__(self, user_id, usuario, password, nivel):
          self.id = user_id
          self.usuario = usuario
          self.password = password
          self.nivel = nivel
          self.authenticated = False
     def is_active(self):
          return self.is_active()
     def is_anonymous(self):
          return False
     def is_authenticated(self):
          return self.authenticated
     def is_active(self):
          return True
     def get_id(self):
          return self.id
     def get_nivel(self):
          return self.nivel