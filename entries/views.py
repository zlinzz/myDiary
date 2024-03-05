from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,

    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Entry
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin

# Define the login_url 

class LockedView(LoginRequiredMixin):
    login_url = "admin:login"

# ---------------------------------------------
# inherit from ListView, LockedView class 
class EntryListView(LockedView, ListView):
    # specify which model should be used for retrieving the data to display in the view
    model = Entry
    # set entries in ascending order by date 
    queryset = Entry.objects.all().order_by("-date_created")

# inherit from DetailView, LockedView class 
class EntryDetailView(LockedView, DetailView):
    model = Entry

# ---------------------------------------------
# CRUD operations 
    
class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    # define which model fields should be displayed in the form
    fields = ["title", "content"]
    # reverse_lazy() is basically a method to retrieve the url by its name 
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"

class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content"]

    # get_success_url - just a general practice when you need to dynamically access to additional context 
    # get_success_url() simply returns the value of success_url
    success_message = "Your entry was updated!"

    def get_success_url(self):
        return reverse_lazy(
            "entry-detail",
            kwargs={"pk": self.object.id}
        )


class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")    
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

