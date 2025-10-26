
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from events.models import Event
from django.utils.timezone import now
from blog.models import Article, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from gallery.models import Artwork, ArtworkFeedback
from gallery.forms import ArtworkFeedbackForm
from django.contrib import messages

def index(request):
    return render(request, 'main/index.html')


# ---------------------- events --------------------------

def public_events_list_view(request):
    events = (
        Event.objects
        .filter(is_published=True)
        .select_related('place')
        .order_by('start_date')
    )
    return render(request, 'main/events/public_events_list.html', {
        'events': events
    })


def public_event_detail_view(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related('place'),
        id=event_id,
        is_published=True
    )
    return render(request, 'main/events/public_event_detail.html', {
        'event': event
    })


# ---------------------- blog --------------------------

def public_article_list_view(request):
    articles = (
        Article.objects
        .filter(is_published=True)
        .select_related('category', 'author')
        .order_by('-published_at')
    )
    return render(request, 'main/articles/public_blog_list.html', {
        'articles': articles
    })


def public_article_detail_view(request, article_id):
    article = get_object_or_404(
        Article.objects.select_related('category', 'author'),
        id=article_id,
        is_published=True
    )
    return render(request, 'main/articles/public_blog_detail.html', {
        'article': article
    })


 # ---------------------- gallery --------------------------


def public_artwork_list_view(request):
    """
    Show all visible artworks to visitors.
    """
    artworks = Artwork.objects.filter(is_visible=True).order_by('-created_at')
    return render(request, 'main/artwork/public_artwork_list.html', {
        'artworks': artworks
    })


def public_artwork_detail_view(request, artwork_id):
    """
    Show 1 artwork + approved feedback.
    Also handle POST form to submit new feedback.
    """
    artwork = get_object_or_404(
        Artwork,
        id=artwork_id,
        is_visible=True
    )

    # Approved feedback only
    approved_feedback = ArtworkFeedback.objects.filter(
        artwork=artwork,
        is_approved=True
    ).select_related('user').order_by('-created_at')

    # --- Handle feedback form submission ---
    if request.method == "POST":
        # Build a form manually instead of using ArtworkFeedbackForm directly,
        # because we don't want users to control is_approved, user, etc.
        name = request.POST.get("name", "").strip()
        comment = request.POST.get("comment", "").strip()
        rating = request.POST.get("rating", "").strip()

        # simple validation
        if not rating.isdigit():
            rating_val = 5
        else:
            rating_val = int(rating)
            if rating_val < 1:
                rating_val = 1
            if rating_val > 5:
                rating_val = 5

        if comment == "":
            messages.error(request, "Comment cannot be empty.")
        else:
            fb = ArtworkFeedback(
                artwork=artwork,
                comment=comment,
                rating=rating_val,
                created_at=timezone.now(),
                is_approved=False  # VERY IMPORTANT: not public yet
            )

            # Attach user if logged in
            if request.user.is_authenticated:
                fb.user = request.user
                # If user is logged in, we can auto-fill display name later in template using fb.user.username
            else:
                fb.name = name or "Anonymous"

            fb.save()
            messages.success(request, "Thanks! Your feedback was submitted and is waiting for approval.")
            # redirect after POST so refresh doesn't re-post the form
            return redirect('public_artwork_detail', artwork_id=artwork.id)

    # Blank form defaults
    initial_name = ""
    if request.user.is_authenticated:
        # We can prefill with username for logged-in users
        initial_name = request.user.username

    context = {
        'artwork': artwork,
        'approved_feedback': approved_feedback,
        'initial_name': initial_name,
    }
    return render(request, 'main/artwork/public_artwork_detail.html', context)