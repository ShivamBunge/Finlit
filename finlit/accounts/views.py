
from django.http.response import HttpResponse
from profession.models import Profession
from django.contrib.messages.api import error
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, portfolio

# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        elif user is super:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")


def register(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect("login")
        else:
            messages.info(request, "Password not matching.")
            return redirect("register")
    else:
        return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')


def start(request):
    if (request.user.is_authenticated):
        profs = Profession.objects.all()
        return render(request, "pg0.html", {'profs': profs})
    else:
        return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("/")

# def advice(request):
    # return render(request, "advice.html")

def prof_ch(request):
    member = Profile.objects.get(user__id=request.user.id)
    prtf = portfolio.objects.get(player__id=request.user.id)  # prtf line
    if request.method == "POST":
        choice = request.POST['select']
        member.current_job = choice
        member.save()

        prtf.stocks = 0
        prtf.mutual_funds = 0
        prtf.fds = 0
        prtf.gold = 0
        prtf.loans = 0

        prtf.total_prtf_val = int(prtf.stocks)+int(prtf.mutual_funds)+int(prtf.fds)+int(prtf.gold)
            
        prtf.save()

        if choice == "Doctor":
            member.prof = Profession.objects.get(prof_name=choice)
            # member.prof.income=200000
            member.save()
            # Previous position of prtf line
            prtf.balance = member.prof.income - member.prof.expend
            prtf.pg_no = 1
            prtf.save()
            # Previous position of prtf changes and save
            return render(request, "pg1-dr.html", {"prtf": prtf, "member": member.prof})
        elif choice == "Businessman":
            member.prof = Profession.objects.get(prof_name=choice)
            member.save()
            prtf.balance = member.prof.income - member.prof.expend
            prtf.pg_no = 1
            prtf.save()
            return render(request, "pg1-busi.html")
        elif choice == "Engineer":
            member.prof = Profession.objects.get(prof_name=choice)
            member.save()
            prtf.balance = member.prof.income - member.prof.expend
            prtf.pg_no = 1
            prtf.save()
            return render(request, "pg1-eng.html")
        elif choice == "Police":
            member.prof = Profession.objects.get(prof_name=choice)
            member.save()
            prtf.balance = member.prof.income - member.prof.expend
            prtf.pg_no = 1
            prtf.save()
            return render(request, "pg1-pol.html")
    # elif request.method=="GET":
    #     return
    else:
        return redirect("start")

# ----------------All here is for testing-------------------------------------




# ------------------------------------------------------------------------------


def withdraw(request):
    prtf = portfolio.objects.get(player__id=request.user.id)
    return render(request, "withdraw.html", {"prtf": prtf})


def confirm_wd(request):
    member = Profile.objects.get(user__id=request.user.id)
    prtf = portfolio.objects.get(player__id=request.user.id)
    # print(prtf.balance)
    stck = request.POST["stocks"]
    mf = request.POST["mutual_funds"]
    fd = request.POST["fds"]
    gold = request.POST["gold"]

    prtf.balance += int(stck)+int(mf)+int(fd)+int(gold)

    prtf.stocks -= int(stck)
    prtf.mutual_funds -= int(mf)
    prtf.fds -= int(fd)
    prtf.gold -= int(gold)
    prtf.save()
    # return render(request,"pg2.html",{"prtf":prtf,"member":member.prof})
    # return redirect(request.META.get('HTTP_REFERER'))
    if prtf.pg_no == 2:
        return render(request, "pg2.html", {"prtf": prtf, "member": member.prof})
    elif prtf.pg_no==3:
        return render(request,"pg3.html",{"prtf":prtf,"member":member.prof})
    elif prtf.pg_no==4:
        return render(request,"pg4.html",{"prtf":prtf,"member":member.prof})
    elif prtf.pg_no==5:
        return render(request,"pg5.html",{"prtf":prtf,"member":member.prof})
    elif prtf.pg_no==6:
        return render(request,"pg6.html",{"prtf":prtf,"member":member.prof})

def invest(request):

    prtf=portfolio.objects.get(player__id=request.user.id)
    if prtf.pg_no==2:
        car_status = request.POST["car"]
        if car_status == "loan":
            prtf.loans=210000
            prtf.balance -=prtf.loans
            prtf.save()
        elif car_status == "savings":
            prtf.balance -= 600000
            prtf.save()
    return render(request,"invest.html",{"prtf":prtf})

# --------individual income and expend (global)------------
inc=0
exp=0

percent=[0,0]

def confirm_inv(request):
    global inc, exp
    member = Profile.objects.get(user__id=request.user.id)
    prtf=portfolio.objects.get(player__id=request.user.id)
    # print(prtf.balance)

    stck=request.POST["stocks"]
    mf=request.POST["mutual_funds"]
    fd=request.POST["fds"]
    gold=request.POST["gold"]

    if int(stck)+int(mf)+int(fd)+int(gold) == 0:
        return redirect(request.META.get('HTTP_REFERER'))
    
    # if prtf.pg_no==0:
    #     return redirect(request.META.get('HTTP_REFERER'))
    if prtf.pg_no==1:

        # if stck+mf+fd+gold !=0:
        prtf.balance += member.prof.income * 12
        prtf.balance -= member.prof.expend * 12

        prtf.balance -= int(stck)+int(mf)+int(fd)+int(gold)
        prtf.balance -= 80000 #tax

        prtf.stocks += int(stck)
        prtf.mutual_funds += int(mf)
        prtf.fds += int(fd)
        prtf.gold += int(gold)

        prtf.stocks += (prtf.stocks*0.15)
        prtf.mutual_funds += (prtf.mutual_funds*0.20)
        prtf.fds += (prtf.fds*0.005)
        prtf.gold += (prtf.gold*0.003)

        if member.prof.progress==1:
            member.prof.income += (member.prof.income*0.05)
            inc= member.prof.income
            percent[0]=5
        elif member.prof.progress==2:
            member.prof.income += (member.prof.income*0.1)
            inc= member.prof.income
            percent[0]=10
        elif member.prof.progress==3:
            member.prof.income += (member.prof.income*0.15)
            inc= member.prof.income
            percent[0]=15
        

        prtf.total_prtf_val = prtf.stocks + prtf.mutual_funds + prtf.fds + prtf.gold

        prtf.pg_no = 2
        prtf.save()
        return render(request,"pg2.html",{"prtf":prtf,"member":member.prof,"percent":percent})
    elif prtf.pg_no==2:
        member.prof.income = inc
        print(member.prof.income)
        prtf.balance += member.prof.income * 12
        prtf.balance -= member.prof.expend * 12

        prtf.balance -= int(stck)+int(mf)+int(fd)+int(gold)
        prtf.balance -= 150000   #grandfather hospital expenses
        prtf.balance -=65000    #house renovate
        prtf.balance -= 80000 #tax
        
        #----------Monthly saving----------------
        mon_save=0
        mon_save=member.prof.income * 12
        mon_save -=member.prof.expend *12
        mon_save -= 150000   #grandfather hospital expenses
        mon_save -=65000    #house renovate
        mon_save -= 80000   #tax
        mon_save_list = [mon_save//12]
        # -----------------------------------------
        prtf.stocks += int(stck)
        prtf.mutual_funds += int(mf)
        prtf.fds += int(fd)
        prtf.gold += int(gold)

        prtf.stocks += (prtf.stocks*0.20)
        prtf.mutual_funds += (prtf.mutual_funds*0.25)
        prtf.fds += (prtf.fds*0.006)
        prtf.gold += (prtf.gold*0.003)
        if member.prof.progress==1:
            member.prof.income += (member.prof.income*0.05)
            member.prof.expend += (member.prof.expend*0.02)
            inc= member.prof.income
            percent[0]=5
            percent[1]=2
            exp=member.prof.expend
        elif member.prof.progress==2:
            member.prof.income += (member.prof.income*0.1)
            member.prof.expend += (member.prof.expend*0.04)
            inc= member.prof.income
            percent[0]=10
            percent[1]=4
            exp=member.prof.expend
        elif member.prof.progress==3:
            member.prof.income += (member.prof.income*0.15)
            member.prof.expend += (member.prof.expend*0.06)
            inc= member.prof.income
            percent[0]=15
            percent[1]=6
            exp=member.prof.expend

        prtf.total_prtf_val = prtf.stocks + prtf.mutual_funds + prtf.fds + prtf.gold

        prtf.pg_no=3

        prtf.save()
        return render(request,"pg3.html",{"prtf":prtf,"member":member.prof,"mon_save":mon_save_list,"percent":percent})
    elif prtf.pg_no==3:
        member.prof.income = inc
        member.prof.expend = exp

        prtf.balance += member.prof.income * 12
        prtf.balance -= member.prof.expend * 12

        prtf.balance -= int(stck)+int(mf)+int(fd)+int(gold)
        prtf.balance -= 120000 # wedding
        prtf.balance -= 80000 #tax
        prtf.balance -= prtf.loans #loans

        #----------Monthly saving----------------
        mon_save=0
        mon_save=member.prof.income * 12
        mon_save -=member.prof.expend *12
        mon_save -= 120000   #wedding
        mon_save -= 80000   #tax
        mon_save_list = [mon_save//12]
        # -----------------------------------------

        prtf.stocks += int(stck)
        prtf.mutual_funds += int(mf)
        prtf.fds += int(fd)
        prtf.gold += int(gold)

        prtf.stocks -= (prtf.stocks*0.14)
        prtf.mutual_funds -= (prtf.mutual_funds*0.10)
        prtf.fds += (prtf.fds*0.0045)
        prtf.gold += (prtf.gold*0.0027)
        if member.prof.progress==1:
            member.prof.income += (member.prof.income*0.06)
            member.prof.expend += (member.prof.expend*0.03)
            inc= member.prof.income
            percent[0]=6
            percent[1]=3
            exp=member.prof.expend
        elif member.prof.progress==2:
            member.prof.income += (member.prof.income*0.12)
            member.prof.expend += (member.prof.expend*0.05)
            inc= member.prof.income
            percent[0]=12
            percent[1]=5
            exp=member.prof.expend
        elif member.prof.progress==3:
            member.prof.income += (member.prof.income*0.16)
            member.prof.expend += (member.prof.expend*0.07)
            inc= member.prof.income
            percent[0]=16
            percent[1]=7
            exp=member.prof.expend


        prtf.total_prtf_val = prtf.stocks + prtf.mutual_funds + prtf.fds + prtf.gold
        networth= [prtf.balance + prtf. total_prtf_val]
        prtf.pg_no = 4
        prtf.save()
        return render(request,"pg4.html",{"prtf":prtf,"member":member.prof,"nw":networth,"mon_save":mon_save_list,"percent":percent})
    elif prtf.pg_no==4:
        member.prof.income = inc 
        member.prof.expend = exp

        prtf.balance += member.prof.income * 12
        prtf.balance -= member.prof.expend * 12

        prtf.balance -= int(stck)+int(mf)+int(fd)+int(gold)
        prtf.balance -= 80000 #tax
        prtf.balance -= prtf.loans #loans

        #----------Monthly saving----------------
        mon_save=0
        mon_save=member.prof.income * 12
        mon_save -=member.prof.expend *12
        mon_save -= 80000   #tax
        mon_save_list = [mon_save//12]
        # -----------------------------------------

        prtf.stocks += int(stck)
        prtf.mutual_funds += int(mf)
        prtf.fds += int(fd)
        prtf.gold += int(gold)

        prtf.stocks -= (prtf.stocks*0.25)
        prtf.mutual_funds -= (prtf.mutual_funds*0.27)
        prtf.fds += (prtf.fds*0.035)
        prtf.gold += (prtf.gold*0.05)
        if member.prof.progress==1:
            member.prof.income += (member.prof.income*0.04)
            member.prof.expend += (member.prof.expend*0.03)
            inc= member.prof.income
            percent[0]=4
            percent[1]=3
            exp=member.prof.expend
        elif member.prof.progress==2:
            member.prof.income += (member.prof.income*0.14)
            member.prof.expend += (member.prof.expend*0.06)
            inc= member.prof.income
            percent[0]=14
            percent[1]=6
            exp=member.prof.expend
        elif member.prof.progress==3:
            member.prof.income += (member.prof.income*0.18)
            member.prof.expend += (member.prof.expend*0.08)
            inc= member.prof.income
            percent[0]=18
            percent[1]=8
            exp=member.prof.expend
        

        prtf.total_prtf_val = prtf.stocks + prtf.mutual_funds + prtf.fds + prtf.gold
        prtf.pg_no = 5
        prtf.save()
        return render(request,"pg5.html",{"prtf":prtf,"member":member.prof,"mon_save":mon_save_list,"percent":percent})
    elif prtf.pg_no==5:
        member.prof.income =inc
        member.prof.expend =exp

        prtf.balance += member.prof.income * 12
        prtf.balance -= member.prof.expend * 12

        prtf.balance -= int(stck)+int(mf)+int(fd)+int(gold)
        prtf.balance -= 90000 #tax
        prtf.balance -= prtf.loans #loans

        #----------Monthly saving----------------
        mon_save=0
        mon_save=member.prof.income * 12
        mon_save -=member.prof.expend *12
        mon_save -= 90000   #tax
        mon_save_list = [mon_save//12]
        # -----------------------------------------

        prtf.stocks += int(stck)
        prtf.mutual_funds += int(mf)
        prtf.fds += int(fd)
        prtf.gold += int(gold)

        prtf.stocks += (prtf.stocks*0.37)
        prtf.mutual_funds += (prtf.mutual_funds*0.29)
        prtf.fds += (prtf.fds*0.05)
        prtf.gold += (prtf.gold*0.01)
        if member.prof.progress==1:
            member.prof.income += (member.prof.income*0.06)
            inc= member.prof.income
            percent[0]=6
        elif member.prof.progress==2:
            member.prof.income += (member.prof.income*0.1)
            inc= member.prof.income
            percent[0]=10
        elif member.prof.progress==3:
            member.prof.income += (member.prof.income*0.12)
           
            inc= member.prof.income
            percent[0]=12
       
       
 
        prtf.total_prtf_val = prtf.stocks + prtf.mutual_funds + prtf.fds + prtf.gold
        prtf.pg_no = 6
        prtf.save()
        return render(request,"pg6.html",{"prtf":prtf,"member":member.prof,"mon_save":mon_save_list,"percent":percent})
    elif prtf.pg_no==6:
        networth= [prtf.balance + prtf. total_prtf_val]
        return render(request,"last.html",{"prtf":prtf,"nw":networth,"member":member.prof})


def about(request):
    return render(request,"about_us.html")