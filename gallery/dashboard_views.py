from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artwork, ArtworkFeedback
from .forms import ArtworkForm, ArtworkFeedbackForm

def staff_only(request):
    return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# ------------ ARTWORK CRUD ------------

@login_required
def artwork_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    artworks = Artwork.objects.all().order_by('-created_at')
    return render(request, 'dashboard/artwork/artwork_list.html', {
        'artworks': artworks,
    })


@login_required
def artwork_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)   # <-- ADD request.FILES
        if form.is_valid():
            form.save()
            return redirect('dashboard_artwork_list')
    else:
        form = ArtworkForm()

    return render(request, 'dashboard/artwork/artwork_form.html', {
        'form': form,
        'form_title': 'Add Artwork',
        'submit_label': 'Create',
    })


@login_required
def artwork_edit_view(request, artwork_id):
    if not staff_only(request):
        return redirect('profile')

    artwork = get_object_or_404(Artwork, id=artwork_id)

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)  # <-- files + instance
        if form.is_valid():
            form.save()
            return redirect('dashboard_artwork_list')
    else:
        form = ArtworkForm(instance=artwork)

    return render(request, 'dashboard/artwork/artwork_form.html', {
        'form': form,
        'form_title': f'Edit Artwork: {artwork.title}',
        'submit_label': 'Save',
    })


@login_required
def artwork_delete_view(request, artwork_id):
    if not staff_only(request):
        return redirect('profile')

    artwork = get_object_or_404(Artwork, id=artwork_id)

    if request.method == "POST":
        artwork.delete()
        return redirect('dashboard_artwork_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': artwork.title,
        'cancel_url_name': 'dashboard_artwork_list',
    })


# ------------ FEEDBACK MODERATION CRUD ------------

@login_required
def feedback_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    # newest first, so admin sees recent comments
    feedbacks = (
        ArtworkFeedback.objects
        .select_related('artwork', 'user')
        .order_by('-created_at')
    )

    return render(request, 'dashboard/feedback/feedback_list.html', {
        'feedbacks': feedbacks,
    })


@login_required
def feedback_edit_view(request, feedback_id):
    if not staff_only(request):
        return redirect('profile')

    fb = get_object_or_404(ArtworkFeedback, id=feedback_id)

    if request.method == "POST":
        form = ArtworkFeedbackForm(request.POST, instance=fb)
        if form.is_valid():
            form.save()
            return redirect('dashboard_feedback_list')
    else:
        form = ArtworkFeedbackForm(instance=fb)

    return render(request, 'dashboard/feedback/feedback_form.html', {
        'form': form,
        'form_title': f'Edit Feedback on {fb.artwork.title}',
        'submit_label': 'Save',
    })


@login_required
def feedback_delete_view(request, feedback_id):
    if not staff_only(request):
        return redirect('profile')

    fb = get_object_or_404(ArtworkFeedback, id=feedback_id)

    if request.method == "POST":
        fb.delete()
        return redirect('dashboard_feedback_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f'Feedback on {fb.artwork.title}',
        'cancel_url_name': 'dashboard_feedback_list',
    })
