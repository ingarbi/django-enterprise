from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, validate_email
from django.forms import Form, ModelForm, formset_factory
from .fields import MultipleEmailField
from chapter_3.models import Vehicle


class ContactForm(Form):
    template_name = 'chapter_5/forms/custom-form.html'
    full_name = forms.CharField(
        label='Full Name',
        help_text='Enter your full name, first and last name please',
        min_length=2,
        max_length=300,
        required=True,
        error_messages={
            'required': 'Please provide us with a name to address you as',
            'min_length': 'Please lengthen your name, min 2 characters',
            'max_length': 'Please shorten your name, max 300 characters'
        },
        widget=forms.TextInput(
            attrs={
                'id': 'full-name',
                'class': 'form-input-class',
                'placeholder': 'Your Name, Written By...'
            }
        ),

    )
    email_1 = forms.CharField(
        label='email_1 Field',
        min_length=5,
        max_length=254,
        required=False,
        help_text='Email address in example@example.com format.',
        validators=[
            EmailValidator(
                'Please enter a valid email address'
            ),
        ],
        error_messages={
            'min_length': 'Please lengthen your name, min 5 characters',
            'max_length': 'Please shorten your name, max 254 characters'
        }
    )

    email_2 = forms.EmailField(
        label='email_2 Field',
        min_length=5,
        max_length=254,
        required=True,
        help_text='Email address in example@example.com format for contacting you should we have questions about your message.',
        error_messages={
            'required': 'Please provide us an email address should we need to reach you',
            'email': 'Please enter a valid email address',
            'min_length': 'Please lengthen your name, min 5 characters',
            'max_length': 'Please shorten your name, max 254 characters'
        }
    )
    email_3 = forms.CharField(
        label='Email Using CharField and Using Clean Method',
        required=False,
        help_text='Email address in example@example.com format for contacting you should we have questions about your message.',
    )

    def clean_email_3(self):
        email = self.cleaned_data['email_3']
        if email != '':
            try:
                validate_email(email)
            except ValidationError:
                self.add_error('email_3', f'The following is not a valid email address: {email}'
                               )
        else:
            self.add_error(
                'email_3',
                'This field is required'
            )
        return email

    conditional_required = forms.CharField(
        label='Required only if field labeled "email_3" has a value',
        help_text='This field is only required if the field labeled "email_3 Field" has a value',
        required=False,
    )

    def clean(self):
        email = self.cleaned_data['email_3']
        text_field = self.cleaned_data['conditional_required']
        if email and not text_field:
            self.add_error('conditional_required',
                           'If there is a value in the field labeled "email_3" then this field is required'
                           )

    multiple_emails = MultipleEmailField(
        label='Multiple Email Field',
        help_text='Please enter one or more email addresses,each separated by a comma and no spaces',
        required=True,
    )


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vin',
            'sold',
            'price',
            'make',
            'vehicle_model',
            'engine',
        ]


class ProspectiveBuyerForm(Form):
    first_name = forms.CharField(
        label='First Name',
        help_text='Enter your first name only',
        required=True,
        error_messages={
            'required': 'Please provide us with a first name',
        }
    )

    last_name = forms.CharField(
        label='Last Name',
        help_text='Enter your last name only',
        required=True,
        error_messages={
            'required': 'Please provide us with a last sname',
        }
    )


ProspectiveBuyerFormSet = formset_factory(
    ProspectiveBuyerForm,
    extra=1
)
