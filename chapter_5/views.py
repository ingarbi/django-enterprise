from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView, FormView, UpdateView

from chapter_3.models import Vehicle

from .forms import ContactForm, VehicleForm, ProspectiveBuyerFormSet


class FormClassView(FormView):
    template_name = 'chapter_5/form-class.html'
    form_class = ContactForm
    success_url = '/chapter-5/contact-form-success/'

    def get(self, request, *args, **kwargs):
        initial = {
            'full_name': 'FirstName LastName',
            'email_1': 'example1@example.com',
            # Add A Value For Every Field...
        }
        return TemplateResponse(
            request,
            self.template_name,
            {
                'title': 'FormClassView Page',
                'page_id': 'form-class-id',
                'page_class': 'form-class-page',
                'h1_tag': 'This is the FormClassView Page Using ContactForm',
                'form': self.form_class(initial),
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(
                self.success_url
            )
        else:
            return TemplateResponse(request,
                                    self.template_name,
                                    {
                                        'title': 'FormClassView Page - Please Correct The Errors Below',
                                        'page_id': 'form-class-id',
                                        'page_class': 'form-class-page errors found',
                                        'h1_tag': 'This is the FormClassView Page Using ContactForm<br /><small class="error-msg">Errors Found</small>',
                                        'form': form,
                                    }
                                    )


class ModelFormClassCreateView(CreateView):
    template_name = 'chapter_5/model-form-class.html'
    form_class = VehicleForm
    success_url = '/chapter-5/vehicle-form-success/'

    def get(self, request, *args, **kwargs):
        buyer_formset = ProspectiveBuyerFormSet()
        return TemplateResponse(
            request,
            self.template_name,
            {
                'title': 'ModelFormClassCreateView Page',
                'page_id': 'model-form-class-id',
                'page_class': 'model-form-class-page',
                'h1_tag': 'This is the ModelFormClassCreateView Class Page Using VehicleForm',
                'form': self.form_class(),
                'buyer_formset': buyer_formset,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        buyer_formset = ProspectiveBuyerFormSet(
            request.POST)
        if form.is_valid():
            vehicle = form.instance
            vehicle.save()
            return HttpResponseRedirect(
                self.success_url
            )
        else:
            return TemplateResponse(
                request,
                self.template_name,
                {
                    'title': 'ModelFormClassCreateView Page - Please Correct The Errors Below',
                    'page_id': 'model-form-class-id',
                    'page_class': 'model-form-class-page errors-found',
                    'h1_tag': 'This is the ModelFormClassCreateView Page Using VehicleForm<br/><small class="error-msg">Errors Found</small>',
                    'form': form,
                    'buyer_formset': buyer_formset,
                }
            )


class ModelFormClassUpdateView(UpdateView):
    template_name = 'chapter_5/model-form-class.html'
    form_class = VehicleForm
    success_url = '/chapter-5/vehicle-form-success/'

    def get(self, request, id, *args, **kwargs):
        try:
            vehicle = Vehicle.objects.get(pk=id)
        except Vehicle.DoesNotExist:
            form = self.form_class()
        else:
            form = self.form_class(instance=vehicle)
        return TemplateResponse(
            request,
            self.template_name,
            {
                'title': 'ModelFormClassUpdateView Page',
                'page_id': 'model-form-class-id',
                'page_class': 'model-form-class-page',
                'h1_tag': 'This is the ModelFormClassUpdateView Class Page Using VehicleForm',
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            vehicle = form.instance
            vehicle.save()
            return HttpResponseRedirect(
                self.success_url
            )
        else:
            return TemplateResponse(
                request,
                self.template_name,
                {
                    'title': 'ModelFormClassCreateView Page - Please Correct The Errors Below',
                    'page_id': 'model-form-class-id',
                    'page_class': 'model-form-class-page errors-found',
                    'h1_tag': 'This is the ModelFormClassCreateView Page Using VehicleForm<br/><small class="error-msg">Errors Found</small>',
                    'form': form,
                }
            )
