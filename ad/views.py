from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import FlatAd

class FlatAdListView(ListView):
    model = FlatAd

class FlatAdDetailView(DetailView):
    model = FlatAd

def review(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.review()
    return redirect('ad:ad-list')

def unreview(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.unreview()
    return redirect('ad:ad-list')

def interesting(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.mark_interesting()
    return redirect('ad:ad-list')

def notinteresting(request, pk):
    ad = get_object_or_404(FlatAd, pk=pk)
    ad.mark_notinteresting()
    return redirect('ad:ad-list')

def update_ads(request):
    FlatAd.objects.import_last_ads()
    return redirect('ad:ad-list')
