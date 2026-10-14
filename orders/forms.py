from django import forms
from django.core.validators import RegexValidator


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        label='Nombre Completo',
        max_length=150,
        widget=forms.TextInput(attrs={
            'autocomplete': 'name',
            'class': 'w-full border-b border-gray-300 py-2 focus:outline-none focus:border-black transition-colors bg-transparent',
        }),
    )
    customer_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'w-full border-b border-gray-300 py-2 focus:outline-none focus:border-black transition-colors bg-transparent',
        }),
    )
    customer_phone = forms.CharField(
        label='Teléfono / WhatsApp',
        min_length=7,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s()\-]{7,20}$',
                message='Ingresa un teléfono válido.',
            ),
        ],
        widget=forms.TextInput(attrs={
            'autocomplete': 'tel',
            'placeholder': '+569...',
            'class': 'w-full border-b border-gray-300 py-2 focus:outline-none focus:border-black transition-colors bg-transparent',
        }),
    )
    quantity = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'class': 'w-full border border-gray-300 p-3 focus:outline-none focus:border-black',
        }),
        initial=1,
    )

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product is not None:
            self.fields['quantity'].max_value = product.stock
            self.fields['quantity'].widget.attrs['max'] = product.stock
