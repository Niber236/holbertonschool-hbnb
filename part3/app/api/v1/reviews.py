from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or business rule violation')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        place_id = review_data.get('place_id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        existing_reviews = facade.get_reviews_by_place(place_id)
        if existing_reviews:
            for r in existing_reviews:
                if r.user.id == current_user_id:
                    return {'error': 'You have already reviewed this place'}, 400

        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating
        } for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        # VÉRIFICATION : C'est TON commentaire OU tu es le patron ?
        if review.user.id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        # VÉRIFICATION : C'est TON commentaire OU tu es le patron ?
        if review.user.id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200