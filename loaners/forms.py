from django import forms
from datetimepicker.widgets import DateTimePicker
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm


from .models import Model, Loaner
from datetime import date, datetime
import ctypes
import getpass

dotdot = '---------'

class DateInput(forms.DateInput):
    input_type = 'date'


def get_technician_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    a = (nameBuffer.value).split(', ')
    return a[1] + ' ' + a[0]

class ModelForm(BSModalForm):

    class Meta:
        model = Model
        exclude = ['timestamp']

class ModelTestForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['screen'] = 'Test'
        kwargs['initial'] = initial
        super(ModelTestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Model
        fields = ['hard_drive', 'screen']

class LoanerForm(BSModalForm):

    class Meta:
        model = Loaner
        exclude = ['timestamp']

class LoanerCreateForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['technician'] = dotdot
        initial['borrower'] = dotdot

        initial['date_out'] = datetime.today()
        initial['date_in'] = datetime.today()
        kwargs['initial'] = initial
        super(LoanerCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Loaner
        exclude = ['adapter_included', 'checked_in', 'timestamp']
        labels = {
            'technician' : '',
            'date_out' : '',
            'date_in' : '',
            'borrower' : '',
        }

        widgets = {
            'technician' : forms.HiddenInput(),
            'date_out' : forms.HiddenInput(),
            'date_in' : forms.HiddenInput(),
            'borrower' : forms.HiddenInput(),

        }

class LoanerCheckoutForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['technician'] = get_current_authenticated_user
        initial['date_out'] = datetime.today()
        initial['borrower'] = ''
        initial['checked_in'] = False
        kwargs['initial'] = initial
        super(LoanerCheckoutForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Loaner
        fields = ['borrower', 'date_in', 'adapter_included', 'date_out', 'technician', 'checked_in']
        exclude = ['name', 'model','service_ticket', 'timestamp']
        labels = {
            'technician':'',
            'date_out':'',
            'date_in':'Return date',
            'checked_in':'',
            'adapter_included':'Include adapter?'
        }

        widgets = {
            'technician':forms.HiddenInput(),
            'date_out':forms.HiddenInput(),
            'checked_in':forms.HiddenInput(),
            'date_in':DateInput(attrs={'inline': False, 'min': date.today()}),
        }
    #Validation
    def clean_date_in(self, *args, **kwargs):
        date_in = self.cleaned_data.get("date_in")
        if datetime.date(date_in) < date.today():
            raise forms.ValidationError("This date cannot be in the past.")
        else:
            return date_in

class LoanerCheckinForm(BSModalForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['technician'] = dotdot
        initial['date_out'] = datetime.today()
        initial['date_in'] = datetime.today()
        initial['borrower'] = dotdot
        initial['checked_in'] = True
        initial['adapter_included'] = True
        kwargs['initial'] = initial
        super(LoanerCheckinForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Loaner
        fields = ['date_in', 'date_out', 'checked_in', 'borrower', 'technician', 'adapter_included', 'service_ticket']
        exclude = [ 'timestamp']
        labels = {
            'technician' : '',
            'date_out': '',
            'date_in' : '',
            'borrower' : '',
            'checked_in' : '',
            'adapter_included' : '',
            'service_ticket' : '',
        }

        widgets = {
            'technician' : forms.HiddenInput(),
            'date_out' : forms.HiddenInput(),
            'checked_in' : forms.HiddenInput(),
            'date_in' : forms.HiddenInput(),
            'borrower' : forms.HiddenInput(),
            'adapter_included' : forms.HiddenInput(),
            'service_ticket' : forms.HiddenInput(),
        }

class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
