from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .models import CourseOrg,CityDict
from operation.models import UserFavorite,Course
from organization.models import Teacher
from .forms import UserAskForm
from django.http.response import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:3]
        #所有城市
        all_citys = CityDict.objects.all()

        #取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))


        #类别筛选
        catgory = request.GET.get('ct', "")
        if catgory:
            all_orgs = all_orgs.filter(category=catgory)

        #根据学习人数或课程数排列
        sort = request.GET.get('sort','')
        if sort == 'students':
            all_orgs = all_orgs.order_by("-students")
        elif sort == 'courses':
            all_orgs = all_orgs.order_by("-course_nums")

        #共2家
        org_nums = all_orgs.count()

        #机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #2 表示每页的数量
        p = Paginator(all_orgs,2,request=request)
        orgs = p.page(page)

        return render(request,"org-list.html",{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'catgory':catgory,
            'hot_orgs':hot_orgs,
            'sort':sort
        })


class teacher_listView(View):
    pass

class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        # 有外键地方都可以这么取值
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })

class OrgCourseView(View):
    """
    机构课程列表
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        # 有外键地方都可以这么取值
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })

class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 有外键地方都可以这么取值
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 有外键地方都可以这么取值
        return render(request, 'org-detail-teachers.html', {
            "course_org": course_org,
            "all_teachers": all_teachers,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """
    用户收藏
    """
    def post(self,request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated():
            """
            此处user为一个匿名类，django内置的一种方法，此user与正常的user有相似的用法
            所以此处调用user.is_authenticated()方法，后面带括号.
            """
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type="application/json")

        exit_recods = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_recods:
            """
            记录已经存在，则表示要取消收藏
            """
            exit_recods.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums <= 0:
                    course.fav_nums =0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status": "fail", "msg":"收藏出错"}', content_type="application/json")
