from flask_restx import Namespace, Ressource, fields

api = namespace('auth',description='Authentication operations' )

login_model = api.model('Login' , {
    'email': fields.string(requier=True, description='user email'),
    'password': fields.string(required=True, description='User passeword')
})
