from django import forms


class BootstrapModelFormMixin(forms.ModelForm):
    """As a parent class, used to generate front-end styles"""
    exclude = []

    def __init__(self, *args, **kwargs):
        super(BootstrapModelFormMixin, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            if name not in self.exclude:
                former_attrs = filed.widget.attrs.get('class', '')
                filed.widget.attrs['class'] = f'form-control {former_attrs}'
                filed.widget.attrs['placeholder'] = f'{filed.label}'



