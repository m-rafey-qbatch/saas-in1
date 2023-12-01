from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Post, Reply, Unit, GradeAssignment, Assignment, Submission
import datetime

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
    
    allow_replies = forms.BooleanField(
            widget=forms.CheckboxInput(), 
            required=False,
            label="Allow Replies",
            initial=True
        )
    

    class Meta:
        model = Post
        fields = ['unit', 'subject', 'content', 'image', 'video', 'files', 'allow_replies', 'is_tokengated_content', 'content_cost']


    def __init__(self, *args, current_unit_name=None, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # If a current_unit_name was provided
        if current_unit_name:
            # Limit the queryset to only the corresponding unit
            self.fields['unit'].queryset = Unit.objects.filter(name=current_unit_name)
            
            current_unit = self.fields['unit'].queryset.first()
            
            if current_unit:
                self.fields['unit'].initial = current_unit



class AssignmentForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}), required=True)
    due_date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
        ),
        required=True,
        initial=datetime.date.today()  # Sets initial value to today's date
    )

    class Meta:
        model = Assignment
        fields = ['unit', 'title', 'content', 'image', 'video_upload', 'file_upload', 'due_date']

    def __init__(self, *args, current_unit_name=None, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

        # If a current_unit_name was provided
        if current_unit_name:
            # Limit the queryset to only the corresponding unit
            self.fields['unit'].queryset = Unit.objects.filter(name=current_unit_name)

            current_unit = self.fields['unit'].queryset.first()

            if current_unit:
                self.fields['unit'].initial = current_unit
        # Else, if you want to list all units but make it required for the user to choose
        else:
            self.fields['unit'].queryset = Unit.objects.all()
            self.fields['unit'].empty_label = "Select Unit"
        
        if current_unit_name and not self.fields['unit'].queryset.exists():
            raise ValidationError("Selected unit does not exist.")
        
    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        # Ensure the due date is not in the past
        if due_date < datetime.date.today():
            raise ValidationError("Due date cannot be in the past.")
        return due_date



class SubmissionForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), required=True)

    class Meta:
        model = Submission
        fields = ['content', 'image', 'video_upload', 'file_upload']  # Removed 'assignment'

    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment', None)
        super(SubmissionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # Use the assignment passed during form initialization
        assignment = self.assignment

        # Ensure a submission is not made after the assignment's due date
        if assignment and assignment.due_date < datetime.date.today():
            raise ValidationError("Cannot submit after the assignment's due date.")

        return cleaned_data

    def save(self, commit=True):
        submission = super(SubmissionForm, self).save(commit=False)
        submission.assignment = self.assignment  # Set the assignment to the submission
        if commit:
            submission.save()
        return submission




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



class GradeAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        label='User',  # This will create a label 'User'
        widget=forms.TextInput(attrs={'placeholder': 'Search user by name'})
    )
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), label='Unit') 
    grade = forms.ChoiceField(choices=GradeAssignment.GRADE_CHOICES, label='Grade', required=False)
    is_completed = forms.BooleanField(required=False, label='Completed?', initial=False)
