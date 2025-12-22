from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib import messages
from .models import Service, Category, GalleryImage, ContactMessage

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6] # Featured
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ServiceListView(ListView):
    model = Category
    template_name = 'core/services.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.prefetch_related('services').all()

class GalleryView(ListView):
    model = GalleryImage
    template_name = 'core/gallery.html'
    context_object_name = 'images'

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'core/contact.html')
