from django.urls import path

from . import views

urlpatterns = [
    #path('', views.landing, name='landing'),
    path('', views.login_request, name="login_request"),
    path('logout-request', views.logout_request, name="logout_request"),
    path('manage/', views.manage, name="manage"),

    #Model URLs
    path('model/', views.Index.as_view(), name='index'),
    path('create/', views.ModelCreateView.as_view(), name='create_model'),
    path('update/<int:pk>', views.ModelUpdateView.as_view(), name='update_model'),
    path('updatetest/<int:pk>', views.ModelUpdateTestView.as_view(), name='updatetest_model'),
    path('read/<int:pk>', views.ModelReadView.as_view(), name='read_model'),
    path('delete/<int:pk>', views.ModelDeleteView.as_view(), name='delete_model'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    #Loaner URLs
    path('loaners/', views.Index_Loaner.as_view(), name='index_loaner'),
    path('loaners/create/', views.LoanerCreateView.as_view(), name='create_loaner'),
    path('loaners/update/<int:pk>', views.LoanerUpdateView.as_view(), name='update_loaner'),
    path('loaners/read/<int:pk>', views.LoanerReadView.as_view(), name='read_loaner'),
    path('loaners/delete/<int:pk>', views.LoanerDeleteView.as_view(), name='delete_loaner'),
    path('loaners/checkout/<int:pk>', views.LoanerCheckoutView.as_view(), name='checkout_loaner'),
    path('loaners/checkin/<int:pk>', views.LoanerCheckinView.as_view(), name='checkin_loaner'),

    #Record URLs
    # ex:/loaners/1/records/
    path('loaners/<int:pk>/records/', views.record, name='record'),
]
