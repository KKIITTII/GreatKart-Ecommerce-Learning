from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs  =  {
        'placeholder' : 'Enter Password',
        'class': 'form-control',
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs = {
        'placeholder' : 'Confirm Password',
        'class': 'form-control',
    }))
    
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number", "email", "password")
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = cleaned_data.get("phone_number")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        
        if phone_number and type(int(phone_number)) is not int:
            raise forms.ValidationError('Phone number is not correct')
        
        return cleaned_data


   
# Custom save
# def save(self, *args, **kwargs):
#     self.p1= p1
#     super.save( *args, **kwargs)