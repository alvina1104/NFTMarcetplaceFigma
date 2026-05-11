from django.contrib import admin
from .models import (User, Category,Collection, NFTArt, Bid, Favorite, Comment, Follow, Transaction)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(NFTArt)
admin.site.register(Bid)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Transaction)
