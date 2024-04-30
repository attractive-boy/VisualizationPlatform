from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Score
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'year': openapi.Schema(type=openapi.TYPE_INTEGER),
        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
        'subject': openapi.Schema(type=openapi.TYPE_STRING),
        'province': openapi.Schema(type=openapi.TYPE_STRING),
        'city': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['POST'])
@permission_classes([AllowAny])  # 或者使用 IsAuthenticated
def create_score(request):
    """
    Create a new score entry.

    Parameters:
    - year (int): The year of the score.
    - score (float): The score value.
    - subject (str): The subject of the score.
    - province (str): The province of the score.
    - city (str): The city of the score.
    """
    if request.method == 'POST':
        # 从请求中获取数据
        data = request.POST
        # 创建成绩对象
        score = Score.objects.create(
            year=data.get('year'),
            score=data.get('score'),
            subject=data.get('subject'),
            province=data.get('province'),
            city=data.get('city')
        )
        return JsonResponse({'message': 'Score created successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'year': openapi.Schema(type=openapi.TYPE_INTEGER),
        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
        'subject': openapi.Schema(type=openapi.TYPE_STRING),
        'province': openapi.Schema(type=openapi.TYPE_STRING),
        'city': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['POST'])
@permission_classes([AllowAny])  # 或者使用 IsAuthenticated
def update_score(request, score_id):
    """
    Update an existing score entry.

    Parameters:
    - year (int): The year of the score.
    - score (float): The score value.
    - subject (str): The subject of the score.
    - province (str): The province of the score.
    - city (str): The city of the score.
    """
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        return JsonResponse({'error': 'Score does not exist'}, status=404)

    if request.method == 'POST':
        data = request.POST
        score.year = data.get('year')
        score.score = data.get('score')
        score.subject = data.get('subject')
        score.province = data.get('province')
        score.city = data.get('city')
        score.save()
        return JsonResponse({'message': 'Score updated successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

@swagger_auto_schema(method='delete')
@api_view(['DELETE'])
@permission_classes([AllowAny])  # 或者使用 IsAuthenticated
def delete_score(request, score_id):
    """
    Delete an existing score entry.
    """
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        return JsonResponse({'error': 'Score does not exist'}, status=404)

    if request.method == 'DELETE':
        score.delete()
        return JsonResponse({'message': 'Score deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=400)

@swagger_auto_schema(method='get', responses={200: openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'year': openapi.Schema(type=openapi.TYPE_INTEGER),
        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
        'subject': openapi.Schema(type=openapi.TYPE_STRING),
        'province': openapi.Schema(type=openapi.TYPE_STRING),
        'city': openapi.Schema(type=openapi.TYPE_STRING),
    }
)})
@api_view(['GET'])
@permission_classes([AllowAny])  # 或者使用 IsAuthenticated
def get_score(request, score_id):
    """
    Get details of a specific score entry.

    Parameters:
    - score_id (int): The ID of the score entry.
    """
    try:
        score = Score.objects.get(id=score_id)
    except Score.DoesNotExist:
        return JsonResponse({'error': 'Score does not exist'}, status=404)

    if request.method == 'GET':
        data = {
            'year': score.year,
            'score': score.score,
            'subject': score.subject,
            'province': score.province,
            'city': score.city
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=400)


# 在视图函数中实现分页查询
@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number')
])
@api_view(['GET'])
@permission_classes([AllowAny])  # 或者使用 IsAuthenticated
def get_scores(request):
    """
    Get a paginated list of score entries.

    Parameters:
    - page (int, optional): The page number (default: 1).
    """
    # 获取所有成绩对象
    all_scores = Score.objects.all()

    # 每页显示的成绩数量
    per_page = 10

    # 创建分页器对象
    paginator = Paginator(all_scores, per_page)

    # 获取页码，默认为第一页
    page_number = request.GET.get('page', 1)

    try:
        # 获取指定页码的成绩对象
        scores_page = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果页码不是整数，则默认为第一页
        scores_page = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，则返回最后一页的成绩对象
        scores_page = paginator.page(paginator.num_pages)

    # 构造分页查询结果
    results = []
    for score in scores_page:
        results.append({
            'year': score.year,
            'score': score.score,
            'subject': score.subject,
            'province': score.province,
            'city': score.city
        })

    # 返回分页查询结果
    return JsonResponse({
        'count': paginator.count,
        'next': scores_page.next_page_number() if scores_page.has_next() else None,
        'previous': scores_page.previous_page_number() if scores_page.has_previous() else None,
        'results': results
    })
      
