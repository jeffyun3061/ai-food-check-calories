from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scout_agent.urls')),  # ✅ ''로 해줘야 함!!! (api/ 아님)
]
