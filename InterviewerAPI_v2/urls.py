from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import InterviewViewSet, AnswerViewSet
from .settings import STATIC_ROOT, STATIC_URL


router = DefaultRouter()
router.register('interview', InterviewViewSet, 'interview')
router.register('answer', AnswerViewSet, 'answer')

urlpatterns = [
    *router.urls,
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(STATIC_URL, document_root=STATIC_ROOT)
