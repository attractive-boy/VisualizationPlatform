from django.urls import path
from . import views

urlpatterns = [
    # 1.1 不同年份的高考全国总平均分变化趋势折线图
    path('national_average_score_trend/', views.national_average_score_trend, name='national_average_score_trend'),

    # 1.2 不同年份的各科成绩平均分柱状图，柱状图底下显示对应的年份
    path('subject_avg_score_bar_chart/', views.subject_avg_score_bar_chart, name='subject_avg_score_bar_chart'),

    # 1.3 不同年份的全国高考及格率趋势折线图
    path('national_pass_rate_trend/', views.national_pass_rate_trend, name='national_pass_rate_trend'),

    # 1.4 具体年份的各科成绩平均分柱状图
    path('subject_avg_score_by_year/<int:year>/', views.subject_avg_score_by_year, name='subject_avg_score_by_year'),

    # 2.1 具体地区对应不同年份的高考总平均分变化趋势折线图
    path('area_average_score_trend/', views.area_average_score_trend, name='area_average_score_trend'),

    # 2.2 具体地区对应的不同年份的各科成绩平均分柱状图
    path('subject_avg_score_by_area/', views.subject_avg_score_by_area, name='subject_avg_score_by_area'),

    # 2.3 具体地区对应的不同年份的高考及格率趋势折线图
    path('area_pass_rate_trend/', views.area_pass_rate_trend, name='area_pass_rate_trend'),

    # 2.4 具体地区具体年份的各科成绩平均分柱状图
    path('subject_avg_score_by_area_and_year/', views.subject_avg_score_by_area_and_year, name='subject_avg_score_by_area_and_year'),

    # 3.1 具体城市对应不同年份的高考总平均分变化趋势折线图
    path('city_average_score_trend/', views.city_average_score_trend, name='city_average_score_trend'),

    # 3.2 具体城市不同年份各科成绩平均分柱状图
    path('subject_avg_score_by_city/', views.subject_avg_score_by_city, name='subject_avg_score_by_city'),

    # 3.3 具体城市的不同年份高考及格率趋势折线图
    path('city_pass_rate_trend/', views.city_pass_rate_trend, name='city_pass_rate_trend'),

    # 3.4 具体城市具体年份各科成绩平均分柱状图
    path('subject_avg_score_by_city_and_year/', views.subject_avg_score_by_city_and_year, name='subject_avg_score_by_city_and_year'),

]
