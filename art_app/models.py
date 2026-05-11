from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    wallet_address = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Көк чек (верификация) үчүн
    rank = models.PositiveIntegerField(null=True, blank=True)  # #2 деген рейтинг үчүн
    total_volume = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)  # 2.25 ETH үчүн
    RoleChoices = (
        ('buyer', 'buyer'),
        ('seller', 'seller'))
    role = models.CharField(max_length=20, choices=RoleChoices, default='buyer')
    facebook_link = models.URLField(max_length=300, null=True, blank=True)
    twitter_link = models.URLField(max_length=300, null=True, blank=True)
    instagram_link = models.URLField(max_length=300, null=True, blank=True)
    linkedin_link = models.URLField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.category_name


class Collection(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    collection_name = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to='collection_banners/')
    logo = models.ImageField(upload_to='collection_logos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.collection_name




class NFTArt(models.Model):
    STATUS_CHOICES = (('sale', 'sale'), ('auction', 'auction'), ('sold', 'sold'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nfts')
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name='nfts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='nfts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='nfts/')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    views = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sale')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    nft = models.ForeignKey(NFTArt, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    nft = models.ForeignKey(NFTArt, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'nft')

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    nft = models.ForeignKey(NFTArt, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return self.follower.username


class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    nft = models.ForeignKey(NFTArt, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_hash = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buyer.username