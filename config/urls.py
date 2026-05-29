from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/professores/',include('professores.urls')),
    path('api/',include('agendamentos.urls')),
    path('api/',include('avaliacoes.urls')),
    path('api/pagamentos/',include('pagamentos.urls')),
    path('api/alunos/', include('alunos.urls')),

]