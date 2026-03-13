from flask_restx import Namespace, Resource, fields

api = Namespace('auth',description='Authentication operations' )

login_model = api.model('Login' , {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='User passeword')
})
