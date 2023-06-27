from django import forms
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class FormControl(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})



class LoginForm(forms.ModelForm, FormControl):
    username = forms.CharField()


    class Meta:
        model = User
        fields = ("password", )
    
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise forms.ValidationError("This user does not exist")
        
        if not user.is_active:
            raise forms.ValidationError("This account is not activated")
        
        return super().clean()




class RegisterForm(forms.ModelForm, FormControl):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")


    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if len(password) < 6:
            raise forms.ValidationError("Passwordun minimum uzunlugu 6 olmalidir")

        if not password[0].isalpha() and not password[0].isupper():
            raise forms.ValidationError("Password boyuk herfle baslamalidir")
        
        return super().clean()


    def save(self, commit=True):
        password = self.cleaned_data.pop("password")
        self.cleaned_data["is_active"] = False

        if commit:
            user = User.objects.create(**self.cleaned_data)
            user.set_password(password)
            user.save()
            return user

        user = User(**self.cleaned_data)
        user.set_password(password)
        return user
