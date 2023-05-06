from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db import connection
from django.conf import settings
from django.db.models import Q
from django.core.mail import EmailMessage

def home(request):
    return render(request,'home.html',{})
def public_register(request):
    if request.method == 'POST':
        email = request.POST.get('lastname')
        uname = request.POST.get('username')
        psw = request.POST.get('password')
        pnum = request.POST.get('mail')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        addr = request.POST.get('addr')
        img = request.FILES['image']
        phone = len(pnum)
        if phone == 10:
            crt = Public_Detail.objects.create(email=email,
            phone_number=pnum,username=uname,password=psw,image=img,
            country=country,state=state,city=city,address=addr,status='Pending')
            recipient_list = [email]
            email_from = settings.EMAIL_HOST_USER
            b = EmailMessage('Verify Your  E-Mail ','Click Here: http://127.0.0.1:8000/verify_email/',email_from,recipient_list).send()
            if crt:
                messages.success(request,'Registered Successfully')
                return redirect('public_login')
        else:
            messages.success(request,'Phone Number Must Contain 10 Digit')

    return render(request,'public_register.html',{})
def verify_email(request):
    cursor=connection.cursor()
    sql=''' SELECT p.id from app_public_detail as p ORDER BY p.id DESC'''
    res=cursor.execute(sql)
    row=cursor.fetchone()
    ids=row[0]
    Public_Detail.objects.filter(id=int(ids)).update(status='Verified')
    return render(request,'verify_email.html',{})
def public_login(request):
    if request.session.has_key('public'):
        return redirect("public_dashboard")
    else:
        if request.method == 'POST':
            username = request.POST.get('uname')
            password =  request.POST.get('psw')
            post = Public_Detail.objects.filter(username=username,password=password,status='Verified')
            if post:
                username = request.POST.get('uname')
                request.session['public'] = username
                a = request.session['public']
                sess = Public_Detail.objects.only('id').get(username=a).id
                request.session['p_id']=sess
                return redirect("public_dashboard")
            else:
                messages.success(request, 'Invalid Username or Password Or Account Not Yet Verified..')
    return render(request,'public_login.html',{})
def public_dashboard(request):
    if request.session.has_key('public'):
        return render(request,'public_dashboard.html',{})
    else:
        return render(request,'public_login.html',{})
def public_logout(request):
    try:
        del request.session['public']
    except:
     pass
    return render(request, 'public_login.html', {})
def send_query(request):
    if request.session.has_key('public'):
        public_id = request.session['p_id']
        ids = Public_Detail.objects.get(id=int(public_id))
        a = Category_Detail.objects.all()
        if request.method == 'POST':
            area = request.POST.get('area')
            address = request.POST.get('addr')
            serv = request.POST.get('service')
            msg = request.POST.get('msg')
            video = request.FILES['video']
            service_id = Category_Detail.objects.get(id=int(serv))
            crt = Rise_Complaint.objects.create(
            public_id=ids,area=area,address=address,service_id=service_id,msg=msg,video=video,
            initial_status='Submitted',status='Pending')
            if crt:
                messages.success(request,'Your Compliant Has Been Filed.. We will Update You Soon Thanks !!!')
        return render(request,'send_query.html',{'a':a})
    else:
        return render(request,'public_login.html',{})
def manage_query(request):
    if request.session.has_key('public'):
        public_id = request.session['p_id']
        ids = Rise_Complaint.objects.filter(public_id=int(public_id))
        return render(request,'manage_query.html',{'ids':ids})
    else:
        return render(request,'public_login.html',{})
from django.db.models import Sum, Count
def admin_dashboard(request):
    tot = Rise_Complaint.objects.all().aggregate(Count('reference_id'))
    tot1 = Rise_Complaint.objects.filter(status='Pending').aggregate(Count('reference_id'))
    tot2 = Rise_Complaint.objects.filter(status='Progress').aggregate(Count('reference_id'))
    tot3 = Rise_Complaint.objects.filter(status='Completed').aggregate(Count('reference_id'))
    return render(request,'admin_dashboard.html',{'tot':tot,'tot1':tot1,'tot2':tot2,'tot3':tot3})
def view_complaint(request):
    cursor=connection.cursor()
    sql='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
    p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
    INNER JOIN app_public_detail as p ON r.public_id_id=p.id GROUP BY r.area, r.service_id_id '''
    res=cursor.execute(sql)
    row=cursor.fetchall()
    if request.method == 'POST':
        a=request.POST.get('search')
        sql1='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
        p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
        INNER JOIN app_public_detail as p ON r.public_id_id=p.id where r.reference_id='%d' GROUP BY r.area, r.service_id_id ''' % (int(a))
        res1=cursor.execute(sql1)
        detail=cursor.fetchall()
        return render(request,'view_complaints.html',{'row':row,'detail':detail})
    return render(request,'view_complaints.html',{'row':row})
def pending_complaint(request):
    a=request.GET.get('status')
    cursor=connection.cursor()
    sql='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
    p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
    INNER JOIN app_public_detail as p ON r.public_id_id=p.id where r.status='%s' GROUP BY r.area, r.service_id_id   ''' % (a)
    res=cursor.execute(sql)
    row=cursor.fetchall()
    return render(request,'view_complaints.html',{'row':row})
def update(request,pk,ids):
    if request.method=='POST':
        a=request.POST.get('status')
        row=Rise_Complaint.objects.filter(area__iexact=pk,service_id=ids).update(status=a)
        if row:
            messages.success(request,'All The Compliant Status Updated Successfully...')
            return render(request,'update.html',{})
    return render(request,'update.html',{})
def feedback(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        comment=request.POST.get('comment')
        row=Feedback.objects.create(name=name,email=email,mobile=mobile,comment=comment)
        if row:
            messages.success(request,'Thanks for your Valuable Feedback..')
    return render(request,'feedback.html',{})



from django.contrib.auth import authenticate,login as auth_login
def staff_login(request) :
    if request.method == 'POST' :
        staffid=request.POST.get('staffid')
        pass1=request.POST.get('psw')
        user=authenticate(username=staffid,password=pass1)
        if user is not None and user.is_staff == True:
            auth_login(request,user)
            if staffid == 'water@123' :
                messages.success(request,'You successfully login to our portal')
                return redirect('water_dashboard')
            if staffid == 'electricity@123' :
                messages.success(request,'You successfully login to our portal')
                return redirect('electricity_dashboard')
            elif staffid == 'drain@123' :
                messages.success(request,'You successfully login to our portal')
                return redirect('drain_dashboard')
        
        else :
            messages.info(request,'Invalid user credentials...')
            return redirect('staff_login')
    return render(request,'staff_login.html',{})

#-------------------WATER BOARD-----------------------------
def water_dashboard(request):
    tot = Rise_Complaint.objects.all().aggregate(Count('reference_id'))
    tot1 = Rise_Complaint.objects.filter(status='Pending').aggregate(Count('reference_id'))
    tot2 = Rise_Complaint.objects.filter(status='Progress').aggregate(Count('reference_id'))
    tot3 = Rise_Complaint.objects.filter(status='Completed').aggregate(Count('reference_id'))
    return render(request,'water_dashboard.html',{'tot':tot,'tot1':tot1,'tot2':tot2,'tot3':tot3})

def water_complaint(request):
    cursor=connection.cursor()
    sql='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
    p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
    INNER JOIN app_public_detail as p ON r.public_id_id=p.id where c.category_name='Water Complaint' or c.category_name='Drinking Water Contamination' or c.category_name='Water Leakage Repair' or c.category_name='Water Connection' GROUP BY r.area, r.service_id_id '''
    res=cursor.execute(sql)
    row=cursor.fetchall()
    if request.method == 'POST':
        a=request.POST.get('search')
        sql1='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
        p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
        INNER JOIN app_public_detail as p ON r.public_id_id=p.id where r.reference_id='%d'and c.category_name='Water Complaint' or c.category_name='Drinking Water Contamination' or c.category_name='Water Leakage Repair' or c.category_name='Water Connection' GROUP BY r.area, r.service_id_id ''' % (int(a))
        res1=cursor.execute(sql1)
        detail=cursor.fetchall()
        return render(request,'water_complaints.html',{'row':row,'detail':detail})
    return render(request,'water_complaints.html',{'row':row})

def water_update(request,pk,ids):
    if request.method=='POST':
        a=request.POST.get('status')
        row=Rise_Complaint.objects.filter(area__iexact=pk,service_id=ids).update(status=a)
        if row:
            messages.success(request,'All The Compliant Status Updated Successfully...')
            return render(request,'water_update.html',{})
    return render(request,'water_update.html',{})



    #-------------------eLECTRICITY BOARD-----------------------------
def electricity_dashboard(request):
    tot = Rise_Complaint.objects.all().aggregate(Count('reference_id'))
    tot1 = Rise_Complaint.objects.filter(status='Pending').aggregate(Count('reference_id'))
    tot2 = Rise_Complaint.objects.filter(status='Progress').aggregate(Count('reference_id'))
    tot3 = Rise_Complaint.objects.filter(status='Completed').aggregate(Count('reference_id'))
    return render(request,'electricity_dashboard.html',{'tot':tot,'tot1':tot1,'tot2':tot2,'tot3':tot3})

def electricity_complaint(request):
    cursor=connection.cursor()
    sql='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
    p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
    INNER JOIN app_public_detail as p ON r.public_id_id=p.id where c.category_name='Electricity' GROUP BY r.area, r.service_id_id '''
    res=cursor.execute(sql)
    row=cursor.fetchall()
    if request.method == 'POST':
        a=request.POST.get('search')
        sql1='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
        p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
        INNER JOIN app_public_detail as p ON r.public_id_id=p.id where r.reference_id='%d'and c.category_name='Electricity' GROUP BY r.area, r.service_id_id ''' % (int(a))
        res1=cursor.execute(sql1)
        detail=cursor.fetchall()
        return render(request,'electricity_complaints.html',{'row':row,'detail':detail})
    return render(request,'electricity_complaints.html',{'row':row})

def electricity_update(request,pk,ids):
    if request.method=='POST':
        a=request.POST.get('status')
        row=Rise_Complaint.objects.filter(area__iexact=pk,service_id=ids).update(status=a)
        if row:
            messages.success(request,'All The Compliant Status Updated Successfully...')
            return render(request,'electricity_update.html',{})
    return render(request,'electricity_update.html',{})

#=====================Drain================================

def drain_dashboard(request):
    tot = Rise_Complaint.objects.all().aggregate(Count('reference_id'))
    tot1 = Rise_Complaint.objects.filter(status='Pending').aggregate(Count('reference_id'))
    tot2 = Rise_Complaint.objects.filter(status='Progress').aggregate(Count('reference_id'))
    tot3 = Rise_Complaint.objects.filter(status='Completed').aggregate(Count('reference_id'))
    return render(request,'drain_dashboard.html',{'tot':tot,'tot1':tot1,'tot2':tot2,'tot3':tot3})

def drain_complaint(request):
    cursor=connection.cursor()
    sql='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
    p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
    INNER JOIN app_public_detail as p ON r.public_id_id=p.id where c.category_name='Drainage Problem' or c.category_name='Mosquito Minace' or c.category_name='Trash Related' GROUP BY r.area, r.service_id_id '''
    res=cursor.execute(sql)
    row=cursor.fetchall()
    if request.method == 'POST':
        a=request.POST.get('search')
        sql1='''SELECT r.reference_id,r.area,r.address,c.category_name,r.msg,r.date,r.video,p.username,p.email,
        p.phone_number,r.status,r.initial_status,c.id from app_category_detail as c INNER JOIN app_rise_complaint as r ON c.id=r.service_id_id
        INNER JOIN app_public_detail as p ON r.public_id_id=p.id where r.reference_id='%d'and c.category_name='Drainage Problem' or c.category_name='Mosquito Minace' or c.category_name='Trash Related' GROUP BY r.area, r.service_id_id ''' % (int(a))
        res1=cursor.execute(sql1)
        detail=cursor.fetchall()
        return render(request,'drain_complaints.html',{'row':row,'detail':detail})
    return render(request,'drain_complaints.html',{'row':row})

def drain_update(request,pk,ids):
    if request.method=='POST':
        a=request.POST.get('status')
        row=Rise_Complaint.objects.filter(area__iexact=pk,service_id=ids).update(status=a)
        if row:
            messages.success(request,'All The Compliant Status Updated Successfully...')
            return render(request,'drain_update.html',{})
    return render(request,'drain_update.html',{})
