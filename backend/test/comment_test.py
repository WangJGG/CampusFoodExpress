from datetime import datetime, timezone
from repository.models import Comment,db  # 假设这些是你的模型类
from app import create_app
app = create_app()


# 插入评论数据
comments = [
    Comment(
        id=5,
        user_id=1,
        restaurant_id=1,
        text='Amazing food! Loved the steak and wine pairing.',
        rating=5,
        created_at=datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
        images="images/steak.jpg;images/wine.jpg"
    ),
    Comment(
        id=6,
        user_id=2,
        restaurant_id=2,
        text='Sushi was fresh and delicious. Will visit again!',
        rating=4,
        created_at=datetime(2024, 1, 20, 14, 30, 0, tzinfo=timezone.utc),
        images="images/sushi.jpg"
    ),
    Comment(
        id=7,
        user_id=3,
        restaurant_id=3,
        text='The hotpot broth was a bit too spicy for me, but overall a good experience.',
        rating=3,
        created_at=datetime(2024, 1, 25, 19, 45, 0, tzinfo=timezone.utc),
        images=None
    ),
    Comment(
        id=8,
        user_id=2,
        restaurant_id=3,
        text='Great selection of dipping sauces and fresh ingredients!',
        rating=5,
        created_at=datetime(2024, 1, 30, 18, 15, 0, tzinfo=timezone.utc),
        images="images/sauce.jpg;images/ingredients.jpg"
    ),
]

with app.app_context():
    db.session.add_all(comments)

    # 提交数据到数据库
    try:
        db.session.commit()
        print("Test data inserted successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
