from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, ClientAccount, CustomUser
from django import forms

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Фамилия'}))
    middle_name = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Отчество'}))
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control",
                                                                                'placeholder': 'Логин',
                                                                                'readonly':'readonly'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'E-mail'}))
    phone_number = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"phoneable form-control",'placeholder': 'Номер телефона'}))
    password1 = forms.CharField(required=False ,widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=False  ,widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder': 'Пароль еще раз'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','middle_name','username','phone_number','email','password1','password2')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
            if not password2:
                raise forms.ValidationError("Введите повторний пароль.")
            if len(password1)<=5:
                raise forms.ValidationError("Пароль дольжен содержить минимум 6 символов..")
            if password1 != password2:
                raise forms.ValidationError("Пороли не совподают.")
            return password2
        return password2

class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput, label="")
    class Meta:
        model = CustomUser
        fields = ('image', )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Фамилия'}))
    middle_name = forms.CharField(max_length=100,required=False,widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Отчество'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Лицевой счет'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'E-mail'}))
    phone_number = forms.CharField(max_length=100,required=False,widget=forms.TextInput(
                                attrs={"class":"phoneable form-control",'placeholder': 'Номер телефона'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(
                                attrs={'class': "form-control",'placeholder': 'Пароль'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(
                                attrs={'class': "form-control",'placeholder': 'Пароль еще раз'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','middle_name','username','phone_number','email')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("Введите повторний пароль.")
        if password1 != password2:
            raise forms.ValidationError("Пороли не совподают.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError("Введите пароль.")
        if len(password1)<=5:
            raise forms.ValidationError("Пароль дольжен содержить минимум 6 символов..")
        return password1
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if Account.objects.filter(account=username).count()==0:
            raise forms.ValidationError("Лицевой счет не найден")
        if ClientAccount.objects.filter(account__account=username).count()>0:
            raise forms.ValidationError("По данному лицевому счету уже зарегистрирован пользователь")
        if CustomUser.objects.filter(username=username).count()>0:
            raise forms.ValidationError("Пользователь уже сущесвует.")
        return username
    def save(self):
        data = self.cleaned_data
        user = CustomUser(email=data['email'],
                            username=data['username'],
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            middle_name=data['middle_name'],
                            phone_number=data['phone_number'],
                            role="client",
                            is_active=False)
        user.set_password(data['password1'])
        user.save()
        account = Account.objects.get(account=data['username'])
        ClientAccount(client=user,account=account).save()
        