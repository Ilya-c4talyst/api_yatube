from posts.models import Comment, Group, Post
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_list(self, serializer):
        if self.request.user.is_authenticated:
            return super().list(serializer)
        else:
            return Response(
                "Ошибка авторизации.",
                status=status.HTTP_401_UNAUTHORIZED
            )

    def update(self, request, *args, **kwargs):  # Как реализовать это верно?
        post = self.get_object()                 # Через perform/serializer
        if self.request.user == post.author:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Недостаточно прав для редактирования."},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user == post.author:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Недостаточно прав для удаления."},
                status=status.HTTP_403_FORBIDDEN
            )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.author:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Недостаточно прав для редактирования."},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.author_id:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Недостаточно прав для удаления."},
                status=status.HTTP_403_FORBIDDEN
            )
