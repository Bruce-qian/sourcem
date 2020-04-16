from django.shortcuts import render
from django.http import  HttpResponse
from . import models
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
import datetime
import re
# Create your views here.

#主页
def index(request):
    hook = 0
    #用session判断用户是否登录,is_empty()已登录返回false
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
    except:
        return redirect('/index/login/')
    #所有车俩的集合
    cars = models.Car.objects.all()
    #所有会议室的集合
    mets = models.Metr.objects.all()
    #所有车辆申请
    carapp = models.Carord.objects.all()
    #所有会议室申请
    metapp = models.Metorder.objects.all()
    #计算预约数
    carappnum = carapp.__len__()
    metappnum = metapp.__len__()
    cardict = {}
    metdict ={}
    for c in cars:
        num = carapp.filter(cid=c).__len__()
        cardict[c.cid] = num
    for m in mets:
        num = metapp.filter(mid=m).__len__()
        metdict[m.mid] = num
    NOW = datetime.datetime.now()
    carsix = {}
    metsix = {}
    day0 = NOW.strftime('%Y-%m-%d')#今天3.16
    day1 = (NOW + datetime.timedelta(days=1)).strftime('%Y-%m-%d')#明天3.17
    day2 = (NOW + datetime.timedelta(days=2)).strftime('%Y-%m-%d')#后天.3.18
    day3 = (NOW + datetime.timedelta(days=3)).strftime('%Y-%m-%d') #大后天.3.19
    day4 = (NOW + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')#昨天3.15
    day5 = (NOW + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')#前天3.14
    day6 = (NOW + datetime.timedelta(days=-3)).strftime('%Y-%m-%d')#大后天3.13
    carsix[day6] = carapp.filter(time__gte=day6).filter(time__lt=day5).__len__()  # 3.13-3.14
    carsix[day5] = carapp.filter(time__gte=day5).filter(time__lt=day4).__len__()  # 3.14-3.15
    carsix[day4] = carapp.filter(time__gte=day4).filter(time__lt=day0).__len__()  # 3.15-3.16
    carsix[day0] = carapp.filter(time__gte=day0).filter(time__lt=day1).__len__()#3.16-3.17
    carsix[day1] = carapp.filter(time__gte=day1).filter(time__lt=day2).__len__()#3.17-3.18
    carsix[day2] = carapp.filter(time__gte=day2).filter(time__lt=day3).__len__()#3.18.3.19
    metsix[day6] = metapp.filter(time__gte=day6).filter(time__lt=day5).__len__()  # 3.13-3.14
    metsix[day5] = metapp.filter(time__gte=day5).filter(time__lt=day4).__len__()  # 3.14-3.15
    metsix[day4] = metapp.filter(time__gte=day4).filter(time__lt=day0).__len__()  # 3.15-3.16
    metsix[day0] = metapp.filter(time__gte=day0).filter(time__lt=day1).__len__()  # 3.16-3.17
    metsix[day1] = metapp.filter(time__gte=day1).filter(time__lt=day2).__len__()  # 3.17-3.18
    metsix[day2] = metapp.filter(time__gte=day2).filter(time__lt=day3).__len__()  # 3.18.3.19
    return render(request,'index.html',{'hook':hook, 'name':name, 'carappnum':carappnum, 'metappnum':metappnum,'cardict':cardict, 'metdict':metdict, 'carsix':carsix, 'metsix':metsix})
    #return render(request,'test.html',{'hook':hook, 'name':name, 'carappnum':carappnum, 'metappnum':metappnum,'carsix':carsix})



#登陆后台，现在是明文存储后面改成秘闻
def login(request):
    if request.method == "POST":#判断请求的方式
        message = "请检查填写内容"#初始化提示信息
        username = request.POST['account']
        password = request.POST['psw']
        #判断用户是否存在
        try:
            u = models.User.objects.get(acc=username)
        except:
            message = "用户不存在"
            return render(request, 'login.html', locals())
        #验证用户身份,如果验证不通过就返回none
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['acc'] = u.acc
            request.session['na'] = u.na
            request.session['auth'] = u.auth
            request.session['sex'] = u.sex
            request.session['offer'] = u.offer
            request.session['part'] = u.part
            return redirect('/index/')#身份验证通过跳转到主页
        else:
            message = "密码不正确"
    return render(request, 'login.html', locals())

#用户注册后台函数
def regist(request):
    if request.method == "POST":
        accounts = request.POST['account']
        psw = request.POST['psw']
        psw1 = request.POST['psw1']
        if psw != psw1:
            message = "两次密码不同"
            return render(request, 'regist.html', locals())
        same = models.User.objects.filter(acc=accounts)
        if same:
            message = "用户已存在"
            return render(request, 'regist.html', locals())
        name = request.POST['name']
        sex = request.POST['sex']
        part = request.POST['part']
        offer = request.POST['offer']
        #将除密码之外的信息存储在自定义的用户表中
        user = models.User()
        user.acc = accounts
        #user.paw = psw
        user.na = name
        user.sex = sex
        user.part = part
        user.offer = offer
        user.auth = 0
        user.save()
        #将账户密码存贮的django提供的用户表中，方便调用django的模块进行密码加密和身份验证
        user = User.objects.create_user(username=accounts, password=psw)
        return redirect('/index/login/')#注册成功跳转到登录页面
        #return render(request, 'test.html', locals())
    return render(request, 'regist.html', locals())

'''
#用户查看个人信息的后台
def userInfCheck(request):
    #从session获取用户账号
    #从数据库查找用户信息
    #暂时不提供密码修改功能
    acc = request.session['account']
    #捕捉异常
    user = models.User.objects.get(acc=acc)
    name = user.na
    sex = user.sex
    auth = user.auth
    part = user.part
    offer = user.offer
    hook = 7
    return render(request, 'ucheck.html', {'name':name, 'sex':sex, 'auth':auth, 'part':part, 'offer':offer, 'hook':hook})



#用户个人信息修改函数,暂时不允许修改密码
def userInfChange(request):
    #获取到的修改的信息
    account = request.session['account']
    name = "kk"
    sex = 1
    auth = 0
    part = "市场部"
    offer = "职员"
    user = models.User.objects.get(acc=account)
    user.na = name
    user.sex = sex
    user.auth = auth
    user.part = part
    user.offer = offer
    user.save()
    return redirect('/index/')

'''

#会议室信息录入后台函数
def metInfGet(request):
    # 用session判断用户是否登录,is_empty()已登录返回false
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 6
    #验证权限
    if auth == 0:
        if request.method == "POST":
            numss = request.POST['mid']
            size = request.POST['size']
            lot = request.POST['lot']
            time = request.POST['time']
            dis = request.POST['dis']
            same1 = models.Metr.objects.filter(mid=numss)
            if same1:
                message = "编号已存在"
                return render(request, 'metinf.html', {'message':message, 'hook':hook, 'name':name, 'mid':numss, 'size':size, 'lot':lot, 'time':time, 'dis':dis})
            same2 = models.Car.objects.filter(cid=numss)
            if same2:
                message = "编号已存在"
                return render(request, 'metinf.html', {'message':message, 'hook':hook, 'name':name, 'mid':numss, 'size':size, 'lot':lot, 'time':time, 'dis':dis})
            metr = models.Metr()
            metr.mid = numss
            metr.size = request.POST['size']
            metr.lot = request.POST['lot']
            metr.sta = 0
            metr.tim = request.POST['time']
            metr.dis = request.POST['dis']
            metr.img = request.FILES.get('img')
            metr.save()
            message = "录入成功"
            return render(request, 'metinf.html', {'message':message, 'hook':hook, 'name':name})
        else:
            return render(request, 'metinf.html', {'hook': hook, 'name': name})
    message = "权限不够"
    return render(request, 'metinf.html', {'message':message, 'hook':hook, 'name':name})


#获取所有会议室资源并以列表的形式输出（管理员）
def metlist(request):
    # 用session判断用户是否登录,is_empty()已登录返回false
    if request.session.is_empty():
        return redirect('/index/login/')
    hook = 6
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    if auth == 0:
        mets = models.Metr.objects.all()
        return render(request, 'metlist.html', {'metrs':mets, 'hook':hook, 'name':name})
    else:
        message = "用户权限不足"
        return render(request, 'metlist.html', {'message':message,'hook': hook, 'name': name})

#查看会议室信息(管理员)
def metInfCheck(request):
    #传入的会议室id
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 6
    if auth == 0:
        if request.method == "POST":
            mid = request.POST['mid']
            met = models.Metr.objects.get(mid=mid)
            size = met.size
            lot = met.lot
            dis = met.dis
            sta = met.sta
            time = met.tim
            img = met.img
            return render(request, 'metinfchange.html', {'size':size, 'mid':mid, 'lot':lot, 'dis':dis, 'sta':sta, 'time':time, 'hook':hook, 'name':name, 'img':img})
    return render(request, 'metcheck.html', {'message':'用户权限不足', 'hook':hook, 'name':name})


#会议室删除
def metDel(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 6
    if auth == 0:
        if request.method == "POST":
            mid = request.POST['mid']
            flag = request.POST['flag']
            if flag == "0":
                met = models.Metr.objects.get(mid=mid)
                size = met.size
                lot = met.lot
                dis = met.dis
                sta = met.sta
                time = met.tim
                img = met.img
                return render(request, 'metdel.html',
                              {'size': size, 'mid': mid, 'lot': lot, 'dis': dis, 'sta': sta, 'time': time, 'hook': hook,
                               'name': name, 'img': img})
            if flag == "1":
                num = models.Metr.objects.get(mid=mid).delete()
                if num != 0:
                    message = "删除成功"
                else:
                    message = "删除失败"
                return render(request, 'metdel.html', {'message':message, 'name':name, 'hook':hook})
    return render(request, 'metdel.html', {'message': '用户权限不足', 'hook': hook, 'name': name})


#修改会议室信息
def metInfChange(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 6
    if auth == 0:
        if request.method == "POST":
            mid = request.POST['mid']
            met = models.Metr.objects.get(mid=mid)
            met.size = request.POST['size']
            met.lot = request.POST['lot']
            #met.sta = 0
            met.tim = request.POST['time']
            met.dis = request.POST['dis']
            img = request.FILES.get('img')
            if img is not None:
                met.img = img
            met.save()
            message = "修改成功"
            return render(request, 'metinfchange.html', {'message':message, 'name':name, 'hook':hook})
    message = "用户权限不足"
    return render(request, 'metinfchange.html', {'message': message, 'name': name, 'hook':hook})


#车辆信息录入(管理员)
def carIngGet(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 5
    if auth == 0:
        if request.method == "POST":
            nums = request.POST['cid']
            cflag = request.POST['cflag']
            size = request.POST['size']
            time = request.POST['time']
            chetime = request.POST['chetime']
            comtime = request.POST['comtime']
            suretime = request.POST['suretime']
            same1 = models.Car.objects.filter(cid=nums)
            if same1:
               message = "编号已存在"
               return render(request, 'carinf.html', {'message':message, 'hook':hook, 'name':name, 'cid':nums, 'cflag':cflag, 'size':size, 'time':time, 'chetime':chetime, 'suretime':suretime})
            same2 = models.Metr.objects.filter(mid=nums)
            if same2:
               message = "编号已存在"
               return render(request, 'carinf.html', {'message':message, 'hook':hook, 'name':name, 'cid':nums, 'cflag':cflag, 'size':size, 'time':time, 'chetime':chetime, 'suretime':suretime})
            pat = "^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$"
            result = re.match(pat, cflag, flags=re.I)
            if result is None:
                message = "请检查车牌号"
                return render(request, 'carinf.html', {'message': message, 'hook': hook, 'name': name, 'cid':nums, 'cflag':cflag, 'size':size, 'time':time, 'chetime':chetime, 'suretime':suretime})
            car = models.Car()
            car.cid = request.POST['cid']
            car.cflag = cflag
            car.size = size
            car.sta = 0
            car.tim = time
            car.chetime = chetime
            car.comtime = comtime
            car.suretime = suretime
            car.img = request.FILES.get('img')
            car.save()
            message = "录入成功"
            return render(request, 'carinf.html', {'message':message, 'hook':hook, 'name':name})
        else:
            return render(request, 'carinf.html', {'hook': hook, 'name': name})
    message = "权限不够"
    return render(request, 'carinf.html', {'message':message, 'hook':hook, 'name':name})


#车辆列表（管理员）
def carlist(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 5
    if auth == 0:
        car = models.Car.objects.all()
        return render(request, 'carlist.html', {'cars':car, 'hook':hook, 'name':name})
    return render(request, 'carlist.html', {'message': "用户权限不足", 'hook': hook, 'name':name})


#查看车辆信息,修改车辆信息(管理员)
def carInfCheck(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 5
    #传入的车辆id
    if auth == 0:
        if request.method == "POST":
            cid = request.POST['cid']
            car = models.Car.objects.get(cid=cid)
            sta = car.sta
            size = car.size
            time = car.tim
            suretime = car.suretime
            comtime = car.comtime
            chetime = car.chetime
            cflag = car.cflag
            img = car.img
            return render(request, 'carinfchange.html', {'cid':cid, 'sta':sta, 'size':size, 'time':time, 'suretime':suretime, 'comtime':comtime, 'chetime':chetime, 'cflag':cflag, 'hook':hook, 'name':name, 'img':img})
    return render(request, 'carcheck.html', {'message':'用户权限不足', 'hook':hook, 'name':name})



#删除车辆
def carDel(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 5
    # 传入的车辆id
    message = ""
    if auth == 0:
        if request.method == "POST":
            cid = request.POST['cid']
            flag = request.POST['flag']
            if flag == "0":
                car = models.Car.objects.get(cid=cid)
                sta = car.sta
                size = car.size
                time = car.tim
                suretime = car.suretime
                comtime = car.comtime
                chetime = car.chetime
                cflag = car.cflag
                img = car.img
                return render(request, 'cardel.html',
                              {'cid': cid, 'sta': sta, 'size': size, 'time': time, 'suretime': suretime, 'comtime': comtime,
                               'chetime': chetime, 'cflag': cflag, 'hook': hook, 'name': name, 'img': img})
            if flag == "1":
                num = models.Car.objects.get(cid=cid).delete()
                if num != 0:
                    message = "删除成功"
                else:
                    message = "删除失败"
                return render(request, 'cardel.html', {'message':message, 'name':name, 'hook':hook})
    return render(request, 'cardel.html', {'message': '用户权限不足', 'hook': hook, 'name': name})


#车辆信息修改(管理员)
def carInfChange(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 5
    if auth == 0:
        cid = request.POST['cid']
        cflag = request.POST['cflag']
        size = request.POST['size']
        time = request.POST['time']
        chetime = request.POST['chetime']
        comtime = request.POST['comtime']
        suretime = request.POST['suretime']
        img = request.FILES.get('img')
        try:
            car = models.Car.objects.get(cid=cid)
        except:
            message = "车辆不存在"
            return render(request, 'carinfchange.html', {'name':name, 'hook':hook, 'message':message})
        pat = "^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$"
        result = re.match(pat, cflag, flags=re.I)
        if result is None:
            message = "请检查车牌号"
            return render(request, 'carinfchange.html',
                          {'message': message, 'hook': hook, 'name': name, 'cid': cid, 'cflag': cflag, 'size': size,
                           'time': car.tim, 'chetime': car.chetime, 'suretime': car.suretime, 'comtime':car.comtime, 'img':car.img})
        car.cflag = cflag
        car.size = size
        #car.sta = 0
        car.tim = time
        car.chetime = chetime
        car.comtime = comtime
        car.suretime = suretime
        if img is not None:
            car.img = img
        car.save()
        message = "修改成功"
        return render(request, 'carinfchange.html', {'message':message, 'name':name, 'hook':hook})
    message = "用户权限不足"
    return render(request, 'carinfchange.html', {'message': message, 'name': name, 'hook':hook})





#车辆预预约可用资源查询列表
def carapplist(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 1
    if request.method == "POST":
        stime = request.POST['stime']
        etime = request.POST['etime']
        if stime == "" or stime == "":
            message = "时间不能为空"
            return render(request, 'carapplist.html',
                          {'stime': stime, 'etime': etime, 'message': message, 'name': name})
        if stime >= etime:
            message = "结束时间需要大于开始时间"
            return render(request, 'carapplist.html', {'stime':stime, 'etime':etime, 'message':message, 'name':name})
        NOW = datetime.datetime.now()
        strs = NOW.strftime('%Y-%m-%d %H:%M:%S')
        if stime < strs:
            message = "开始时间不能小于现在时间"
            return render(request, 'carapplist.html',
                          {'stime': stime, 'etime': etime, 'message': message, 'name': name})
        s = models.Carord.objects.filter(stime__lte=etime).filter(etime__gte=stime).values_list('cid')  # 返回开始时间小于等于etime或结束时间大于等于stime的记录的车辆的id的元组
        exCars = models.Car.objects.exclude(cid__in=s)  # 剔除时间上重叠的车辆，并返回quertset
        return render(request, 'carapplist.html', {'stime':stime, 'etime':etime, 'cars':exCars, 'hook':hook, 'name':name})
    return render(request, 'carapplist.html', {'hook':hook, 'name':name})

#车辆预约信息确认与预约信息完善
def corderconf(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 1
    if request.method == "POST":
        cid = request.POST['cid']
        cflag = request.POST['cflag']
        size = request.POST['size']
        sta = request.POST['sta']
        stime = request.POST['stime']
        etime = request.POST['etime']
        img = models.Car.objects.get(cid=cid).img
        return render(request, 'corconf.html', {'cid':cid, 'cflag':cflag, 'size':size, 'sta':sta, 'stime':stime, 'etime':etime, 'hook':hook, 'name':name, 'img':img})
    message = "出错了"
    return render(request, 'corconf.html', {'message':message, 'hook':hook, 'name':name})

#车辆预约（）
def carOrder(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 1
    if request.method == "POST":
        acc = request.session['acc']
        try:
            user = models.User.objects.get(acc=acc)
        except:
            message = "用户不存在"
            return render(request, 'carapplist.html', {'message': message, 'hook': hook, 'name': name})
        # 确定该编号是否存在
        # 是否有冲突的预约记录
        cid = request.POST['cid']
        try:
            car = models.Car.objects.get(cid=cid)#设置try捕捉异常
        except:
            message = "车辆不存在"
            return render(request, 'carapplist.html', {'message': message, 'hook': hook, 'name': name})
        stime = request.POST['stimes']
        etime = request.POST['etimes']
        foor = request.POST['foor']
        corder = models.Carord()
        corder.acc = user
        corder.cid = car
        corder.sta = 0
        corder.stime = stime
        corder.etime = etime
        corder.foor = foor
        corder.time = datetime.datetime.now()
        corder.save()
        message = "车辆申请成功"
        return render(request, 'carapplist.html', {'message':message, 'hook':hook, 'name':name})
    message = "车辆申请失败"
    return render(request, 'carapplist.html', {'message': message, 'hook':hook, 'name':name})


#车辆申请审核界面(管理员)
def carordere(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 3
    message2 = ""
    NOW = datetime.datetime.now()
    strs = NOW.strftime('%Y-%m-%d')
    carords = models.Carord.objects.filter(sta=0).filter(etime__lte=strs)
    for c in carords:
        c.sta = 2
        c.save()
    if auth == 0:
        if request.method == "POST":
            orderid = request.POST['orderid']
            sta = request.POST['chose']
            try:
                carorder = models.Carord.objects.get(id=orderid)
                carorder.sta = sta
                carorder.save()
                message2 = "操作成功"
            except:
                message2 = "该申请不存在"
        carorders = models.Carord.objects.filter(sta=0)#没有符合的返回0,none
        if carorders is None:
            message = "没有要审核的记录"
            return render(request, 'carordere.html', {'message':message, 'message2':message2, 'name':name, 'hook':hook})
        return render(request, 'carordere.html', {'carorders':carorders, 'hook':hook, 'message2':message2, 'name':name})
    message = "权限不够"
    return render(request, 'carordere.html', {'message':message, 'hook':hook, 'name':name})



#会议室预预约可用资源查询列表
def metapplist(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 2
    if request.method == "POST":
        stime = request.POST['stime']
        etime = request.POST['etime']
        if stime == "" or etime == "":
            message = "时间不能为空"
            return render(request, 'metapplist.html',
                          {'stime': stime, 'etime': etime, 'message': message, 'hook': hook, 'name': name})
        if stime >= etime:
            message = "结束时间不能小于开始时间"
            return render(request, 'metapplist.html', {'stime':stime, 'etime':etime, 'message':message, 'hook':hook, 'name':name})
        NOW = datetime.datetime.now()
        strs = NOW.strftime('%Y-%m-%d %H:%M:%S')
        if stime < strs:
            message = "开始时间不能小于当前时间"
            return render(request, 'metapplist.html',
                          {'stime': stime, 'etime': etime, 'message': message, 'hook': hook, 'name': name})
        m = models.Metorder.objects.filter(stime__lte=etime).filter(etime__gte=stime).values_list(
            'mid')  # 查找时间重叠的会议室并将会议室的id以元组的形式返回
        exMet = models.Metr.objects.exclude(mid__in=m)
        return render(request, 'metapplist.html', {'stime':stime, 'etime':etime, 'mets':exMet, 'hook':hook, 'name':name})
    return render(request, 'metapplist.html', {'hook':hook, 'name':name})



#会议室预约信息确认与完善
def metordercon(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 2
    if request.method == "POST":
        mid = request.POST['mid']
        size = request.POST['size']
        stime = request.POST['stime']
        etime = request.POST['etime']
        lot = request.POST['lot']
        img = models.Metr.objects.get(mid=mid).img
        return render(request, 'metconf.html', {'mid':mid, 'size':size, 'stime':stime, 'etime':etime, 'lot':lot, 'hook':hook, 'name':name, 'img':img})


#会议室预约
def metOrder(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 2
    if request.method == "POST":
        acc = request.session['acc']
        mid = request.POST['mid']
        stime = request.POST['stime']
        etime = request.POST['etime']
        foor = request.POST['foor']
        try:
            user = models.User.objects.get(acc=acc)
            met = models.Metr.objects.get(mid=mid)
        except:
            message = "出现错误"
            return render(request, 'metapplist.html', {'message': message, 'hook': hook, 'name': name})
        metorder = models.Metorder()
        metorder.acc = user
        metorder.mid = met
        metorder.stime = stime
        metorder.etime = etime
        metorder.sta = 0
        metorder.time = datetime.datetime.now()
        metorder.foor = foor
        metorder.save()
        message = "会议室申请成功"
        return render(request, 'metapplist.html', {'message':message, 'hook':hook, 'name':name})
    message = "会议室申请失败"
    return render(request, 'metapplist.html', {'message':message, 'hook':hook, 'name':name})


#审核会议室的申请(管理员)
def metordere(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 4
    auth = request.session['auth']
    message2 = ""
    NOW = datetime.datetime.now()
    strs = NOW.strftime('%Y-%m-%d')
    metords = models.Metorder.objects.filter(sta=0).filter(etime__lte=strs)
    for m in metords:
        m.sta = 2
        m.save()
    if auth == 0:
        if request.method == "POST":
            orderid = request.POST['orderid']
            sta = request.POST['chose']
            try:
                metorder = models.Metorder.objects.get(id=orderid)
                metorder.sta = sta
                metorder.save()
                message2 = "操作成功"
            except:
                message2 = "该申请不存在"
        metorders = models.Metorder.objects.filter(sta=0)
        if metorders is None:
            message = "没有要审查的记录"
            return render(request, 'metordere.html', {'message': message, 'hook':hook, 'message2':message2, 'name':name})
        return render(request, 'metordere.html', {'metorders':metorders, 'hook':hook, 'name':name, 'message2':message2})
    message = "权限不够"
    return render(request, 'metordere.html', {'message':message, 'hook':hook, 'name':name})



#用户中心,显示用户的个人信息
def user(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    hook = 7
    try:
        acc = request.session['acc']
    except:
        return redirect('/index/login/')
    message = ""
    if request.method == "POST":
        try:
            u = models.User.objects.get(acc=acc)
        except:
            message = "用户不存在"
            return render(request, 'user.html', {'message':message, 'hook':hook})
        na = request.POST['name']
        sex = request.POST['sex']
        part = request.POST['part']
        offer = request.POST['offer']
        psw = request.POST['psw']
        psw1 = request.POST['psw1']
        ff = request.POST['shifou']
        if ff == "0" and psw != "" and psw1 != "":  # 要修改密码
            if psw != psw1:
                message = "两次密码不同"
            else:
                try:
                    user = User.objects.get(username=acc)
                except:
                    message = "用户不存在"
                    return render(request, 'user.html', {'message': message, 'hook': hook})
                user.set_password(psw)
                user.save()
                u.na = na
                u.sex = sex
                u.part = part
                u.offer = offer
                u.save()
                message = "修改成功"
                #同步修改session内容
                request.session['na'] = na
                request.session['sex'] = sex
                request.session['offer'] = offer
                request.session['part'] = part
    try:
        user = models.User.objects.get(acc=acc)
    except:
        message = "用户不存在"
        return render(request, 'user.html', {'message': message, 'hook': hook})
    offer = user.offer
    part = user.part
    auth = user.auth
    sex = user.sex
    na = user.na
    name = request.session['na']
    return render(request, 'user.html', {'acc':acc, 'offer':offer, 'part':part, 'auth':auth, 'sex':sex, 'na':na, 'hook':hook, 'name':name, 'message':message})


#我的申请及取消申请
def myapply(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
        acc = request.session['acc']
    except:
        return redirect('/index/login/')
    hook = 8
    message = ""
    NOW = datetime.datetime.now()
    strs = NOW.strftime('%Y-%m-%d')
    carords = models.Carord.objects.filter(sta=0).filter(etime__lte=strs)
    metords = models.Metorder.objects.filter(sta=0).filter(etime__lte=strs)
    for c in carords:
        c.sta = 2#过期
        c.save()
    for m in metords:
        m.sta = 2
        m.save()
    if request.method == "POST":
        tp = request.POST['type']
        id = request.POST['id']
        if id != "":
            if tp == "car":
                try:
                    models.Carord.objects.get(id=id).delete()
                    message = "操作成功"
                except:
                    message = "操作失败"
            elif tp == "met":
                try:
                    models.Metorder.objects.get(id=id).delete()
                    message = "操作成功"
                except:
                    message = "操作失败"
        else:
            message = "出现错误"
    acc = request.session['acc']
    carorder = models.Carord.objects.filter(acc=acc)
    metorder = models.Metorder.objects.filter(acc=acc)
    return render(request, 'myapply.html', {'carorders':carorder, 'metorders':metorder, 'message':message, 'hook':hook, 'name':name})




#用户管理（管理员）
def uManage(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 9
    if auth == 0:
        if request.method == "POST":
            acc = request.POST['acc']
            try:
                users = models.User.objects.filter(acc=acc)
            except:
                message = "用户不存在"
                return  render(request, 'umanage.html', {'hook':hook, 'name':name, 'message':message})
            return render(request, 'umanage.html', {'users': users, 'hook': hook, 'name': name})
        else:
            users = models.User.objects.all()
            return render(request, 'umanage.html', {'users':users, 'hook':hook, 'name':name})
    message = "用户权限不够"
    return render(request, 'umanage.html', {'message':message, 'name':name, 'hook':hook})

#添加用户（管理员）
def uManageAdd(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 9
    if auth == 0:
        if request.method == "POST":
            accounts = request.POST['account']
            psw = request.POST['psw']
            psw1 = request.POST['psw1']
            if psw != psw1:
                message = "两次密码不同"
                return render(request, 'umanageadd.html', locals())
            same = models.User.objects.filter(acc=accounts)
            if same:
                message = "用户已存在"
                return render(request, 'umanageadd.html', locals())
            name = request.POST['name']
            sex = request.POST['sex']
            part = request.POST['part']
            offer = request.POST['offer']
            # 将除密码之外的信息存储在自定义的用户表中
            user = models.User()
            user.acc = accounts
            # user.paw = psw
            user.na = name
            user.sex = sex
            user.part = part
            user.offer = offer
            user.auth = 0
            user.save()
            # 将账户密码存贮的django提供的用户表中，方便调用django的模块进行密码加密和身份验证
            user = User.objects.create_user(username=accounts, password=psw)
            message = "添加成功"
            return render(request, 'umanageadd.html', {'name': name, 'hook': hook, 'message':message})
        else:
            return render(request, 'umanageadd.html', {'name':name, 'hook':hook})
    message = "用户权限不足"
    return render(request, 'umanageadd.html', {'name': name, 'hook': hook, 'message':message})


#修改用胡信息（管理员）
def uManageChange(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 9
    if auth == 0:
        acc = request.POST['acc']
        try:
            u = models.User.objects.get(acc=acc)
        except:
            message = "用户不存在"
            return render(request, 'umanagechange.html', {'message':message, 'name':name, 'hook':hook})
        flag = request.POST['flag']
        if flag == "0":
            return render(request, 'umanagechange.html', {'name':name, "hook":hook, 'user':u})
        if flag == "1":
            psw = request.POST['psw']
            psw1 = request.POST['psw1']
            if psw != "def" and psw1 != "def" and psw != "" and psw1 != "":#要修改密码
                if psw != psw1:
                    message = "两次密码不同"
                    return render(request, 'umanagechange.html', locals())
                else:
                    try:
                        user = User.objects.get(username=acc)
                    except:
                        message = "出现错误"
                        return render(request, 'umanagechange.html', {'name': name, 'hook': hook, 'message': message})
                    user.set_password(psw)
                    user.save()
            name = request.POST['name']
            sex = request.POST['sex']
            part = request.POST['part']
            offer = request.POST['offer']
            u.na = name
            u.sex = sex
            u.part = part
            u.offer = offer
            u.save()
            message = "修改成功"
            return render(request, 'umanagechange.html', {'name':name, 'hook':hook, 'user':u, 'message':message})
    message = "用户权限不足"
    return render(request, 'umanagechange.html', {'name': name, 'hook': hook, 'message': message})


#删除用户（管理员）
def userDel(request):
    if request.session.is_empty():
        return redirect('/index/login/')
    try:
        name = request.session['na']
        auth = request.session['auth']
    except:
        return redirect('/index/login/')
    hook = 9
    message = ""
    if auth == 0:
        acc = request.POST['acc']
        try:
            u = models.User.objects.get(acc=acc)
        except:
            message = "用户不存在"
            return render(request, 'userdel.html', {'message': message, 'name': name, 'hook': hook})
        flag = request.POST['flag']
        if flag == "0":
            return render(request, 'userdel.html', {'name': name, "hook": hook, 'user': u})
        if flag == "1":
            try:
                num1 = models.User.objects.get(acc=acc).delete()
                num2 = User.objects.get(username=acc).delete()
            except:
                message = "出现错误"
                return render(request, 'userdel.html', {'name': name, 'hook': hook, 'message': message})
            if num1 and num2:
                message = "删除成功"
            else:
                message = "删除失败"
            return render(request, 'userdel.html', {'name': name, 'hook': hook, 'message': message})
    message = "用户权限不足"
    return render(request, 'userdel.html', {'name': name, 'hook': hook, 'message': message})




#退出
def logOut(request):
    logout(request)
    return redirect('/index/login/')