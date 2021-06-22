from service.models import Organization, OrganizationObject
from main.service import get_homes
from location.models import City, Country, Object, Street
from users.models import Account, CustomUser, Faktura
from django.shortcuts import render,redirect
import random, string, openpyxl
from django.contrib import messages
from .forms import OwnerForm, ProfileImageForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.core.paginator import Paginator
from domok.settings import EMAIL_FROM
from django.core.mail import EmailMultiAlternatives
from .services import get_years
from django.contrib.auth.decorators import login_required

def set_password(request,pk):
    letters = string.ascii_letters
    digits = string.digits
    digits2 = string.digits
    password = ''.join(random.choice(digits) for i in range(3))
    password+=''.join(random.choice(letters) for i in range(5))
    password+=''.join(random.choice(digits2) for i in range(3))
    user = CustomUser.objects.get(id=pk)
    user.set_password(password)
    user.save()

    subject, from_email, to = 'info', 'EMAIL_FROM', user.email
    text_content = 'This is an important message.'
    html_content = "<html>"\
            +"<body>"\
            +"Здравствуйте, "+user.last_name+" "+user.first_name +"!<br>"\
            +"Ваш пароль для доступа на сайт ДомОК был изменен.<br>"\
            +'Для авторизации на сайте перейдите по адресу: <a href="http://'+request.get_host()+'">'+request.get_host()+"</a><br><br>"\
            +"Логин: <b>"+user.username+"</b><br>"\
            +"Пароль: <b>"+password+"</b><br><br>"\
            +"С уважением, администрация сайта ДомОК."\
            +"</body>"\
            +"</html>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/'+request.GET.get('type')+'/'+pk+"/change/?pch=True")

def upload_account(request):
    if request.method == "POST":
        if request.FILES:
            excel_file = request.FILES['myfile']
            if not excel_file.name.endswith('xlsx'):
                messages.error(request, "Неправильный формат.")
                return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/?wf=True')
            wb = openpyxl.load_workbook(excel_file)
            sheetname = str(wb.sheetnames[0])
            try:
                worksheet = wb[sheetname]
            except:
                messages.error(request, "file format or excel sheet name is incorrect.")
                return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/?wf=True')
            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value).strip())
                excel_data.append(row_data)
            error_rows = []
            for row in excel_data[1:]:
                try:
                    Account.objects.get(account=row[0])
                except:
                    try:
                        city = City.objects.get(name = row[2])
                        try:
                            street = Street.objects.get(city_id=city.id,name=row[3])
                        except:
                            street = Street(city_id=city.id, name=row[3])
                            street.save()
                        try:
                            object = Object.objects.get(street_id=street.id,
                                                        home=row[4],
                                                        campus= None if row[5] =="" or row[5] =="None" else row[5],
                                                        appartment_number= None if row[6] =="" or row[6] =="None" else row[6]
                                                        )
                        except:
                            object = Object(street_id=street.id,
                                                        home=row[4],
                                                        campus= None if row[5] =="" or row[5] =="None" else row[5],
                                                        appartment_number=  None if row[6] =="" or row[6] =="None" else row[6]
                                                        )
                            object.save()
                        try:
                            organization = Organization.objects.get(name=row[10])
                            OrganizationObject(organization_id = organization.id,object_id = object.id).save()
                        except:
                            pass
                        account = Account()
                        account.account = row[0]
                        account.name =  row[1]
                        account.total_square = 0 if row[7] =="" or row[7] =="None" else float(row[7])
                        account.living_square =  0 if row[8] =="" or row[8] =="None" else  float(row[8])
                        account.share =  0 if row[9] =="" or row[9] =="None" else float(row[9])
                        account.object_id=object.id
                        account.save()
                    except:
                        error_rows.append(row[0])
            if len(error_rows)==0:
                messages.info(request, "Счета успешно сохранены.")
            else:
                rows = ""
                for row in error_rows:
                    rows += " "+row+","
                messages.warning(request, "Есть строки, которые не были импортированы. Строки "+rows)
            return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/')
        else:
            messages.error(request, "Нет файла.")
            return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/')

def upload_fakturas(request):
    accounts = Account.objects.all()
    post = request.POST
    year = post['year']
    month = post['month']
    excel_file = request.FILES['file']
    if not excel_file.name.endswith('xlsx'):
        messages.error(request, "Формат файла должен быть xlsx.")
        return redirect("{0}://{1}".format('http', request.get_host()) + "/admin/users/faktura/")
    wb = openpyxl.load_workbook(excel_file)
    new_sheets = []
    for index, sheet in enumerate(wb.worksheets):
        if index%2==0:
            cell_value = sheet.cell(row=1, column=1).value
            start_index = cell_value.index("Лицевой счет : ")+15
            end_index = cell_value.index("(",start_index)
            first_sheet = wb.worksheets[index]
            second_sheet =  wb.worksheets[index+1]
            new_sheets.append({
                0:first_sheet,
                1:second_sheet,
                2:cell_value[start_index:end_index].strip()
            })
    for sheet in wb.worksheets:
        wb.remove(sheet)
    for nsh in new_sheets:
        first_worksheet = wb.copy_worksheet(nsh[0])
        first_worksheet.title = "Страница 1"
        second_worksheet = wb.copy_worksheet(nsh[1])
        second_worksheet.title = "Страница 2"
        wb.save('media/fakturas/'+year+"_"+month+"_"+nsh[2]+".xlsx")
        for sheet in wb.worksheets:
            wb.remove(sheet)
        faktura = Faktura(file='fakturas/'+year+"_"+month+"_"+nsh[2]+".xlsx",created_by_id=request.user.id,year=year,month=month,account_name=nsh[2])
        if accounts.filter(account=nsh[2]).count()>0:
            faktura.account = accounts.filter(account=nsh[2]).first()
        faktura.save()
    messages.success(request, "Файл успешно загружен.")
    return redirect("{0}://{1}".format('http', request.get_host()) + "/admin/users/faktura/")

@login_required(login_url="/accounts/login/")
def contacts(request):
    organization_workers = CustomUser.objects.filter(
        worker_organizations__organization__organization_objects__object_id = request.session.get('current_object')).exclude(id=request.user.id)
    moderators = CustomUser.objects.filter(custom_user_account__object_id = request.session.get('current_object')).exclude(id=request.user.id)
    homes = get_homes(request)
    context = {"organization_workers":organization_workers,'moderators':moderators,
                "homes":homes['homes'], "current":homes['current']}
    return render(request,'contacts/contacts.html',context)

@login_required(login_url="/accounts/login/")
def account(request):
    fakturas = Faktura.objects.filter(account__object_id = request.session.get('current_object'))
    name = request.GET.get('name','')
    account_filter = request.GET.get('account','')
    appartment_number = request.GET.get('appartment_number',"")
    year = request.GET.get('year',None)
    month = request.GET.get('month',None)
    if name is not None:
        fakturas = fakturas.filter(Q(account__custom_user__first_name__icontains = name) | 
                                Q(account__custom_user__last_name__icontains = name) |
                                Q(account__custom_user__middle_name__icontains = name))
    if account_filter is not None:
        fakturas = fakturas.filter(account__account__icontains = account_filter)
    if appartment_number is not None:
        fakturas = fakturas.filter(account__object__appartment_number__icontains = appartment_number)
    if year is not None and year != "":
        year = int(year)
        fakturas = fakturas.filter(year = year)
    if month is not None and month != "":
        month = int(month)
        fakturas = fakturas.filter(month = month)
    years = "<select name='year' class='form-control'>"\
                +"<option value=''>Выберите год</option>"    
    for item in get_years():
        if year == item[0]:
            years+="<option value='"+str(item[0])+"' selected>"+str(item[0])+"</option>"
        else:
            years+="<option value='"+str(item[0])+"'>"+str(item[0])+"</option>"
    years+= "</select>"
    paginator = Paginator(fakturas.distinct(), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'], "fakturas":page_obj,"years":years,"filters":{
                                    "name":name,
                                    "year":year,
                                    "account":account_filter,
                                    "appartment_number":appartment_number,
                                    "month":month,
                                }}
    return render(request,'accounts/accounts.html', context)

@login_required(login_url="/accounts/login/")
def upload_faktura(request):
    if request.user.role != "moderator":
        return redirect('users:account')
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    if request.method == 'POST':
        accounts = Account.objects.all()
        post = request.POST
        year = post['year']
        month = post['month']
        excel_file = request.FILES['file']
        if not excel_file.name.endswith('xlsx'):
            context['errors'] = "Формат файла должен быть xlsx."
            return render(request,'accounts/upload-faktura.html', context)
        wb = openpyxl.load_workbook(excel_file)
        new_sheets = []
        for index, sheet in enumerate(wb.worksheets):
            if index%2==0:
                cell_value = sheet.cell(row=1, column=1).value
                start_index = cell_value.index("Лицевой счет : ")+15
                end_index = cell_value.index("(",start_index)
                first_sheet = wb.worksheets[index]
                second_sheet =  wb.worksheets[index+1]
                new_sheets.append({
                    0:first_sheet,
                    1:second_sheet,
                    2:cell_value[start_index:end_index].strip()
                })
        for sheet in wb.worksheets:
            wb.remove(sheet)
        for nsh in new_sheets:
            first_worksheet = wb.copy_worksheet(nsh[0])
            first_worksheet.title = "Страница 1"
            second_worksheet = wb.copy_worksheet(nsh[1])
            second_worksheet.title = "Страница 2"
            wb.save('media/fakturas/'+year+"_"+month+"_"+nsh[2]+".xlsx")
            for sheet in wb.worksheets:
                wb.remove(sheet)
            faktura = Faktura(file='fakturas/'+year+"_"+month+"_"+nsh[2]+".xlsx",created_by_id=request.user.id,year=year,month=month,account_name=nsh[2])
            if accounts.filter(account=nsh[2]).count()>0:
                faktura.account = accounts.filter(account=nsh[2]).first()
            faktura.save()
        return redirect("users:account")
    
    return render(request,'accounts/upload-faktura.html', context)

def upload(request):
    if request.method == 'POST':
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user)   
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(request.user.image.url)

@login_required(login_url="/accounts/login/")
def profile(request):
    custom_user = CustomUser.objects.get(id = request.user.id)
    image_form = ProfileImageForm(instance=custom_user)    
    profile_form = ProfileForm(instance=custom_user)
    initial = {
            "username":custom_user.username
        }
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,initial=initial, instance=custom_user)   
        if profile_form.is_valid():
            if profile_form.cleaned_data['password1'] is not None and profile_form.cleaned_data['password1']!="":
                custom_user.set_password(profile_form.cleaned_data['password1'])
            user = profile_form.save()
            update_session_auth_hash(request, user)
        else:
            profile_form.errors
    else:
        profile_form = ProfileForm(initial=initial,instance=custom_user) 
    homes = get_homes(request)
    context = {
        'image_form': image_form,
        'profile_form': profile_form,
        'accounts':None,
        "homes":homes['homes'], 
        "current":homes['current']
        }
    if request.user.role == 'client':
        accounts = Account.objects.filter(custom_user_id = custom_user.id)
        context['accounts'] = accounts
    return render(request,'profile/profile.html',context)

@login_required(login_url="/accounts/login/")
def owners(request):
    accounts = Account.objects.filter(object_id=request.session.get('current_object'))
    name = request.GET.get('name',None)
    phone_number = request.GET.get('phone_number',None)
    account_filter = request.GET.get('account',None)
    appartment_number = request.GET.get('appartment_number',None)
    active = request.GET.get('active',None)
    if name is not None and name !="":
        accounts = accounts.filter(Q(custom_user__first_name__icontains = name) | 
                                Q(custom_user__last_name__icontains = name) |
                                Q(custom_user__middle_name__icontains = name))
    if phone_number is not None and phone_number !="":
        phone_number_f = phone_number.replace("(","").replace(")","").replace("-","").replace("+","")
        accounts = accounts.filter(custom_user__phone_number__icontains = phone_number_f)
    if account_filter is not None and account_filter !="":
        accounts = accounts.filter(account__icontains = account_filter)
    if appartment_number is not None and appartment_number !="":
        accounts = accounts.filter(object__appartment_number__icontains = appartment_number)
    if active is not None and active !="":
        if (int(active) == 1) | (int(active) == -1) | (int(active) == 0):
            accounts = accounts.filter(custom_user__is_active = int(active))
    paginator = Paginator(accounts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],
        "accounts":page_obj,
        "leng":accounts.count(),
        "filters":{
            "name":name if name is not None else "",
            "phone_number":phone_number if phone_number is not None else "",
            "account":account_filter if account_filter is not None else "",
            "appartment_number":appartment_number if appartment_number is not None else "",
            "active":active if active is not None else "",
        }}
    return render(request,'contacts/owners.html',context)

def upload_owner_image(request,pk):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=pk)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=user)   
        if image_form.is_valid():
            image_form.save()
            user_updated = CustomUser.objects.get(id=pk)
            return HttpResponse(user_updated.image.url)

@login_required(login_url="/accounts/login/")
def owner(request,pk):
    custom_user = CustomUser.objects.get(id = pk)
    image_form = ProfileImageForm(instance=custom_user)    
    profile_form = OwnerForm(instance=custom_user)
    initial = {
            "username":custom_user.username
        }
    if request.method == 'POST':
        profile_form = OwnerForm(request.POST,initial=initial, instance=custom_user)   
        if profile_form.is_valid():
            if profile_form.cleaned_data['password1'] is not None and profile_form.cleaned_data['password1']!="":
                custom_user.set_password(profile_form.cleaned_data['password1'])
            user = profile_form.save()
            update_session_auth_hash(request, user)
        else:
            profile_form.errors
    else:
        profile_form = OwnerForm(initial=initial,instance=custom_user) 
    homes = get_homes(request)
    context = {
        'image_form': image_form,
        'profile_form': profile_form,
        'accounts':None,
        "homes":homes['homes'], 
        "current":homes['current'],
        "custom_user":custom_user
        }
    account = Account.objects.filter(custom_user_id = custom_user.id).first()
    context['account'] = account
    return render(request,'contacts/owner.html',context)
