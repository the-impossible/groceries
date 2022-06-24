#Django Imports
from django.shortcuts import render
from django.views import View

#My App imports
class HomeView(View):
    def get(self, request):
        return render(request,'basics/index.html')

class AboutView(View):
    def get(self, request):
        return render(request,'basics/about.html')

class ProductView(View):
    def get(self, request):
        return render(request,'basics/product.html')

class ContactView(View):
    def get(self, request):
        return render(request,'basics/contact.html')