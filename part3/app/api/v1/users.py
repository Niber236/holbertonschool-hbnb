from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# On rajoute les champs optionnels pour que l'admin puisse les modifier via Swagger
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user (Admin only)'),
    'password': fields.String(description='Password of the user (Admin only)')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        all_users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in all_users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Le videur vérifie : c'est TON profil OU tu es le patron ?
        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        
        # Si le mec n'est PAS admin, on détruit ses tentatives de changer email/mot de passe
        if not is_admin:
            user_data.pop('email', None)
            user_data.pop('password', None)
        else:
            # Si c'est l'admin, on vérifie que le nouvel email n'est pas déjà pris par un autre
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already registered'}, 400
        
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
            
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200