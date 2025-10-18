from repository.favorite_repository import FavoriteRepository
from repository.models import Restaurant
from flask import request
class FavoriteService:
    """Handles business logic related to Favorites."""

    def __init__(self):
        self.favorite_repo = FavoriteRepository()

    def add_favorite(self, user_id, restaurant_id):
        """Add a new favorite for a user."""
        # Check if the restaurant exists
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None, "Restaurant not found"

        # Check if the user has already favorited the restaurant
        existing_favorite = self.favorite_repo.get_favorite_by_user_and_restaurant(user_id, restaurant_id)
        if existing_favorite:
            return None, "Already favorited"

        # Add the new favorite
        new_favorite = self.favorite_repo.add_favorite(user_id, restaurant_id)
        return new_favorite, "Favorite added successfully"

    def delete_favorite(self, user_id, restaurant_id):
        """Delete a favorite for a user."""
        favorite = self.favorite_repo.delete_favorite(user_id, restaurant_id)
        if not favorite:
            return None, "Favorite not found"
        return favorite, "Favorite deleted successfully"

    def get_favorites(self, user_id):
        """Get all favorite restaurants for a user."""
        favorites = self.favorite_repo.get_all_favorites(user_id)
        favorite_restaurants = [
            {
                'id': favorite.restaurant.id,
                'name': favorite.restaurant.name,
                'address': favorite.restaurant.address,
                'phone': favorite.restaurant.phone,
                'image': f"{request.host_url}{favorite.restaurant.image}",
                'created_at': favorite.created_at
            }
            for favorite in favorites
        ]
        return favorite_restaurants

    def check_favorite(self, user_id, restaurant_id):
        """Check if a restaurant is favorited by the user."""
        favorite = self.favorite_repo.get_favorite_by_user_and_restaurant(user_id, restaurant_id)
        return favorite is not None
