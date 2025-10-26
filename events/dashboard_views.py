# events/dashboard_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Place, Event
from .forms import PlaceForm, EventForm

def staff_only(request):
    return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# ---------- PLACES ----------

@login_required
def place_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    places = Place.objects.all().order_by('name')
    return render(request, 'dashboard/places/place_list.html', {
        'places': places,
    })


@login_required
def place_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_place_list')
    else:
        form = PlaceForm()

    return render(request, 'dashboard/places/place_form.html', {
        'form': form,
        'form_title': 'Add Place',
        'submit_label': 'Create',
    })


@login_required
def place_edit_view(request, place_id):
    if not staff_only(request):
        return redirect('profile')

    place = get_object_or_404(Place, id=place_id)

    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect('dashboard_place_list')
    else:
        form = PlaceForm(instance=place)

    return render(request, 'dashboard/places/place_form.html', {
        'form': form,
        'form_title': f'Edit Place: {place.name}',
        'submit_label': 'Save',
    })


@login_required
def place_delete_view(request, place_id):
    if not staff_only(request):
        return redirect('profile')

    place = get_object_or_404(Place, id=place_id)

    if request.method == "POST":
        # because of on_delete=PROTECT in Event.place,
        # this will raise error if there are still events using this place
        place.delete()
        return redirect('dashboard_place_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': place.name,
        'cancel_url_name': 'dashboard_place_list',
    })


# ---------- EVENTS ----------

@login_required
def event_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    events = Event.objects.all().select_related('place').order_by('-start_date')
    return render(request, 'dashboard/events/event_list.html', {
        'events': events,
    })


@login_required
def event_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_event_list')
    else:
        form = EventForm()

    return render(request, 'dashboard/events/event_form.html', {
        'form': form,
        'form_title': 'Add Event',
        'submit_label': 'Create',
    })


@login_required
def event_edit_view(request, event_id):
    if not staff_only(request):
        return redirect('profile')

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard_event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'dashboard/events/event_form.html', {
        'form': form,
        'form_title': f'Edit Event: {event.title}',
        'submit_label': 'Save',
    })


@login_required
def event_delete_view(request, event_id):
    if not staff_only(request):
        return redirect('profile')

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect('dashboard_event_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': event.title,
        'cancel_url_name': 'dashboard_event_list',
    })
