from main.service import get_homes
from location.models import City, Country, Object, Street
from users.models import Account, CustomUser
from django.shortcuts import render,redirect
import random, string, openpyxl
from django.contrib import messages
from .forms import ProfileImageForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash

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
    return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/'+request.GET.get('type')+'/'+pk+"/change/?pch="+password)

def upload_account(request):
    if request.method == "POST":
        if request.FILES:
            excel_file = request.FILES['myfile']
            if not excel_file.name.endswith('xlsx'):
                messages.error(request, "wrong format")
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
                    try:
                        country = Country.objects.get(name = row[2])
                    except:
                        country = Country(name=row[2])
                        country.save()
                    try:
                        city = City.objects.get(country_id = country.id, name = row[3])
                    except:
                        city = City(country_id=country.id, name=row[3])
                        city.save()
                    try:
                        street = Street.objects.get(city_id=city.id,name=row[4])
                    except:
                        street = Street(city_id=city.id, name=row[4])
                        street.save()
                    try:
                        object = Object.objects.get(street_id=street.id,
                                                    home=row[5],
                                                    campus=row[6],
                                                    appartment=row[7][:-2]
                                                    )
                    except:
                        object = Object(street_id=street.id,
                                                    home=row[5],
                                                    campus=row[6],
                                                    appartment=row[7][:-2]
                                                    )
                        object.save()
                    account = Account()
                    account.account = row[0][:-2]
                    account.name = row[1]
                    account.total_square = row[8]
                    account.living_square = row[9]
                    account.share = row[10]
                    account.object_id=object.id
                    account.save()
                except:
                    error_rows.append(row[0][:-2])
            if len(error_rows)==0:
                messages.info(request, "Succeed")
            else:
                rows = ""
                for row in error_rows:
                    rows += " "+row+","
                messages.warning(request, "There are some rows, which was not imported. Rows"+rows)
            return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/')
        else:
            messages.error(request, "No file")
            return redirect("{0}://{1}".format('http', request.get_host()) + '/admin/users/account/')

def contacts(request):
    organization_workers =[]
    for organization in CustomUser.objects.get(id=request.user.id).organization.all():
        for item in organization.organization_workers.all():
            organization_workers.append(item.worker)
    moderators = CustomUser.objects.all()
    homes = get_homes(request)
    context = {"organization_workers":organization_workers,'moderators':moderators,
                "homes":homes['homes'], "current":homes['current']}
    return render(request,'contacts/contacts.html',context)

def account(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'accounts/accounts.html', context)

def upload(request):
    if request.method == 'POST':
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user)   
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(request.user.image.url)

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
        accounts = Account.objects.filter(account_clients__client_id = custom_user.id)
        context['accounts'] = accounts
    return render(request,'profile/profile.html',context)

def owners(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'contacts/owners.html',context)
