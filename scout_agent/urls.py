from django.urls import path
from .views import LeadScoutView, PDFAnalysisView, analyze_food_image

urlpatterns = [
    path('api/scout/upload/', PDFAnalysisView.as_view(), name='pdf_analysis_upload'),
    path('api/lead/', LeadScoutView.as_view(), name='lead_scout'),
    path('api/food/analyze/', analyze_food_image, name='food_analysis'),
]
