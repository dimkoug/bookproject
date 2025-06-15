from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings



from core.functions import is_ajax
from core.mixins import *
from core.views import *
from .forms import *


class PublisherListView(BaseListView):

    model = Publisher
    queryset = Publisher.objects.select_related('profile')
    paginate_by = settings.PAGINATED_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
    
    
class PublisherDetailView(BaseDetailView):
    model = Publisher

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
    
class PublisherCreateView(BaseCreateView):
    model = Publisher
    form_class = PublisherForm


    def form_valid(self,form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)



class PublisherUpdateView(BaseUpdateView):
    model = Publisher
    form_class = PublisherForm




class PublisherDeleteView(BaseDeleteView):
    model = Publisher
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
    
    
    
class PublishingContractListView(BaseListView):

    model = PublishingContract
    queryset = PublishingContract.objects.select_related('author','author__profile', 'publisher')
    paginate_by = settings.PAGINATED_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author__profile_id=self.request.user.profile.id)
        return queryset
    
    
class PublishingContractDetailView(BaseDetailView):
    model = PublishingContract

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author__profile')
        queryset = queryset.filter(author__profile_id=self.request.user.profile.id)
        return queryset
    
class PublishingContractCreateView(BaseCreateView):
    model = PublishingContract
    form_class = PublishingContractForm


    # def form_valid(self,form):
    #     form.instance.profile = self.request.user.profile
    #     form.save()
    #     return super().form_valid(form)



class PublishingContractUpdateView(BaseUpdateView):
    model = PublishingContract
    form_class = PublishingContractForm




class PublishingContractDeleteView(BaseDeleteView):
    model = PublishingContract
    ajax_partial = 'partials/ajax_delete_modal.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author__profile')
        queryset = queryset.filter(author__profile_id=self.request.user.profile.id)
        return queryset