from rest_framework import serializers

from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.pk')
    author_first_name = serializers.ReadOnlyField(source='author.first_name')
    author_last_name = serializers.ReadOnlyField(source='author.last_name')
    author_image = serializers.CharField(source='author.image', read_only=True)

    class Meta:
        model = Comment
        fields = [
            "pk", "text", "author_id", "created_at", "author_first_name", "author_last_name", "ad_id", "author_image"
        ]


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['pk', 'image', 'title', 'price', 'description']


class AdDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.pk')
    author_first_name = serializers.ReadOnlyField(source='author.first_name')
    author_last_name = serializers.ReadOnlyField(source='author.last_name')
    phone = serializers.CharField(source='author.phone', read_only=True)

    class Meta:
        model = Ad
        fields = [
            'pk', 'image', 'title', 'price', 'description',
            'author_first_name', 'author_last_name', 'author_id'
        ]
