from django import forms
from .models import Post, Reply, Unit

class PostForm(forms.ModelForm):
    subject = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}),required=True)
    is_tokengated_content = forms.BooleanField(
        widget=forms.CheckboxInput(), 
        required=False,
        label="Token Access Only" 
    )
    content_cost = forms.IntegerField(
        label='Token Cost', 
        required=False,
        widget=forms.NumberInput(attrs={
            'min': '0', 
            'style': 'width: 100px;'
        }))
    

    class Meta:
        model = Post
        fields = ['unit', 'subject', 'content', 'image', 'video', 'files', 'is_tokengated_content', 'content_cost']


    def __init__(self, *args, current_unit_name=None, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # If a current_unit_name was provided
        if current_unit_name:
            # Limit the queryset to only the corresponding unit
            self.fields['unit'].queryset = Unit.objects.filter(name=current_unit_name)
            
            current_unit = self.fields['unit'].queryset.first()
            
            if current_unit:
                self.fields['unit'].initial = current_unit



class ReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}),required=True)
    is_private = forms.BooleanField(
        widget=forms.CheckboxInput(), 
        required=False,
        help_text='Selecting this checkbox will ensure that only your instructor will see your reply post.',
        label="Mark as Private" 
    )

    class Meta:
        model = Reply
        fields = ['content', 'image', 'video', 'files', 'is_private']
