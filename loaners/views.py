from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def landing(request):
    return render(request, 'loaners/landing.html')

def login_request(request):


    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")

                #if user is staff redirect to manage page
                if user.is_staff == True:
                    return redirect('/manage')

                else:
                    return redirect('/loaners')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    if request.user.is_authenticated:
        return redirect("/loaners")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "landing.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def manage(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    return render(request, 'manage.html')

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView,
                                           )

from .forms import ModelForm, ModelTestForm, LoanerForm, LoanerCreateForm, LoanerCheckoutForm, LoanerCheckinForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Model, Loaner, Record

#Model Views
class Index(LoginRequiredMixin,generic.ListView):
    login_url = "/"
    model = Model
    context_object_name = 'models'
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return  HttpResponseForbidden()

        models = Model.objects.all()
        return render(request, self.template_name, {'models': models})


class ModelCreateView(BSModalCreateView):
    template_name = 'loaners/create_model.html'
    form_class = ModelForm
    success_message = 'Success: Model was created.'
    success_url = reverse_lazy('index')


class ModelUpdateView(BSModalUpdateView):
    model = Model
    template_name = 'loaners/update_model.html'
    form_class = ModelForm
    success_message = 'Success: Model was updated.'
    success_url = reverse_lazy('index')


class ModelReadView(BSModalReadView):
    model = Model
    template_name = 'loaners/read_model.html'


class ModelDeleteView(BSModalDeleteView):
    model = Model
    template_name = 'loaners/delete_model.html'
    success_message = 'Success: Model was deleted.'
    success_url = reverse_lazy('index')

#Sign Up Views
class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'loaners/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index_loaner')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'loaners/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index_loaner')

class ModelUpdateTestView(BSModalUpdateView):
    model = Model
    template_name = 'loaners/update_model.html'
    form_class = ModelTestForm
    success_message = 'Success: ModelTest was updated.'
    success_url = reverse_lazy('index')

#Loaner Views

class Index_Loaner(LoginRequiredMixin, generic.ListView):
    login_url = "/"
    model = Loaner
    context_object_name = 'loaners'
    template_name = 'index_loaner.html'


class LoanerCreateView(BSModalCreateView):
    template_name = 'loaners/create_loaner.html'
    form_class = LoanerCreateForm
    success_message = 'Success: Loaner was created.'
    success_url = reverse_lazy('index_loaner')


class LoanerUpdateView(BSModalUpdateView):
    model = Loaner
    template_name = 'loaners/update_loaner.html'
    form_class = LoanerForm
    success_message = 'Success: Loaner was updated.'
    success_url = reverse_lazy('index_loaner')

class LoanerCheckoutView(BSModalUpdateView):
    model = Loaner
    template_name = 'loaners/checkout_loaner.html'
    form_class = LoanerCheckoutForm
    success_message = 'Success: Loaner checked out.'
    success_url = reverse_lazy('index_loaner')

class LoanerCheckinView(BSModalUpdateView):
    model = Loaner
    template_name = 'loaners/checkin_loaner.html'
    form_class = LoanerCheckinForm
    success_message = 'Success: Loaner checked in.'
    success_url = reverse_lazy('index_loaner')

class LoanerReadView(BSModalReadView):
    model = Loaner
    template_name = 'loaners/read_loaner.html'


class LoanerDeleteView(BSModalDeleteView):
    model = Loaner
    template_name = 'loaners/delete_loaner.html'
    success_message = 'Success: Loaner was deleted.'
    success_url = reverse_lazy('index_loaner')

#Record Views

def record(request, pk):
    loaner = Loaner.objects.get(pk=pk)
    name = loaner.name
    record_list = loaner.record_set.all().order_by('-action_date')
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(record_list, 100)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    context = {'name' : name, 'records' : records}

    return render(request, 'record.html', context)
