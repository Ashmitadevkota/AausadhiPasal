# from attr import field
# from matplotlib.pyplot import cla
# from django.contrib.auth.forms import ShippingForm
# from django.contrib.auth.models import User




# from secrets import choice


# class ShippingForm(forms.Form):
#     province = forms.CharField(choices=Province, default='Province',max_length=20 )
#     class Meta:
#         model = ShippingAddress
#         fields = ['province']

# from django import forms

# from medicines.models import ShippingAddress


# def phone(value):
#     if len(value)>=10:
#         raise forms.ValidationError(f"Your phoneno should be of 10 ")


# class ShippingForm(forms.ModelForm):
#     address = forms.CharField(max_length=100)
#     city = forms.CharField(max_length=100)
#     ward_no = forms.IntegerField()
#     zip_code = forms.CharField(max_length=5 )
#     phone = forms.CharField(label="phone",widget=forms.TextInput(attrs={"placeholder":"phone no","id":"phone"}),validators=[phone],error_messages={'required':'phoneno is required'})
#     pres = forms.ImageField()

#     class  Meta:
#          model = ShippingAddress
#          fields =['phone']
   

# class ShippingForm(forms.ModelForm):
#     # specify the name of model to use
#     class Meta:
#         model = ShippingAddress
#         fields = "__all__"

# class ShippingForm(forms.ModelForm):
#     class Meta:
#         model = ShippingAddress
#         fields = "__all__"