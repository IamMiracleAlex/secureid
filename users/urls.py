from django.urls import path

from users import views



urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('password-reset-request/', views.ResetPasswordRequest.as_view()),
    path('reset-password-validate-token/', views.ResetPasswordValidateToken.as_view()),
    path('reset-password-confirm/', views.ResetPasswordConfirm.as_view()),
]
