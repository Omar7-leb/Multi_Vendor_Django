from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=250)
    zipcode = forms.CharField(max_length=10)
    place = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['phone'].initial = user.customer.phone_number
        self.fields['address'].initial = user.customer.address
