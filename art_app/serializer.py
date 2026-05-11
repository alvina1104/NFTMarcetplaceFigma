from .models import (User, Category, Collection, NFTArt, Bid, Favorite,
                    Comment, Follow, Transaction)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserListSerializer(serializers.ModelSerializer):
    eth_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'avatar', 'rank',
            'is_verified', 'total_volume', 'eth_amount'
        ]

    def get_eth_amount(self, obj):
        return f"{obj.total_volume} ETH"

class UserDetailSerializer(serializers.ModelSerializer):
    collections_count = serializers.SerializerMethodField()
    nfts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_collections_count(self, obj):
        return obj.collections.count()

    def get_nfts_count(self, obj):
        return obj.nfts.count()


class UserArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'image']



class NFTArtListSerializer(serializers.ModelSerializer):
    owner = UserArtSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = NFTArt
        fields = [
            'id', 'title', 'image', 'price',
            'status', 'likes_count', 'views',
            'owner', 'category'
        ]


class BidListSerializer(serializers.ModelSerializer):
    owner = UserListSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ['owner', 'amount', 'created_at']


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['nft', 'amount', 'created_at']
        read_only_fields = ['created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The value must be greater than zero.!")
        return value


class NFTArtDetailSerializer(serializers.ModelSerializer):
    owner = UserArtSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    bids = BidListSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = NFTArt
        fields = ['id', 'title', 'owner', 'collection', 'category',
            'bids', 'comments', 'is_favorited', 'price',
            'image', 'status']

    def get_comments(self, obj):
        return []

    def get_is_favorited(self, obj):
        return False

    def get_status(self, obj):
        return obj.status


class CollectionListSerializer(serializers.ModelSerializer):
    nfts = NFTArtListSerializer(read_only=True, many=True)
    owner = UserArtSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id', 'collection_name', 'banner',
            'logo', 'owner', 'nfts']




class CategoryDetailSerializer(serializers.ModelSerializer):
    nfts = NFTArtListSerializer(read_only=True, many=True)
    nfts_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'nfts_count', 'nfts']

    def get_nfts_count(self, obj):
        return obj.nfts.count()



class CollectionDetailSerializer(serializers.ModelSerializer):
    owner = UserArtSerializer(read_only=True)
    nfts = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'

    def get_nfts(self, obj):
        return NFTArtListSerializer(obj.nfts.all(), many=True).data




class FavoriteSerializer(serializers.ModelSerializer):
    nft = NFTArtListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserArtSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = UserArtSerializer(read_only=True)
    following = UserArtSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'

class TransactionListSerializer(serializers.ModelSerializer):
    buyer = UserArtSerializer(read_only=True)
    seller = UserArtSerializer(read_only=True)
    nft = NFTArtListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'buyer', 'seller',
            'nft', 'amount',
            'transaction_hash', 'created_at'
        ]

class TransactionDetailSerializer(serializers.ModelSerializer):
    buyer = UserArtSerializer(read_only=True)
    seller = UserArtSerializer(read_only=True)
    nft = NFTArtListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'