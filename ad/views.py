from django.core.urlresolvers import reverse_lazy

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import StreetForm
from .models import FlatAd, Street

class FlatAdListView(ListView):
    model = FlatAd
    paginate_by = 15

class FlatAdDetailView(DetailView):
    model = FlatAd

class AddressCreateView(CreateView):
    model = Street
    exclude = ['ad']
    form_class = StreetForm

    def form_valid(self, form):
        form.instance.ad = get_object_or_404(FlatAd, pk=self.kwargs['pk'])
        return super(AddressCreateView, self).form_valid(form)

class AddressUpdateView(UpdateView):
    model = Street
    exclude = ['ad']
    form_class = StreetForm

def review(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.review()
    try:
        next_ad = FlatAd.objects.filter(reviewed=False).last().pk
        return redirect('ad:ad-detail', pk=next_ad)
    except:
        return redirect('ad:ad-list')

def unreview(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.unreview()
    return redirect('ad:ad-list')

def interesting(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.mark_interesting()
    try:
        next_ad = FlatAd.objects.filter(reviewed=False).last().pk
        return redirect('ad:ad-detail', pk=next_ad)
    except:
        return redirect('ad:ad-list')

def notinteresting(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.mark_notinteresting()
    return redirect('ad:ad-list')

def update_ads(request):
    FlatAd.objects.import_last_ads()
    return redirect('ad:ad-list')
