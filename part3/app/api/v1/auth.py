from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth',description='Authentication operations' )

login_model = api.model('Login' , {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='User passeword')
})
@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True )

    def post(self):
        login_data = api.payload
        email = login_data.get('email')
        password = login_data.get('password')
        user = facade.get_user_by_email(email)
        
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # MODIFIE CETTE LIGNE ICI :
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={'is_admin': user.is_admin}
        )
        
        return {'access_token': access_token}, 200
     
        