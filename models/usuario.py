from sql_alchemy import banco

class UserModel (banco.Model):
    __tablename__ = 'usuarios'
    
    user_id = banco.Column (banco.Integer, primary_key=True)
    login = banco.Column (banco.String(40))
    senha = banco.Column (banco.String(40))

    