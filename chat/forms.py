from django import forms
from users.models import ChatRoom
from django.contrib.auth.models import User
from django.utils.html import format_html


class ChatRoomForm(forms.ModelForm):
    class ParticipantField(forms.ModelMultipleChoiceField):
        def __init__(self, *args, **kwargs):
            superusers_first = User.objects.all().order_by('-is_superuser', 'username')
            kwargs['queryset'] = superusers_first
            super().__init__(*args, **kwargs)

        def label_from_instance(self, obj):
            try:
                label = obj.personal_profile.full_name
            except AttributeError:
                label = obj.username  # Fallback to username if personal_profile does not exist

            if obj.is_superuser:
                label += " (Moderator)"
            return format_html('<span style="color:{}">{}</span>',
                               'red' if obj.is_superuser else 'black',
                               label)

    participants = ParticipantField(
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta:
        model = ChatRoom
        fields = ['participants']

    # Add the custom __init__ method
    def __init__(self, *args, user=None, **kwargs):
        super(ChatRoomForm, self).__init__(*args, **kwargs)
        if user:
            superusers_first = User.objects.exclude(id=user.id).order_by('-is_superuser', 'username')
            self.fields['participants'].queryset = superusers_first
