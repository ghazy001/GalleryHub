from events.models import Event
from blog.models import Article
from django.shortcuts import  redirect
from gallery.models import Artwork, ArtworkFeedback
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from workshops.models import Workshop
from .forms import ImageGenerateForm
import requests
from django.shortcuts import render
from django.conf import settings
from .forms import ImageGenerateForm, BackgroundRemoveForm , ImageEditorForm
from django.conf import settings
import requests
from django.utils import timezone
from django.shortcuts import render, redirect
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




# ---------------------- workshops --------------------------



def public_workshop_list_view(request):
    now = timezone.now()
    # active and in the future or ongoing
    workshops = (
        Workshop.objects
        .filter(is_active=True, end_time__gte=now)
        .select_related('place')
        .prefetch_related('materials')
        .order_by('start_time')
    )

    return render(request, 'main/workshops/public_workshop_list.html', {
        'workshops': workshops
    })


def public_workshop_detail_view(request, workshop_id):
    workshop = get_object_or_404(
        Workshop.objects.select_related('place').prefetch_related('materials'),
        id=workshop_id,
        is_active=True
    )

    return render(request, 'main/workshops/public_workshop_detail.html', {
        'workshop': workshop
    })





# ---------------------- image generation --------------------------



def ai_image_generator_page(request):
    image_url = None
    error = None

    print("DEBUG KEY:", settings.DEEPAI_API_KEY)

    if request.method == "POST":
        form = ImageGenerateForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]

            try:
                resp = requests.post(
                    "https://api.deepai.org/api/text2img",
                    data={'text': prompt},
                    headers={'api-key': settings.DEEPAI_API_KEY},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()

                image_url = data.get("output_url")
                if not image_url:
                    error = "The AI did not return an image. Try another prompt."

            except requests.exceptions.RequestException as e:
                error = f"Request failed: {e}"
    else:
        form = ImageGenerateForm()

    return render(
        request,
        "main/Ai/generator.html",
        {
            "form": form,
            "image_url": image_url,
            "error": error,
        }
    )


#---------------------- ai background removal --------------------------

def ai_background_remover_page(request):
    output_url = None
    error = None

    if request.method == "POST":
        form = BackgroundRemoveForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data["image"]

            # choose the key source:
            # 1. try env (recommended, like before)
            # 2. fallback hardcoded for dev ONLY
            api_key = getattr(settings, "DEEPAI_API_KEY", None) or "94242180-9293-4b4f-af09-f9e3fe00b173"

            try:
                resp = requests.post(
                    "https://api.deepai.org/api/background-remover",
                    headers={"api-key": api_key},
                    files={
                        "image": (img_file.name, img_file.read())
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()

                # DeepAI usually returns {"output_url": "..."}
                output_url = data.get("output_url")
                if not output_url:
                    error = "The AI did not return a processed image. Try another file."

            except requests.exceptions.RequestException as e:
                error = f"Request failed: {e}"

        else:
            error = "Invalid form. Please upload an image."
    else:
        form = BackgroundRemoveForm()

    return render(
        request,
        "main/Ai/background_remove.html",
        {
            "form": form,
            "output_url": output_url,
            "error": error,
        }
    )


#---------------------- ai image editor --------------------------
def ai_photo_editor_page(request):
    output_url = None
    error = None

    if request.method == "POST":
        form = ImageEditorForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data["image"]
            edit_text = form.cleaned_data["text"]

            api_key = getattr(settings, "DEEPAI_API_KEY", None) or "94242180-9293-4b4f-af09-f9e3fe00b173"

            try:
                resp = requests.post(
                    "https://api.deepai.org/api/image-editor",
                    headers={"api-key": api_key},
                    files={
                        "image": (img_file.name, img_file.read()),
                    },
                    data={
                        "text": edit_text,
                    },
                    timeout=40,
                )
                resp.raise_for_status()
                data = resp.json()

                output_url = data.get("output_url")
                if not output_url:
                    error = "The AI did not return an edited image. Try adjusting your edit text."

            except requests.exceptions.RequestException as e:
                error = f"Request failed: {e}"
        else:
            error = "Please provide an image and edit instructions."
    else:
        form = ImageEditorForm()

    return render(
        request,
        "main/Ai/photo_editor.html",
        {
            "form": form,
            "output_url": output_url,
            "error": error,
        }
    )



