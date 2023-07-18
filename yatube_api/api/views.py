from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from posts.models import Follow, Group, Post

from .permissions import AuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    """Апи работы с постами"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """Апи работы с комментариями"""

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


class GroupViewSet(ReadOnlyModelViewSet):
    """Апи просмотра групп"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    """Апи подписок"""

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.followers

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)
