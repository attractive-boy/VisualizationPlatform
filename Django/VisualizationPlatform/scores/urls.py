from django.urls import path
from .views import create_score, update_score, delete_score,get_scores

urlpatterns = [
    path('create/', create_score, name='create_score'),
    path('update/<int:score_id>/', update_score, name='update_score'),
    path('delete/<int:score_id>/', delete_score, name='delete_score'),
    path('', get_scores, name='get_scores'),  # 添加分页查询路径
]