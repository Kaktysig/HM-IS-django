from internet_shop.models import UserBasketItems, ReadyOrder
from django import forms


class AddToBasketForm(forms.ModelForm):
    def __init__(self, good, *args, **kwargs):
        super(AddToBasketForm, self).__init__(*args, **kwargs)  # populates the post
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = UserBasketItems
        exclude = ('good', 'summ')


class AddOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)  # populates the post
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ReadyOrder
        fields = '__all__'