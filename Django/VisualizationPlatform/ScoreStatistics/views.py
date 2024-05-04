# views.py

from django.http import JsonResponse
from .models import ScoreStatistics
from django.db import models


# 1.1 不同年份的高考全国总平均分变化趋势折线图
def national_average_score_trend(request):
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    avg_scores = []
    for year in years:
        total_score_sum = ScoreStatistics.objects.filter(year=year).aggregate(total_score_sum=models.Sum('total_score'))['total_score_sum']
        data_count_sum = ScoreStatistics.objects.filter(year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
        if total_score_sum and data_count_sum:
            avg_score = total_score_sum / data_count_sum
            avg_scores.append({'year': year, 'average_score': avg_score})
    data = {'national_average_score_trend': avg_scores}
    return JsonResponse(data)

# 1.2 不同年份的各科成绩平均分柱状图，柱状图底下显示对应的年份
def subject_avg_score_bar_chart(request):
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score', 'biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores_by_year = []
    for year in years:
        liberal_arts_count = ScoreStatistics.objects.filter(year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
        science_count = ScoreStatistics.objects.filter(year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
        avg_scores = {'year': year}
        for subject in subjects:
            total_score_sum = ScoreStatistics.objects.filter(year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
            data_count_sum = ScoreStatistics.objects.filter(year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
            if total_score_sum is not None and data_count_sum is not None and data_count_sum != 0:
                if subject in ['language_score', 'politics_score', 'history_score']:
                    avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
                else:
                    avg_score = total_score_sum / science_count if science_count != 0 else 0
                avg_scores[subject.replace('_score', '')] = avg_score
        avg_scores_by_year.append(avg_scores)
    data = {'subject_avg_score_bar_chart': avg_scores_by_year}
    return JsonResponse(data)

# 1.3 不同年份的全国高考及格率趋势折线图
def national_pass_rate_trend(request):
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    pass_rates = []
    for year in years:
        total_count = ScoreStatistics.objects.filter(year=year).aggregate(total_count=models.Sum('data_count'))['total_count']
        pass_count = ScoreStatistics.objects.filter(year=year).aggregate(pass_count=models.Sum('pass_count'))['pass_count']
        if total_count:
            pass_rate = pass_count / total_count
            pass_rates.append({'year': year, 'pass_rate': pass_rate})
    data = {'national_pass_rate_trend': pass_rates}
    return JsonResponse(data)

# 1.4 具体年份的各科成绩平均分柱状图
def subject_avg_score_by_year(request, year):
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score', 'biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores = {}
    liberal_arts_count = ScoreStatistics.objects.filter(year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
    science_count = ScoreStatistics.objects.filter(year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
    for subject in subjects:
        total_score_sum = ScoreStatistics.objects.filter(year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
        data_count_sum = ScoreStatistics.objects.filter(year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
        if total_score_sum and data_count_sum:
            if subject in ['language_score', 'politics_score', 'history_score']:
                avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
            else:
                avg_score = total_score_sum / science_count if science_count != 0 else 0
            avg_scores[subject.replace('_score', '')] = avg_score
    data = {'subject_avg_score_by_year': avg_scores}
    return JsonResponse(data)

# 2.1 具体地区对应不同年份的高考总平均分变化趋势折线图
def area_average_score_trend(request):
    provinces = ScoreStatistics.objects.values_list('province', flat=True).distinct()
    avg_scores_by_province = {}
    for province in provinces:
        years = ScoreStatistics.objects.filter(province=province).values_list('year', flat=True).distinct()
        avg_scores_by_year = []
        for year in years:
            total_score_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(total_score_sum=models.Sum('total_score'))['total_score_sum']
            data_count_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
            if total_score_sum and data_count_sum:
                avg_score = total_score_sum / data_count_sum
                avg_scores_by_year.append({'year': year, 'average_score': avg_score})
        avg_scores_by_province[province] = avg_scores_by_year
    data = {'area_average_score_trend': avg_scores_by_province}
    return JsonResponse(data)

# 2.2 具体地区对应的不同年份的各科成绩平均分柱状图
def subject_avg_score_by_area(request):
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score', 'biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores_by_area = {}

    provinces = ScoreStatistics.objects.values_list('province', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()

    for province in provinces:
        avg_scores_by_year = {}
        for year in years:
            avg_scores = {}
            liberal_arts_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            for subject in subjects:
                total_score_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
                data_count_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
                if total_score_sum is not None and data_count_sum is not None and data_count_sum != 0:
                    if subject in ['language_score', 'politics_score', 'history_score']:
                        avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
                    else:
                        avg_score = total_score_sum / science_count if science_count != 0 else 0
                    avg_scores[subject.replace('_score', '')] = avg_score
            avg_scores_by_year[year] = avg_scores
        avg_scores_by_area[province] = avg_scores_by_year

    data = {'subject_avg_score_by_area': avg_scores_by_area}
    return JsonResponse(data)

# 2.3 具体地区对应的不同年份的高考及格率趋势折线图
def area_pass_rate_trend(request):
    provinces = ScoreStatistics.objects.values_list('province', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    pass_rates_by_area_and_year = {}
    
    for province in provinces:
        pass_rates_by_year = []
        for year in years:
            liberal_arts_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            total_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(total_count=models.Sum('data_count'))['total_count']
            pass_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(pass_count=models.Sum('pass_count'))['pass_count']
            if total_count is not None and total_count != 0:
                pass_rate = pass_count / total_count
                pass_rates_by_year.append({'year': year, 'pass_rate': pass_rate})
        pass_rates_by_area_and_year[province] = pass_rates_by_year
    
    data = {'area_pass_rate_trend': pass_rates_by_area_and_year}
    return JsonResponse(data)

# 2.4 具体地区具体年份的各科成绩平均分柱状图
def subject_avg_score_by_area_and_year(request):
    provinces = ScoreStatistics.objects.values_list('province', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score','biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores_by_area_and_year = {}
    
    for province in provinces:
        avg_scores_by_year = {}
        for year in years:
            avg_scores = {}
            liberal_arts_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(province=province, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            for subject in subjects:
                total_score_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
                data_count_sum = ScoreStatistics.objects.filter(province=province, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
                if total_score_sum is not None and data_count_sum is not None and data_count_sum != 0:
                    if subject in ['language_score', 'politics_score', 'history_score']:
                        avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
                    else:
                        avg_score = total_score_sum / science_count if science_count != 0 else 0
                    avg_scores[subject.replace('_score', '')] = avg_score
            avg_scores_by_year[year] = avg_scores
        avg_scores_by_area_and_year[province] = avg_scores_by_year
    
    data = {'subject_avg_score_by_area_and_year': avg_scores_by_area_and_year}
    return JsonResponse(data)

# 3.1 具体城市对应不同年份的高考总平均分变化趋势折线图
def city_average_score_trend(request):
    cities = ScoreStatistics.objects.values_list('city', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    avg_scores_by_city_and_year = {}
    for city in cities:
        avg_scores_by_year = []
        for year in years:
            liberal_arts_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            total_score_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(total_score_sum=models.Sum('total_score'))['total_score_sum']
            data_count_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
            if total_score_sum and data_count_sum:
                avg_score = total_score_sum / data_count_sum
                avg_scores_by_year.append({'year': year, 'average_score': avg_score})
        avg_scores_by_city_and_year[city] = avg_scores_by_year
    data = {'city_average_score_trend': avg_scores_by_city_and_year}
    return JsonResponse(data)

# 3.2 具体城市不同年份各科成绩平均分柱状图
def subject_avg_score_by_city(request):
    cities = ScoreStatistics.objects.values_list('city', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score', 'biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores_by_city_and_year = {}
    for city in cities:
        avg_scores_by_year = {}
        for year in years:
            avg_scores = {}
            liberal_arts_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            for subject in subjects:
                total_score_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
                data_count_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
                if total_score_sum is not None and data_count_sum is not None and data_count_sum != 0:
                    if subject in ['language_score', 'politics_score', 'history_score']:
                        avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
                    else:
                        avg_score = total_score_sum / science_count if science_count != 0 else 0
                    avg_scores[subject.replace('_score', '')] = avg_score
            avg_scores_by_year[year] = avg_scores
        avg_scores_by_city_and_year[city] = avg_scores_by_year
    data = {'subject_avg_score_by_city': avg_scores_by_city_and_year}
    return JsonResponse(data)

# 3.3 具体城市的不同年份高考及格率趋势折线图
def city_pass_rate_trend(request):
    cities = ScoreStatistics.objects.values_list('city', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    pass_rates_by_city_and_year = {}
    for city in cities:
        pass_rates_by_year = []
        for year in years:
            liberal_arts_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            total_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(total_count=models.Sum('data_count'))['total_count']
            pass_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(pass_count=models.Sum('pass_count'))['pass_count']
            if total_count is not None and total_count != 0:
                pass_rate = pass_count / total_count
                pass_rates_by_year.append({'year': year, 'pass_rate': pass_rate})
        pass_rates_by_city_and_year[city] = pass_rates_by_year
    data = {'city_pass_rate_trend': pass_rates_by_city_and_year}
    return JsonResponse(data)

# 3.4 具体城市具体年份各科成绩平均分柱状图
def subject_avg_score_by_city_and_year(request):
    cities = ScoreStatistics.objects.values_list('city', flat=True).distinct()
    years = ScoreStatistics.objects.values_list('year', flat=True).distinct()
    subjects = ['language_score', 'mathematics_score', 'english_score', 'chemistry_score', 'physics_score', 'biology_score', 'geography_score', 'politics_score', 'history_score']
    avg_scores_by_city_and_year = {}
    for city in cities:
        avg_scores_by_year = {}
        for year in years:
            avg_scores = {}
            liberal_arts_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(liberal_arts_count=models.Sum('liberal_arts_count'))['liberal_arts_count']
            science_count = ScoreStatistics.objects.filter(city=city, year=year).aggregate(science_count=models.Sum('science_count'))['science_count']
            for subject in subjects:
                total_score_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(total_score_sum=models.Sum(subject))['total_score_sum']
                data_count_sum = ScoreStatistics.objects.filter(city=city, year=year).aggregate(data_count_sum=models.Sum('data_count'))['data_count_sum']
                if total_score_sum is not None and data_count_sum is not None and data_count_sum != 0:
                    if subject in ['language_score', 'politics_score', 'history_score']:
                        avg_score = total_score_sum / liberal_arts_count if liberal_arts_count != 0 else 0
                    else:
                        avg_score = total_score_sum / science_count if science_count != 0 else 0
                    avg_scores[subject.replace('_score', '')] = avg_score
            avg_scores_by_year[year] = avg_scores
        avg_scores_by_city_and_year[city] = avg_scores_by_year
    data = {'subject_avg_score_by_city_and_year': avg_scores_by_city_and_year}
    return JsonResponse(data)
