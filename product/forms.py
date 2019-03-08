from django import forms

from categories.models import Category
from .models import ProductColor, ProductSize, ProductSizeSettings, Product, Calculation


class ProductColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductColorForm, self).__init__(*args, **kwargs)
        if self.category:
            self.fields['color'].widget.attrs.update({'data-category': self.category})


class ProductSizeSettingsForm(forms.ModelForm):
    class Meta:
        model = ProductSizeSettings
        fields = ['size', 'count']

    def __init__(self, *args, **kwargs):
        super(ProductSizeSettingsForm, self).__init__(*args, **kwargs)
        initial = kwargs.pop('initial', None)
        # print initial
        if initial is not None:
            if 'category_id' in initial:
                category_id = initial['category_id']
                choices = ()
                for x in ProductSize.objects.filter(category_id=category_id):
                    choices += (x.id, x.title),
                self.fields['size'].widget.choices = choices


class OrderInOneClickForm(forms.Form):
    name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'uk-textarea'}), required=False)
    count = forms.IntegerField(widget=forms.HiddenInput())


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ('category', 'product', 'area', 'thickness')

    def __init__(self, *args, **kwargs):
        super(CalculationForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(calculation_category='dry_mixture')
        self.fields['product'].queryset = Product.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['product'].queryset = Product.objects.filter(category_id=category_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['product'].queryset = self.instance.category.product_set.order_by('title')
