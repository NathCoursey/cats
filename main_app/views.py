from django.shortcuts import render
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views.generic.base import TemplateView
from .models import Artist, Artwork, Artgallery
from django.views.generic import DetailView
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artgallerys"] = Artgallery.objects.all()
        return context


class About(TemplateView):
    template_name = "about.html"

@method_decorator(login_required, name='dispatch')
class ArtistList(TemplateView):
    template_name = "artist_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["artists"] = Artist.objects.filter(name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for {name}"
        else:
            context["artists"] = Artist.objects.filter(user=self.request.user)
            context["header"] = "Trending Cats"
        return context

class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio']
    template_name = "artist_create.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArtistCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artgallerys"] = Artgallery.objects.all()
        return context

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"
    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDelete(DeleteView):
    model = Artist
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"


class ArtworksCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        image = request.POST.get("image")
        length = request.POST.get("length")
        artist = Artist.objects.get(pk=pk)
        Artwork.objects.create(title=title, length=length, artist=artist)
        return redirect('artist_detail', pk=pk)


class ArtgalleryArtworksAssoc(View):

    def get(self, request, pk, artworks_pk):
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            Artgallery.objects.get(pk=pk).artworks.remove(artworks_pk)
        if assoc == "add":
            Artgallery.objects.get(pk=pk).artworks.add(artworks_pk)
        return redirect('home')

class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)



