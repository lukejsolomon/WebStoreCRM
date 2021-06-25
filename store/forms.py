from django import forms


from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices= (('Pending', 'Pending'), ('Picked', 'Picked'), ('Shipped', 'Shipped'),),
        required=False,
        widget=forms.RadioSelect()
        )
    class Meta:
        model = ShippingAddress
        fields = ('status', 'note')
        widgets = {
        'note':forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':'Enter Tracking Info',}),
        }
        
class ServiceForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices= (('Pending', 'Pending'), ('Canceled', 'Canceled'),),
        required=False,
        widget=forms.RadioSelect()
        )
    class Meta:
        model = ShippingAddress
        fields = ('status', 'note')
        widgets = {
        'note':forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':'Note',}),
        }
