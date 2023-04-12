from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from .permissions import CheckAuth
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (CheckAuth, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Удаление чужого контента запрещено!')
    #     instance.delete()
    #  Попробовал permissions,
    #  но интересно, правильно ли у меня реализованы обычные методы?


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CheckAuth, permissions.IsAuthenticated)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    # def perform_update(self, serializer):
    #     if self.request.user != serializer.instance.author:
    #         raise PermissionDenied("Изменение чужих комментариев запрещено.")
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Удаление чужого комментария запрещено!')
    #     instance.delete()
