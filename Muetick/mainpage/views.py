from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer,AdminUser,Ticket,Categories,feedback,lostandfound,TicketInfo_telegram,LostAndFound_telegram,ReportFound_telegram,Feedback_telegram
import random
import datetime

def dashboard(request):
    if 'email' in request.session:
        context={'name':request.session['email']}
        if '@admin' in request.session['email']:
            return redirect('adminpage')
        return render(request,"mainpage/dashboard.html",context)
    return redirect('signin')



def catpage(request,mname):
    #eg1 - 10 - Egyptian-gallery
    #gg1 - 15 - Gandhara-gallery
    #lag1 - 20 - Long-archaeology-gallery
    #mag1 - 25 - Minor-art-gallery
    #vf1 - 30 - Varanda-floor
    context={}
    imgpic={'Egyptian-gallery':'mainpage/Egyptian_Gallery_View2.jpg','Gandhara-gallery':'mainpage/Gandhara_Gallery_View1.jpg','Long-archaeology-gallery':'mainpage/LongArchaeology_Gallery_View1.jpg','Minor-art-gallery':'mainpage/This-Minor_Art_GalleryView2.jpg','Varanda-floor':'mainpage/Varanda_1st_floor.jpg'}
    layoutpic={'Egyptian-gallery':'mainpage/Haven_minimap.png','Gandhara-gallery':'mainpage/Ascent_minimap.png','Long-archaeology-gallery':'mainpage/Split_minimap.png','Minor-art-gallery':'mainpage/Lotus_minimap.png','Varanda-floor':'mainpage/Sunset_minimap.png'}
    if 'email' in request.session:
        if request.method=="POST":
            try:
                price=int(request.POST['price'][:-2])
                tickets=int(request.POST['ticketcount'])
            except Exception as e:  
                print(e)
                return redirect('dashboard')
            museum=Categories.objects.filter(name=mname)[0]
            if museum.tickets<tickets:
                context['error']="We're sorry but we do not have that many tickets right now!"
            else:
                museum.tickets-=tickets
                museum.save()
                discount=0
                if tickets>99:
                    discount=0.1*(tickets)
                discount=min(25,discount)
                new_ticket=Ticket.objects.create(
                                tic_id="".join([str(random.randint(1,9)) for x in range(10)]),
                                cusname=Customer.objects.filter(email=request.session['email'])[0],
                                catname=museum,
                                totalcost=int(tickets*museum.price*(1-(discount/100))),
                                trxtime=datetime.datetime.today(),
                                count=tickets,
                            )
                return redirect('profile')
        museum=Categories.objects.filter(name=mname)
        if len(museum)<1:
            return redirect('dashboard')

        context['name']=request.session['email']
        context['m_name']=museum[0].name
        context['price']=museum[0].price
        context['layout']=layoutpic[museum[0].name]
        context['imgbig']=imgpic[museum[0].name]
        context['avail']=museum[0].tickets
        return render(request,"mainpage/catpage.html",context=context)
    return redirect('signin')


def editprofile(request):
    if 'email' in request.session:
        context={'name':request.session['email']}
        if request.method=="POST":
            name=request.POST['name']
            phno=request.POST['phno']
            user=Customer.objects.filter(email=request.session['email'])[0]
            if name!="":
                user.name=name
            if phno!="":
                if len(phno)==10 and  phno.isdigit():
                    user.phno=phno
            user.save()
            return redirect('profile')
        return render(request,"mainpage/edit-profile.html",context)
    return redirect('signin')

def profile(request):
    if 'email' in request.session:
        if '@admin' in request.session['email']:
            return redirect('adminpage')
        cus=Customer.objects.filter(email=request.session['email'])[0]
        if request.method=="POST":
            if request.POST['typeofform']=="l":
                desc=request.POST['desc_lnf']
                museum=request.POST['museum_lnf']
                lnfnew=lostandfound.objects.create(lnf_id="".join([str(random.randint(1,9)) for x in range(10)]),
                                                   cus=cus,
                                                   museum=Categories.objects.filter(name=museum)[0],
                                                   desc=desc
                                                   )
            else:
                desc=request.POST['desc_f']
                museum=request.POST['museum_f']
                fnew=feedback.objects.create(f_id="".join([str(random.randint(1,9)) for x in range(10)]),
                                                   cus=cus,
                                                   museum=Categories.objects.filter(name=museum)[0],
                                                   desc=desc
                                                   )
            return redirect('profile')
        context={'name':request.session['email']}
        
        trxns=Ticket.objects.filter(cusname=cus)
        context['name']=cus.name
        context['email']=cus.email
        context['phno']=cus.phno
        context['trxns']=trxns
        context['lostandfound']=lostandfound.objects.filter(cus=cus)
        context['feedback']=feedback.objects.filter(cus=cus)
        return render(request,"mainpage/profile.html",context=context)
    return redirect('signin')

def signin(request):
    context={"error":"",'name':"Log-In"}
    if request.method=="POST":
        error=""
        email=request.POST['email']
        password=request.POST['password']
        if "@admin" in email:
            user=AdminUser.objects.filter(userid=email)
        else:
            user = Customer.objects.filter(email=email)
        if len(user)<1:
            error="User doesn't exist"
        elif user[0].password!=password:
            error="Incorrect password!"
        context['error']=error
        if error:
            return render(request,"mainpage/Sign_In.html",context)
        else:
            request.session['email']=email
            request.session.modified=True
            request.session.set_expiry(600)
            return redirect("dashboard")
    return render(request,"mainpage/Sign_In.html",context)

def signup(request):
    context={"error":"","name":"Sign-Up"}
    if request.method=="POST":
        error=""
        name=request.POST['name']
        email=request.POST['email']
        phno=request.POST['mobile']
        password=request.POST['password']
        confpassword=request.POST['confirm-password']
        if len(phno)!=10 or not phno.isdigit():
            error+="Phone number must be atleast 10 digits, and must only contain numbers. "
        if len(password)<7:
            error+="Password must atleast be 7 characters in length. "
        if password!=confpassword:
            error+="Passwords don't match."
        users = Customer.objects.filter(email=email)
        if len(users)>0:
            error+="This email already exists. Sign-in instead. "
        context['error']=error
        if error:
            return render(request,"mainpage/Sign_Up.html",context)
        else:
            new_customer=Customer.objects.create(
                        cus_id="".join([str(random.randint(1,9)) for x in range(10)]),
                        name=name,
                        email=email,
                        phno=phno,
                        password=password
                    )
            return redirect("/signin")
            
    return render(request,"mainpage/Sign_Up.html",context)


def adminpage(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email']}
            context['ticketssold']=len(Ticket.objects.filter(trxtime=datetime.datetime.today()))
            context['cashinflow']=sum([x.totalcost for x in Ticket.objects.filter(trxtime=datetime.datetime.today())])
            context['totalaccounts']=len(Customer.objects.all())
            try:
                context['eg']=sum([x.count for x in Ticket.objects.filter(trxtime=datetime.datetime.today(),catname=Categories.objects.filter(cat_id="0000000001")[0])])
            except:
                return redirect('quicksetup')
            context['gg']=sum([x.count for x in Ticket.objects.filter(trxtime=datetime.datetime.today(),catname=Categories.objects.filter(cat_id="0000000002")[0])])
            context['lag']=sum([x.count for x in Ticket.objects.filter(trxtime=datetime.datetime.today(),catname=Categories.objects.filter(cat_id="0000000003")[0])])
            context['mag']=sum([x.count for x in Ticket.objects.filter(trxtime=datetime.datetime.today(),catname=Categories.objects.filter(cat_id="0000000004")[0])])
            context['vf']=sum([x.count for x in Ticket.objects.filter(trxtime=datetime.datetime.today(),catname=Categories.objects.filter(cat_id="0000000005")[0])])
            context['egu']=(Categories.objects.filter(cat_id="0000000001")[0].tickets) + context['eg']
            context['ggu']=(Categories.objects.filter(cat_id="0000000002")[0].tickets) + context['gg']
            context['lagu']=(Categories.objects.filter(cat_id="0000000003")[0].tickets) + context['lag']
            context['magu']=(Categories.objects.filter(cat_id="0000000004")[0].tickets) + context['mag']
            context['vfu']=(Categories.objects.filter(cat_id="0000000005")[0].tickets) + context['vf']
            return render(request,"mainpage/adminpage.html",context=context)
    return redirect('signin')

def dev(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email']}
            return render(request,"mainpage/dev.html",context)
    return redirect('signin')

def transactions(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email']}
            trxns=Ticket.objects.all()
            context['trxns']=trxns
            tele_trxns=TicketInfo_telegram.objects.all()
            context['tele_trxns']=tele_trxns
            return render(request,"mainpage/transactions.html",context=context)
    return redirect('signin')

def lostitems(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email']}
            litems=lostandfound.objects.all()
            context['litems']=litems
            tele_litems=LostAndFound_telegram.objects.all()
            context['tele_litems']=tele_litems
            tele_fitems=ReportFound_telegram.objects.all()
            context['tele_fitems']=tele_fitems
            return render(request,"mainpage/lostitems.html",context=context)
    return redirect('signin')

def feedback_page(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email']}
            feedback_entries=feedback.objects.all()
            context['feedback']=feedback_entries
            tele_feedback=Feedback_telegram.objects.all()
            context['tele_feedback']=tele_feedback
            return render(request,"mainpage/feedback.html",context=context)
    return redirect('signin')

def scan(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            context={'name':request.session['email'],'error':""}
            if request.method=="POST":
                tickid=request.POST['ticketid']
                ticket=Ticket.objects.filter(tic_id=tickid)
                if len(ticket)<1:
                    context['error']="Invalid ticket id!"
                else:
                    ticket=ticket[0]
                    if ticket.checked:
                        context['error']="This ticket has already been used!"
                    else:
                        ticket.checked=not ticket.checked
                        cat=ticket.catname
                        cat.tickets+=ticket.count
                        ticket.save()
                        cat.save()
                        context['error']="Scanning successful!"
            return render(request,"mainpage/scan.html",context=context)
    return redirect('signin')

def quicksetup(request):
    if 'email' in request.session:
        if "@admin" in request.session['email']:
            if len(Categories.objects.filter(cat_id="0000000001"))<1:
                Categories.objects.create(cat_id="0000000001",name="Egyptian-gallery",price=10,tickets=1000)
            if len(Categories.objects.filter(cat_id="0000000002"))<1:
                Categories.objects.create(cat_id="0000000002",name="Gandhara-gallery",price=15,tickets=1000)
            if len(Categories.objects.filter(cat_id="0000000003"))<1:
                Categories.objects.create(cat_id="0000000003",name="Long-archaeology-gallery",price=20,tickets=1000)
            if len(Categories.objects.filter(cat_id="0000000004"))<1:
                Categories.objects.create(cat_id="0000000004",name="Minor-art-gallery",price=25,tickets=1000)
            if len(Categories.objects.filter(cat_id="0000000005"))<1:
                Categories.objects.create(cat_id="0000000005",name="Veranda-floor",price=30,tickets=1000)
    return redirect('adminpage')

def logout(request):
    request.session.clear()
    request.session.flush()
    request.session.modified=True
    return redirect('signin')

def landingpage(request):
    request.session.clear()
    request.session.flush()
    request.session.modified=True
    return render(request,"mainpage/landing_page.html")