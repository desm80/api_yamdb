from rest_framework import serializers


from reviews.models import Comment, Category, Genre, Title, Review

# переопределить поля, валидатор добавить


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        field = "__all__"
        model = Review

# переопредилить поля?


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        field = "__all__"
        model = Comment
