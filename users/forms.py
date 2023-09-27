import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PersonalProfile, NFT
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
    GRADES = [
    ('', 'Choose...'),
    ('1st Grade', '1st Grade'),
    ('2nd Grade', '2nd Grade'),
    ('3rd Grade', '3rd Grade'),
    ('4th Grade', '4th Grade'),
    ('5th Grade', '5th Grade'),
    ('6th Grade', '6th Grade'),
    ('7th Grade', '7th Grade'),
    ('8th Grade', '8th Grade'),
    ('9th Grade', '9th Grade'),
    ('10th Grade', '10th Grade'),
    ('11th Grade', '11th Grade'),
    ('12th Grade', '12th Grade'),
    ('Freshman - Univeristy', 'Freshman - Univeristy'),
    ('Sophmore - Univeristy', 'Sophmore - Univeristy'),
    ('Junior - Univeristy', 'Junior - Univeristy'),
    ('Senior - Univeristy', 'Senior - Univeristy'),
    ('Adult Learner', 'Adult Learner'),
    ]


    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'full_name'}), 
                                help_text='Edit or update your preferred display name. You will have the opportunity to edit this in the future when you create and update your Email Signature, Contact Card, etc.', 
                                required=True, label='Full Name')
    
    grade_level = forms.ChoiceField(
        choices=GRADES,
        required=False,
        label='Grade Level',
        widget=forms.Select(attrs={'class': 'custom-select', 'id': 'grade_level', 'name': 'image_level'}),  
    )
    
    school = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'school'}),
                             help_text='Please enter the name of the school in wihch you are currently enrolled (if applicable).', required=False, label='School')
    
    hometown = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hometown'}),
                             help_text='Share where you currently live or where you are from originally!',
                             required=False, label='Hometown')

    mobile = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'mobile', 'placeholder': '(XXX) XXX-XXXX'}),
                             help_text='Phone number must be entered in this format: (XXX) XXX-XXXX. A country code can also be added as in the following format: +XX (XXX) XXX-XXXX.',
                             validators=[phone_regex], required=False, label='Mobile')
   
    personal_website = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_website', 'placeholder': 'https://www.example.com'}), 
                                      help_text='Please enter a complete website address, including "https://". WEB3 ID will do the necessary formatting for you!',
                                      required=False, label='Personal Website')
   
    personal_linkedin = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'personal_linkedin', 'placeholder': 'https://www.linkedin.com/in/username'}), 
                                       help_text='Please enter the full URL of your LinkedIn profile, following the format: https://www.linkedin.com/in/yourusername. WEB3 ID will do the necessary formatting for you!',
                                       required=False, label='Personal LinkedIn')
   
    p_color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'p-color', 'name': 'p-color'}), required=False, label='Color - Personal Info Card')
    p_color_header = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'p-color-header', 'name': 'p-color-header'}), required=False, label='Header Font Color')
    
    class Meta:
        model = PersonalProfile
        fields = ['full_name', 'grade_level', 'school', 'hometown', 'mobile', 'personal_website', 'personal_linkedin', 'p_color', 'p_color_header']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PersonalProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            initial_full_name = f'{self.user.first_name} {self.user.last_name}'
            self.fields['full_name'].widget.attrs['placeholder'] = initial_full_name

    

