from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from users.views import ResetPasswordView, ChangePasswordView, update_user, mint_nft_view, mint_success_view, apply_filter_and_preview, create_personal_profile, create_company_profile, save_color, save_color_header, save_color_company, save_color_header_company, update_personal_profile, verify_view, verify_success, display_qr_code, track_vcard, qr_dashboard, view_wallet, profile_home_view, email_sig_porfile_view, contact_profile_view, resume_profile_view, profile_personal_view, profile_company_view, update_company_profile, face_login
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
     path('password-change/', ChangePasswordView.as_view(), name='password_change'),
     path('create_personal_profile/', create_personal_profile, name='create_personal_profile'),
     path('create_company_profile/', create_company_profile, name='create_company_profile'),
     path('update-user/', update_user, name='update_user'),
     path('mint-nft/', mint_nft_view, name='mint_nft_view'),
     path('mint-success/', mint_success_view, name='mint-success'),
     path('apply_filter_and_preview/', apply_filter_and_preview, name='apply_filter_and_preview'),
     path('save_color/', save_color, name='save_color'),
     path('save_color_header/', save_color_header, name='save_color_header'),
     path('save_color_company/', save_color_company, name='save_color_company'),
     path('save_color_header_company/', save_color_header_company, name='save_color_header_company'),
     path('profile/update_personal_profile/', update_personal_profile, name='update_personal_profile'),
     path('profile/update_company_profile/', update_company_profile, name='update_company_profile'),
     path('verify/', verify_view, name='verify'), 
     path('verify-success/', verify_success, name='verify-success'),
     path('display-qr-code/', display_qr_code, name='display_qr_code'),
     path('track_vcard/', track_vcard, name='track_vcard'),
     path('qr-dashboard/', qr_dashboard, name='qr_dashboard'),
     path('view_wallet/', view_wallet, name='view_wallet'),
     path('social/', include('socialmedia.urls')),
     path('profile/', profile_home_view, name='profile_home'),
     path('profile/email-signatures', email_sig_porfile_view, name='profile_email_signatures'),
     path('profile/contact-card', contact_profile_view, name='profile_contact_card'),
     path('profile/digital-resume', resume_profile_view, name='profile_digital_resume'),
     path('profile/personal-profile', profile_personal_view, name='profile_personal'),
     path('profile/company-profile', profile_company_view, name='profile_company'),
     path('face_login/', face_login, name='face_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)