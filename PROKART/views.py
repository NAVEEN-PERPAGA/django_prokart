from django.shortcuts import render
from django.views import generic
from .models import Phones, Comments, Ratings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm


class IndexView(generic.ListView):
    context_object_name = 'phones'
    template_name = 'PROKART/index.html'

    def get_queryset(self):
        return Phones.objects.all()


class CreateCommentForm(generic.edit.CreateView):
    model = Comments
    template_name = 'PROKART/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones'] = Phones.objects.get(pk=self.kwargs.get('pk'))
        context['comments'] = Comments.objects.filter(phones=self.kwargs.get('pk'))
        context['ratingE'] = Ratings.objects.get(Q(phone=self.kwargs.get('pk')) & Q(name='E'))
        context['ratingVG'] = Ratings.objects.get(Q(phone=self.kwargs.get('pk')) & Q(name='VG'))
        context['ratingG'] = Ratings.objects.get(Q(phone=self.kwargs.get('pk')) & Q(name='G'))
        context['ratingP'] = Ratings.objects.get(Q(phone=self.kwargs.get('pk')) & Q(name='P'))
        context['ratingVP'] = Ratings.objects.get(Q(phone=self.kwargs.get('pk')) & Q(name='VP'))
        return context

    def get_success_url(self):
        return reverse('prokart:comment', kwargs={'pk': self.kwargs.get('pk')})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(kwargs)
        kwargs['phone_pk'] = self.kwargs.get('pk')
        return kwargs


def voting(request, pk):
    print(request)
    phone = Phones.objects.get(pk=pk)
    ratings = Ratings.objects.filter(phone=phone)

    try:
        selected_rating = Ratings.objects.get(pk=request.POST['rating'])
    except (KeyError, Ratings.DoesNotExist):
        return HttpResponseRedirect(reverse('prokart:comment', args=(pk, )))
    else:
        selected_rating.vote += 1
        selected_rating.save()

        rating_e = phone.ratings_set.get(name='E')
        rating_vg = phone.ratings_set.get(name='VG')
        rating_g = phone.ratings_set.get(name='G')
        rating_p = phone.ratings_set.get(name='P')
        rating_vp = phone.ratings_set.get(name='VP')

        rating_sum = 0
        for rating_object in ratings:
            rating_sum = rating_sum + rating_object.vote

        rating_e.vote_percent = rating_e.vote / rating_sum * 100
        print(rating_e.vote_percent)
        rating_e.save()
        rating_vg.vote_percent = rating_vg.vote / rating_sum * 100
        rating_vg.save()
        rating_g.vote_percent = rating_g.vote / rating_sum * 100
        rating_g.save()
        rating_p.vote_percent = rating_p.vote / rating_sum * 100
        rating_p.save()
        rating_vp.vote_percent = rating_vp.vote / rating_sum * 100
        print(rating_vp.vote_percent)
        rating_vp.save()
    return HttpResponseRedirect(reverse('prokart:comment', args=(pk, )))


def ram_filter(request):
    ram1 = ram2 = ram3 = None

    if '4' in request.GET.getlist('ram'):
        ram1 = 4
    if '6' in request.GET.getlist('ram'):
        ram2 = 6
    if '8' in request.GET.getlist('ram'):
        ram3 = 8

    print(request.GET.getlist('ram'))
    phones = Phones.objects.filter(Q(ram=ram1) | Q(ram=ram2) | Q(ram=ram3))
    return render(request, 'PROKART/index.html', {'phones': phones})


def storage_filter(request):
    storage1 = storage2 = storage3 = None

    if '32' in request.GET.getlist('storage'):
        storage1 = 32
    if '64' in request.GET.getlist('storage'):
        storage2 = 64
    if '128' in request.GET.getlist('storage'):
        storage3 = 128

    print(request.GET)
    phones = Phones.objects.filter(Q(storage=storage1) | Q(storage=storage2) | Q(storage=storage3))
    return render(request, 'PROKART/index.html', {'phones': phones})


def display_filter(request):
    display1 = display2 = display3 = None

    if 'hd' in request.GET.getlist('display'):
        display1 = 'HD'
    if 'fhd' in request.GET.getlist('display'):
        display2 = 'FHD+'
    if 'qhd' in request.GET.getlist('display'):
        display3 = 'QHD'

    phones = Phones.objects.filter(Q(display=display1) | Q(display=display2) | Q(display=display3))
    return render(request, 'PROKART/index.html', {'phones': phones})


def price_filter(request):
    price1 = 0
    price2 = price3 = 1000000
    price4 = price5 = 1000000

    if 'upto 20' in request.GET.getlist('price'):
        price1 = 20000
    if '20-50' in request.GET.getlist('price'):
        price2 = 20000
        price3 = 50000
    if '50-99' in request.GET.getlist('price'):
        price4 = 50000
        price5 = 99000

    phones = Phones.objects.filter(Q(price__lte=price1) |
                                   (Q(price__gte=price2) & Q(price__lte=price3)) |
                                   (Q(price__gte=price4) & Q(price__lte=price5)))
    return render(request, 'PROKART/index.html', {'phones': phones})



