import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PersonalProfile, CompanyProfile, NFT
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name',
                                 max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(label='Last Name',
                                max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(label='Username',
                                max_length=100,
                                required=True,
                                help_text="Choose a unique username that you'll use to sign in. It can contain letters, numbers, and underscores.",
                                widget=forms.TextInput(attrs={
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(label='Email',
                             required=True,
                             widget=forms.TextInput(attrs={
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(label='Password',
                                max_length=50,
                                required=True,
                                help_text="Your password must be at least 8 characters long and include at least one uppercase letter (A-Z), one lowercase letter (a-z), one digit (0-9), and one special character (e.g., !, @, #, $, etc.).",
                                widget=forms.PasswordInput(attrs={
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password1',
                                                                  }))
    password2 = forms.CharField(label=' Confirm Password',
                                max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password2',
                                                                  }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class NFTMintForm(forms.ModelForm):
    FILTERS = [
    ('', 'Choose...'),
    ('aden', 'Aden'),
    ('brannan', 'Brannan'),
    ('brooklyn', 'Brooklyn'),
    ('clarendon', 'Clarendon'),
    ('earlybird', 'Earlybird'),
    ('gingham', 'Gingham'),
    ('hudson', 'Hudson'),
    ('inkwell', 'Inkwell'),
    ('lark', 'Lark'),
    ('lofi', 'Lofi'),
    ('maven', 'Maven'),
    ('mayfair', 'Mayfair'),
    ('moon', 'Moon'),
    ('nashville', 'Nashville'),
    ('perpetua', 'Perpetua'),
    ('reyes', 'Reyes'),
    ('rise', 'Rise'),
    ('slumber', 'Slumber'),
    ('stinson', 'Stinson'),
    ('toaster', 'Toaster'),
    ('valencia', 'Valencia'),
    ('walden', 'Walden'),
    ('willow', 'Willow'),
    ('xpro2', 'Xpro2'),
    ]

    name = forms.CharField(label='Full Name', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nft-name'}), help_text='Edit or update your preferred display name. This name will be publicly visible in your NFTs metadata and on all NFT explorers. ', required=True)
    description = forms.CharField(label='Biography / Description', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'nft-description'}), help_text='Add a biography and any information you want to share with the public. Use this space to tell your story and showcase your personality, interests, and achievements. Remeber: Please note that your bio will be permanently stored on the blockchain. Avoid adding time-sensitive information', required=True)
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'image', 'name': 'image', 'accept': 'image/*'}),
        required=True,
        label='NFT Profile Picture'
    )
    image_filter = forms.ChoiceField(
        choices=FILTERS,
        required=False,
        label='Image Filter',
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'image_filter', 'name': 'image_filter'}),  
    )

    class Meta:
        model = NFT
        fields = ['name', 'description', 'image', 'image_filter']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NFTMintForm, self).__init__(*args, **kwargs)
        if self.user:
            initial_full_name = f'{self.user.first_name} {self.user.last_name}'
            self.fields['name'].widget.attrs['placeholder'] = initial_full_name  


phone_regex = RegexValidator(
    regex=r'^\+?\d{0,3}\s?\(\d{3}\)\s?\d{3}-\d{4}$',
    message="Phone number must be entered in this format: '(XXX) XXX-XXXX'. A country code can also be added as in the following format: '+XX (XXX) XXX-XXXX'."
)


class PersonalProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'full_name'}), 
                                help_text='Edit or update your preferred display name. You will have the opportunity to edit this in the future when you create and update your Email Signature, Contact Card, etc.', 
                                required=True, label='Full Name')
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 
                                                                          'placeholder': 'e.g. Vice President , SEO Expert',}), 
                            required=True, label='Title / Position')
    mobile = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'mobile', 'placeholder': '(XXX) XXX-XXXX'}),
                             help_text='Phone number must be entered in this format: (XXX) XXX-XXXX. A country code can also be added as in the following format: +XX (XXX) XXX-XXXX.',
                             validators=[phone_regex], required=False, label='Mobile')
    office = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'office', 'placeholder': '(XXX) XXX-XXXX   Ext. XXX'}), required=False, label='Office Phone')
    personal_website = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_website', 'placeholder': 'https://www.example.com'}), 
                                      help_text='Please enter a complete website address, including "https://". WEB3 ID will do the necessary formatting for you!',
                                      required=False, label='Personal Website')
    personal_twitter = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_twitter', 'placeholder': 'https://www.twitter.com/username'}), 
                                      help_text='Please enter the full URL of your Twitter profile, following the format: https://twitter.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                      required=False, label='Personal X (Twitter)')
    personal_facebook = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_facebook', 'placeholder': 'https://www.facebook.com/username'}),
                                       help_text='Please enter the full URL of your Facebook profile, following the format: https://www.facebook.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                       required=False, label='Personal Facebook')
    personal_linkedin = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_linkedin', 'placeholder': 'https://www.linkedin.com/in/username'}), 
                                       help_text='Please enter the full URL of your LinkedIn profile, following the format: https://www.linkedin.com/in/yourusername. WEB3 ID will do the necessary formatting for you!',
                                       required=False, label='Personal LinkedIn')
    personal_instagram = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_instagram', 'placeholder': 'https://www.instagram.com/username'}), 
                                        help_text='Please enter the full URL of your Instagram profile, following the format: https://www.instagram.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                        required=False, label='Personal Instagram')
    p_color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'p-color', 'name': 'p-color'}), required=False, label='Color - Personal Info Card')
    p_color_header = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'p-color-header', 'name': 'p-color-header'}), required=False, label='Header Font Color')
    
    class Meta:
        model = PersonalProfile
        fields = ['full_name', 'title', 'mobile', 'office', 'personal_website', 'personal_twitter', 'personal_facebook', 'personal_linkedin', 'personal_instagram', 'p_color', 'p_color_header']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PersonalProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            initial_full_name = f'{self.user.first_name} {self.user.last_name}'
            self.fields['full_name'].widget.attrs['placeholder'] = initial_full_name

    

class CompanyProfileForm(forms.ModelForm):
    STATES = [
    ('', 'Choose...'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
    ]

    comp = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'comp'}), 
                                required=False, label='Company Name')
    company_website = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'company_website', 'placeholder': 'https://www.example.com'}), 
                                      help_text='Please enter a complete website address, including "https://". WEB3 ID will do the necessary formatting for you!',
                                      required=False, label='Company Website')
    company_logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'company_logo', 'name': 'company_logo', 'accept': 'image/*'}),
                                    required=False,
                                    label='Company Logo'
                                )
    co_street1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_street1'}), 
                                required=False, label='Street Address 1')
    co_street2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_street2'}), 
                                required=False, label='Street Address 2')
    co_city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_city'}), 
                                required=False, label='City')
    co_state = forms.ChoiceField(
        choices=STATES,
        required=False,
        label='State',
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'co_state', 'name': 'co_state'}),  
    )

    co_zip = forms.CharField(max_length=10, min_length=5, 
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_zip'}), required=False, label='Zip Code')
    
    co_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_phone', 'placeholder': '(XXX) XXX-XXXX'}),
                             help_text='Phone number must be entered in this format: (XXX) XXX-XXXX. A country code can also be added as in the following format: +XX (XXX) XXX-XXXX.',
                             validators=[phone_regex], required=False, label='Company Main Phone')
    
    co_email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_email'}), 
                                required=False, label='Company Email')
    
    co_fax = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_fax', 'placeholder': '(XXX) XXX-XXXX'}),
                             help_text='Fax number must be entered in this format: (XXX) XXX-XXXX. A country code can also be added as in the following format: +XX (XXX) XXX-XXXX.',
                             validators=[phone_regex], required=False, label='Fax')
    
    co_twitter = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_twitter', 'placeholder': 'https://www.twitter.com/username'}), 
                                      help_text='Please enter the full URL of your company Twitter profile, following the format: https://twitter.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                      required=False, label='Company X (Twitter)')
    co_facebook = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_facebook', 'placeholder': 'https://www.facebook.com/username'}),
                                       help_text='Please enter the full URL of your company Facebook profile, following the format: https://www.facebook.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                       required=False, label='Company Facebook')
    co_linkedin = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_linkedin', 'placeholder': 'https://www.linkedin.com/in/username'}), 
                                       help_text='Please enter the full URL of your company LinkedIn profile, following the format: https://www.linkedin.com/in/yourusername. WEB3 ID will do the necessary formatting for you!',
                                       required=False, label='Company LinkedIn')
    co_instagram = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'co_instagram', 'placeholder': 'https://www.instagram.com/username'}), 
                                        help_text='Please enter the full URL of your company Instagram profile, following the format: https://www.instagram.com/yourusername. WEB3 ID will do the necessary formatting for you!',
                                        required=False, label='Company Instagram')
    c_color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'c-color', 'name': 'c-color'}), required=False, label='Color - Company Info Card')
    c_color_header = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'c-color-header', 'name': 'c-color-header'}), required=False, label='Header Font Color')
    
    class Meta:
        model = CompanyProfile
        fields = ['comp', 'company_website', 'company_logo', 'co_street1', 'co_street2', 'co_city', 'co_state', 'co_zip', 'co_phone', 'co_email', 'co_fax', 'co_twitter', 'co_facebook', 'co_linkedin', 'co_instagram', 'c_color', 'c_color_header']
