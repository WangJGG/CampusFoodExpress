from repository.models import Favorite, Restaurant, db

class FavoriteRepository:
    """Handles database operations related to Favorite."""

    @staticmethod
    def get_favorite_by_user_and_restaurant(user_id, restaurant_id):
        """Check if the user has favorited the restaurant."""
        return Favorite.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()

    @staticmethod
    def add_favorite(user_id, restaurant_id):
        """Add a new favorite."""
        new_favorite = Favorite(user_id=user_id, restaurant_id=restaurant_id)
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite

    @staticmethod
    def delete_favorite(user_id, restaurant_id):
        """Delete a favorite."""
        favorite = Favorite.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
        return favorite

    @staticmethod
    def get_all_favorites(user_id):
        """Get all favorites for a user."""
        return Favorite.query.filter_by(user_id=user_id).all()
