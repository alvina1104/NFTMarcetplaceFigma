from django.urls import path, include
from .views import (
    UserListView, UserDetailView,CategoryListView,CategoryDetailAPIView,
    CollectionViewSet, NFTArtListAPIView,NFTDetailAPIView,
    BidCreateView,BidListView,
    FavoriteViewSet,CommentViewSet,TransactionViewSet,FollowViewSet,
    RegisterView, LoginView, LogoutView)
from rest_framework import routers

router = routers.SimpleRouter()
router.register('collections', CollectionViewSet)
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('comments', CommentViewSet)
router.register('follows', FollowViewSet, basename='follow')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('bids/', BidListView.as_view(), name='bids-list'),
    path('bids/create/', BidCreateView.as_view(), name='bid-create'),
    path('nft_arts/', NFTArtListAPIView.as_view(), name='nft-list'),
    path('nft_arts/<int:pk>/', NFTDetailAPIView.as_view(), name='nft-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
