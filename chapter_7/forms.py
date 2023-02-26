''' Chapter 7 Forms Module '''
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.core.mail import (
    EmailMessage,
    # EmailMultiAlternatives
)
from django.core.validators import EmailValidator, validate_email
from django.forms import Form, ModelForm, formset_factory
from django.template.loader import get_template

from xhtml2pdf import pisa

from .fields import MultipleEmailField
from chapter_3.models import Vehicle


class ContactForm(Form):
    '''
    Form Object Class to capture contact form submissions.
    '''

    # pass
    success_url = '/default-contact-success/'

    full_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(
            attrs={
                'id': 'full-name',
                'class': 'form-input-class',
                'placeholder': 'Your Name, Written By...'
            }
        ),
        help_text='Enter your full name, first and last name please',
        min_length=2,
        max_length=300,
        required=True,
        error_messages={
            'required': 'Please provide us with a name to address you as',
            'min_length': 'Please lengthen your name, min 2 characters',
            'max_length': 'Please shorten your name, max 300 characters'
        }
    )
    email_1 = forms.CharField(
        label='email_1 Field',
        min_length=5,
        max_length=254,
        required=False,
        help_text='Email address in example@example.com format for contacting you should we '
        'have questions about your message.',
        validators=[
            EmailValidator('Please enter a valid email address'),
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
        help_text='Email address in example@example.com format for contacting you should we '
        'have questions about your message.',
        error_messages={
            'required': 'Please provide us an email address should we need to reach you',
            'email': 'Please enter a valid email address',
            'min_length': 'Please lengthen your name, min 5 characters',
            'max_length': 'Please shorten your name, max 254 characters'
        }
    )
    email_3 = forms.CharField(
        label='email_3 Field',
        min_length=5,
        max_length=254,
        required=False,
        help_text='Email address in example@example.com format for contacting you should we '
        'have questions about your message.',
        error_messages={
            'min_length': 'Please lengthen your name, min 5 characters',
            'max_length': 'Please shorten your name, max 254 characters'
        }
    )
    conditional_required = forms.CharField(
        label='Required only if field labeled "email_3" has a value',
        widget=forms.TextInput(
            attrs={
                'id': 'required-test-field',
                'class': 'form-input-class',
                'placeholder': 'Enter Any Value...'
            }
        ),
        help_text='This field is only required if the field labeled "email_3 Field" has a value',
        min_length=2,
        max_length=100,
        required=False,
        error_messages={
            'min_length': 'Please lengthen your name, min 2 characters',
            'max_length': 'Please shorten your name, max 100 characters'
        }
    )
    multiple_emails = MultipleEmailField(
        label='Multiple Email Field',
        help_text='Please enter one or more email addresses, each separated by a comma with '
        'NO spaces',
        required=True,
        error_messages={
            # 'required': 'This multiple_emails field is required.',,
            # 'email': 'Custom email message, overrides default_error_messages'
        }
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 50}
        ),
        required=True,
        help_text='Please provide a message',
        max_length=5000,
        error_messages={
            'required': 'Please provide us a message',
            'max_length': 'Please shorten your name, max 5000 characters'
        }
    )

    def __init__(self, *args, **kwargs):
        # def __init__(self, excluded, *args, **kwargs):
        '''
        Initialize Form Fields
        '''
        super(ContactForm, self).__init__(*args, **kwargs)
        #self.error_class = DivErrorList

        # for field in excluded:
        #    try:
        #        del self.fields[field]
        #    except KeyError as e:
        #        print('Field %s does not exist' % str(e))

    def is_valid(self):
        '''
        Add Error Class to Field Objects
        '''
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {'class': self.fields[f].widget.attrs.get(
                    'class', '') + ' field-error'}
            )

        return ret

    def clean(self):
        '''
        Validation - Compares Two or More Fields Against Each Other
        '''
        # print('clean()')
        # print(self.data)
        # print(self.cleaned_data)

        # Instead of writing self.cleaned_data over and over again, this can also be written as.
        #cleaned_data = super().clean()
        # print(cleaned_data)

        email = self.cleaned_data['email_3']
        text_field = self.cleaned_data['conditional_required']

        # For a more fail-safe approach with more checks and balances, use the example below
        #email = ''
        #text_field = ''

        # if 'email_3' in self.cleaned_data and self.cleaned_data['email_3'] != '':
        #    email = self.cleaned_data['email_3']

        #    if (
        #        'conditional_required' in self.cleaned_data and
        #        self.cleaned_data['conditional_required'] != ''
        #    ):
        #        text_field = self.cleaned_data['conditional_required']

        if email and not text_field:
            self.add_error(
                'conditional_required',
                'If there is a value in the field labeled "email_3" then this field is required'
            )

    def clean_email_3(self):
        '''
        Validation - Compares a Single Field Only - email_3 field.
        '''
        #print('clean_email_3() Fired')
        # print(self.data)
        # print(self.cleaned_data)

        email = self.cleaned_data['email_3']

        if email != '':
            try:
                validate_email(email)
            except ValidationError:
                self.add_error(
                    'email_3',
                    f'The following is not a valid email address: {email}'
                )
                # raise ValidationError(
                #    'The following is not a valid email address: {0}'.format(email)
                # )
        else:
            self.add_error('email_3', 'This field is required')
            #raise ValidationError('This field is required')

        return email

    def send_email(self, request):
        '''
        Method to send generic email
        '''
        print('Creating Email')

        # The 'request' variable not used, but it can be passed in to access here in any way
        # you would normally use the 'request' object.

        data = self.cleaned_data

        # Used for Sending Template Based Emails
        #template = get_template('chapter_7/emails/plain_text_format.html')
        #template = get_template('chapter_7/emails/html_format.html')
        #template = get_template('chapter_7/emails/new_contact_form_entry.html')
        # context = {
        #    'data': data
        # }

        # Used for Plain Text Format
        msg_body = 'Hello World'

        # Used for Rich Text Format
        #msg_body = '<b>Hello World</b>'

        # Used for Template Based Email
        #msg_body = template.render()
        #msg_body = template.render(context)

        # Format Email Headers
        email = EmailMessage(
            subject='New Contact Form Entry',
            body=msg_body,
            from_email='no-reply@example.com',
            reply_to=['no-reply@example.com'],
            cc=[],
            bcc=[],
            to=[data['email_1']],
            attachments=[],
            headers={},
        )

        # email = EmailMultiAlternatives(
        #    subject = 'New Contact Form Entry',
        #    body = msg_body,
        #    from_email = 'no-reply@example.com',
        #    reply_to = ['no-reply@example.com'],
        #    cc = [],
        #    bcc = [],
        #    to = [data['email_1']],
        #    attachments = [],
        #    headers = {},
        # )

        # Change Message From Text/Plain to Text/HTML
        email.content_subtype = 'plain'  # Plain Text Emails
        # email.content_subtype = 'html' # HTML and Rich Text Emails

        #email = EmailMultiAlternatives(subject=subject, body=text_body, to=[user.email])
        #email.attach_alternative('Hello World', 'text/plain')

        # Used for Attaching a PDF Document (or Any File Type)
        # email.attach_file('static/chapter_7/pdf/example.pdf')
        #email.attach_file(settings.STATIC_ROOT + '/chapter_7/pdf/example.pdf')

        # Actually Sends the Email
        email.send(fail_silently=True)

    def generate_pdf(self, request):
        '''
        Method to print/generate generic PDF
        '''
        print('Generating PDF')

        template = get_template('chapter_7/pdfs/pdf_template.html')

        # Used for Template Based PDF - Static PDF Example
        #dest = open(settings.STATIC_ROOT + '/chapter_7/pdf/test.pdf', 'w+b')

        # Used for Template Based PDF w/ Context - Dynamic PDF Example
        data = self.cleaned_data
        context = {
            'data': data
        }

        # Used for Template Based PDF w/ Context - Dynamic PDF Example
        dest = open(settings.STATIC_ROOT + '/chapter_7/pdf/test_2.pdf', 'w+b')

        # Used for Template Based PDF - Static PDF Example
        #html = template.render()

        # Used for Template Based PDF w/ Context - Dynamic PDF Example
        html = template.render(context)

        # Creates the PDF Document
        result = pisa.CreatePDF(
            html,
            dest=dest,
        )

        # Optional Error Catching
        # if result.err:
        #    print('PDF Error Found')
        #    return HttpResponse(
        #        'We had problems generating the PDF. Error found {0}'.format(result.err)
        #    )

        return HttpResponse(result.err)


class VehicleForm(ModelForm):
    '''
    Form Object Class to capture vehicle form submissions.
    '''
    class Meta:
        '''
        Vehicle Form Meta Sub-Class
        '''
        model = Vehicle
        fields = ['vin', 'sold', 'price', 'make', 'vehicle_model', 'engine', ]


class ProspectiveBuyerForm(Form):
    '''
    Form Object Class to capture prospective buyers form submissions.
    '''
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'id': 'first-name',
                'class': 'form-input-class',
                'placeholder': 'First Name, Prospective Buyer'
            }
        ),
        help_text='Enter your first name only',
        min_length=2,
        max_length=300,
        required=True,
        error_messages={
            'required': 'Please provide us with a first name',
            'min_length': 'Please lengthen your name, min 2 characters',
            'max_length': 'Please shorten your name, max 300 characters'
        }
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'id': 'last-name',
                'class': 'form-input-class',
                'placeholder': 'Last Name, Prospective Buyer'
            }
        ),
        help_text='Enter your last name only',
        min_length=2,
        max_length=300,
        required=True,
        error_messages={
            'required': 'Please provide us with a last name',
            'min_length': 'Please lengthen your name, min 2 characters',
            'max_length': 'Please shorten your name, max 300 characters'
        }
    )


ProspectiveBuyerFormSet = formset_factory(
    ProspectiveBuyerForm,
    extra=1
)
