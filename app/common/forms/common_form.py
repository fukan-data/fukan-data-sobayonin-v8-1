from django.forms import Form

class CommonForm(Form):
    def is_not_empty(self, param):
        data = self.cleaned_date
        return param in data and data[param] and data[param] != ''

    def im_empty(self, param):
        return not self.is_not_empty(param)
