import os

from django.core.paginator import Paginator
from .models import Author
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Tag, Picture
from .forms import QuoteForm, TagForm, AuthorForm, PictureForm
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings



def main(request, page=1):
    quotes = Quote.objects.all()
    tags = Tag.objects.annotate(quote_count=Count('quote')).order_by('-quote_count')
    top_tags = tags[:10]
    per_page = 15
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'tags': top_tags})


def add_quote(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:

                selected_tag = form.cleaned_data['tags'][0]
                new_quote = form.save()
                new_quote.tags.add(selected_tag)
                return redirect(to="quotes:root")
            except ValueError as err:
                return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': QuoteForm(), 'error': err})
    return render(request, 'quotes/add_quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                tag = form.save()
                return redirect('quotes:root')
            except IntegrityError as err:
                return render(request, 'quotes/add_tag.html', {'form': form, 'error': f'IntegrityError: {err}'})
            except ValueError as err:
                return render(request, 'quotes/add_tag.html', {'form': TagForm(), 'error': err})
        else:
            return render(request, 'quotes/add_tag.html', {'form': form, 'error': form.errors})
    else:
        return render(request, 'quotes/add_tag.html', {'form': TagForm()})



@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('quotes:root')
            except IntegrityError as err:
                return render(request, 'quotes/add_author.html', {'form': form, 'error': f'IntegrityError: {err}'})
            except ValueError as err:
                return render(request, 'quotes/add_author.html', {'form': AuthorForm(), 'error': err})
        else:
            print(f'Form is not valid: {form.errors}')
            return render(request, 'quotes/add_author.html', {'form': form, 'error': form.errors})
    else:
        return render(request, 'quotes/add_author.html', {'form': AuthorForm()})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes_by_author = author.quote_set.all()

    context = {'author': author, 'quotes_by_author': quotes_by_author}
    return render(request, 'quotes/author_detail.html', context)

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    context = {'tag': tag, 'quotes_10':quotes}
    return render(request, 'quotes/tag_detail.html', context)

@login_required
def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})


@login_required
def delete_quote(request, quote_id):
    quote = Quote.objects.get(pk= quote_id)
    quote.delete()
    messages.success(request, 'Quote successfully deleted!')
    return render(request, 'quotes/quote_edit_deleted.html')

@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote successfully edited!')
            return render(request, 'quotes/quote_edit_deleted.html')
    else:
        form = QuoteForm(instance=quote)

    return render(request, 'quotes/quote_edit.html', {'form': form, 'quote': quote})


@login_required
def upload(request):
    form = PictureForm(instance=Picture())
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        if form.is_valid():
            form.save()
            return redirect('quotes:root')
    return render(request, 'quotes/upload.html', context={"form": form})



@login_required
def pictures(request):
    pictures = Picture.objects.all()
    return render(request, 'quotes/picture.html', context={"pictures": pictures})


@login_required
def edit_picture(request, pic_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        Picture.objects.filter(pk=pic_id).update(description=description)
        return redirect('quotes:root')
    picture = Picture.objects.filter(pk=pic_id).first()
    return render(request, "quotes/edit_picture.html",
           context={"pic": picture, "media": settings.MEDIA_URL})


@login_required
def remove_picture(request, pic_id):
    picture = Picture.objects.filter(pk=pic_id)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(picture.first().path)))
    except OSError as err:
        print(err)
    picture.delete()
    return redirect('quotes:root')