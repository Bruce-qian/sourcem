from django.urls import path
from django.conf.urls.static import static
from sourcem import settings
from . import views

app_name = 'source_manager'
urlpatterns = [
    path('', views.index, name='index_page'),#默认主页
    path('login/', views.login, name='login_page'),#登陆叶面
    path('regist/', views.regist, name='regist_page'),#用户注册
    path('metget/', views.metInfGet, name='metget_page'),#会议室信息录入
    path('carget/', views.carIngGet, name='carget_page'),#车辆信息录入
    path('carorder/', views.carOrder, name='carorder_page'), #车辆预约
    path('metorder/', views.metOrder, name='metorder_page'), #会议室预约
    #path('ucheck/', views.userInfCheck, name='ucheck_page'), #用户查看自己的个人信息
    #path('uchange/', views.userInfChange, name='uchange_page'), #更改用户信息
    path('metcheck/', views.metInfCheck, name='metcheck_page'), #查看会议室信息
    path('carcheck/', views.carInfCheck, name='carcheck_page'), #查看会议室信息
    path('metlist/', views.metlist, name='metlist_page'), #会议室列表
    path('carlist/', views.carlist, name='carlist_page'), #车辆列表
    path('carapplist/', views.carapplist, name='carapplist_page'), #车辆预约可用资源列表
    path('metapplist/', views.metapplist, name='metapplist_page'), #会议室预约可用资源列表
    path('metordere/', views.metordere, name='metordere_page'), #会议室预约申请审核
    path('carordere/', views.carordere, name='carordere_page'), #车辆预约申请审核
    path('user/', views.user, name='user_page'), #个人中心
    path('myapply/', views.myapply, name='myapply_page'), #我的申请及取消申请
    path('cordercon/', views.corderconf, name='cordercon_page'), #车辆申请信息确认和信息完善
    path('metcon/', views.metordercon, name='metordercon_page'), #会议室申请信息确认和信息完善
    path('logout/', views.logOut, name='logout_page'), #退出
    path('metinfch/', views.metInfChange, name='metinfch_page'), #会议室信息修改
    path('carinfch/', views.carInfChange, name='carinfch_page'), #车辆信息修改
    path('umanage/', views.uManage, name='umanage_page'), #用户管理（管理员）
    path('umanageadd/', views.uManageAdd, name='umanageadd_page'), #添加用户（管理员）
    path('umanagechange/', views.uManageChange, name='umanagechange_page'), #修改用户信息（管理员）
    path('userdel/', views.userDel, name='userdel_page'), #删除用户（管理员）
    path('cardel/', views.carDel, name='cardel_page'), #删除车辆（管理员）
    path('metdel/', views.metDel, name='metdel_page'), #删除会议室（管理员）
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
