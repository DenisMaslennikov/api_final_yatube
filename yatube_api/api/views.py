from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from posts.models import Follow, Group, Post

from .exceptions import FollowError
from .permissions import AuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments

    def perform_create(self, serializer: CommentSerializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(
            author=self.request.user,
            post=post,
        )


class GroupViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user.pk)

    def perform_create(self, serializer: FollowSerializer):
        following = serializer.validated_data.get("following")
        if following == self.request.user:
            raise FollowError("Нельзя подписаться на самого себя")
        if Follow.objects.filter(
            user=self.request.user, following=following
        ):
            raise FollowError("Такая подписка уже есть")
        serializer.save(user=self.request.user)
