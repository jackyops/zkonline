from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher
# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(max_length=30, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name=u"难度")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(max_length=100, upload_to='courses/%Y%m', verbose_name=u"封面图")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name=u"课程分类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    youneed_know = models.CharField(max_length=500, verbose_name=u"课程须知", default="")
    teacher_tell = models.CharField(max_length=500, verbose_name=u"老师告知", default="")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        """
        获取课程章节数
        """
        all_lessons = self.lesson_set.all().count()
        return all_lessons


    def get_learn_users(self):
        return self.usercourse_set.all()[:3]

    def get_course_lesson(self):
        """
        获取课程章节
        :return:
        """
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程")
    name = models.CharField(max_length=100,verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name="章节")
    name = models.CharField(max_length=100,verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

class CourseResurce(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程")
    name = models.CharField(max_length=100,verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name="资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name