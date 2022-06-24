#Django Imports
from django.shortcuts import render
from django.views import View

#My App imports
class HomeView(View):
    def get(self, request):
        return render(request,'basics/index.html')