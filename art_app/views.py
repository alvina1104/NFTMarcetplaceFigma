from .serializer import (UserListSerializer, UserDetailSerializer,
    UserRegisterSerializer, UserLoginSerializer,
    CategoryListSerializer, CategoryDetailSerializer,
    CollectionListSerializer,
    NFTArtListSerializer, NFTArtDetailSerializer,
    BidCreateSerializer, BidListSerializer,
    FavoriteSerializer, CommentSerializer,
    FollowSerializer,
    TransactionListSerializer, TransactionDetailSerializer)
from .models import (User, Category, Collection, NFTArt, Bid,
                      Favorite, Comment, Follow, Transaction)
from rest_framework import viewsets, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .permissions import (IsBuyer, IsAuthenticatedReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.select_related('owner').all()
    serializer_class = CollectionListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class NFTArtListAPIView(generics.ListAPIView):
    queryset = NFTArt.objects.select_related('owner','category').all()
    serializer_class = NFTArtListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class NFTDetailAPIView(generics.RetrieveAPIView):
    queryset = NFTArt.objects.select_related('owner', 'category').all()
    serializer_class = NFTArtDetailSerializer
    permission_classes = [IsAuthenticatedReadOnly]


class BidListView(generics.ListAPIView):
    queryset = Bid.objects.select_related('user','nft').all()
    serializer_class = BidListSerializer


class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    permission_classes = [IsBuyer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.select_related('user','nft').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user','nft').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.select_related('follower','following').filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)



class TransactionViewSet(viewsets.ModelViewSet):

    serializer_class = TransactionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.select_related('buyer','seller','nft').filter(
            Q(buyer=self.request.user) |
            Q(seller=self.request.user))

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TransactionDetailSerializer

        return TransactionListSerializer