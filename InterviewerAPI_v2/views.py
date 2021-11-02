from rest_framework import viewsets, permissions
from rest_framework.views import Response, status

from .serializers import InterviewSerializer, AnswerSerializer
from .models import Interview, Answer

from .permissions import IsAdminOrReadOnly


class InterviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = AnswerSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super(AnswerViewSet, self).get_serializer_context()
        if self.request.GET.get('interview'):
            context.update({'interview': self.request.GET.get('interview')})
        context.update({'user': self.request.user})
        return context

    def get_queryset(self):
        if self.request.GET.get('interview', None):
            return self.queryset.filter(user=self.request.user, interview_id=self.request.GET.get('interview'))
        return self.queryset.filter(user=self.request.user)
