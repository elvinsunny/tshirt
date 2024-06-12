from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Address, CustomUser,Seller,Customer,Product

# class CustomerSignUpForm(UserCreationForm):
#     fname = forms.CharField(max_length=100)
#     lname = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone = forms.CharField(max_length=20)

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'fname', 'lname', 'email', 'phone', 'password1', 'password2')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_customer = True  # Assuming you have an is_customer field in your CustomUser model
#         if commit:
#             user.save()
#             customer = Customer.objects.create(
#                 user=user,
#                 fname=self.cleaned_data['fname'],
#                 lname=self.cleaned_data['lname'],
#                 email=self.cleaned_data['email'],
#                 phone=self.cleaned_data['phone']
#             )
#         return user





from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Customer

class CustomerSignUpForm(UserCreationForm):
    fname = forms.CharField(max_length=100)
    lname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    street = forms.CharField(max_length=255)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'fname', 'lname', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            customer = Customer.objects.create(
                user=user,
                fname=self.cleaned_data['fname'],
                lname=self.cleaned_data['lname'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone']
            )
            # Create Address object
            address = Address.objects.create(
                user=user,
                first_name=self.cleaned_data['fname'],
                last_name=self.cleaned_data['lname'],
                phone_number=self.cleaned_data['phone'],
                street=self.cleaned_data['street'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zip_code=self.cleaned_data['zip_code']
            )
        return user


class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True  # Assuming you have an is_seller field in your CustomUser model
        if commit:
            user.save()
            seller = Seller.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                location=self.cleaned_data['location'],
                email=user.email,  # You can use the email entered in the form or from the user model
                phone=self.cleaned_data['phone']
            )
        return user

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    

class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SellerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def clean_price(self):
#         price = self.cleaned_data.get('price')

#         if price == 0:
#             raise forms.ValidationError("Price cannot be 0. Please enter a valid price.")

#         return price
    




# forms.py
class ProductForm(forms.ModelForm):
    quantity_S = forms.IntegerField(min_value=0, initial=0)
    quantity_M = forms.IntegerField(min_value=0, initial=0)
    quantity_L = forms.IntegerField(min_value=0, initial=0)
    quantity_XL = forms.IntegerField(min_value=0, initial=0)

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'description_2', 'description_3', 'image', 'category', 'seller','quantity_S', 'quantity_M', 'quantity_L', 'quantity_XL']

# forms.py

from django import forms
from .models import Product

class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description','description', 'description_2', 'description_3','price', 'image','category','quantity_S', 'quantity_M', 'quantity_L', 'quantity_XL','reorder_level']


from django import forms
from .models import ShippingDetails

class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ['address', 'city', 'state', 'zip_code']






# from django import forms
# from .models import Customer

# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = Customer 
#         fields = ['fname', 'lname', 'email', 'phone']  # Include other fields as needed



# from django import forms
# from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import User  # Add this import

# from .models import Customer

# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = Customer 
#         fields = ['fname', 'lname', 'email', 'phone']  # Include other fields as needed

# class EditUserForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']  # Include other fields as needed



from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User  # If you're using Django's default user model
from .models import Customer

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Customer 
        fields = ['fname', 'lname', 'email', 'phone']  # Include other fields as needed

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'password']  # Include other fields as needed

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = Customer



from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


# forms.py
from django import forms
from .models import Seller

class EditSellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['company_name', 'location', 'email', 'phone']
