from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workshop, Material
from .forms import WorkshopForm, MaterialForm

def staff_only(request):
    return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# ----- MATERIAL CRUD -----

@login_required
def material_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    materials = Material.objects.all().order_by('name')
    return render(request, 'dashboard/material/material_list.html', {
        'materials': materials,
    })


@login_required
def material_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_material_list')
    else:
        form = MaterialForm()

    return render(request, 'dashboard/material/material_form.html', {
        'form': form,
        'form_title': 'Add Material',
        'submit_label': 'Create',
    })


@login_required
def material_edit_view(request, material_id):
    if not staff_only(request):
        return redirect('profile')

    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('dashboard_material_list')
    else:
        form = MaterialForm(instance=material)

    return render(request, 'dashboard/material/material_form.html', {
        'form': form,
        'form_title': f'Edit Material: {material.name}',
        'submit_label': 'Save',
    })


@login_required
def material_delete_view(request, material_id):
    if not staff_only(request):
        return redirect('profile')

    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        material.delete()
        return redirect('dashboard_material_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': material.name,
        'cancel_url_name': 'dashboard_material_list',
    })


# ----- WORKSHOP CRUD -----

@login_required
def workshop_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    workshops = (
        Workshop.objects
        .select_related('place')
        .prefetch_related('materials')
        .order_by('-start_time')
    )

    return render(request, 'dashboard/workshops/workshop_list.html', {
        'workshops': workshops,
    })


@login_required
def workshop_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_workshop_list')
    else:
        form = WorkshopForm()

    return render(request, 'dashboard/workshops/workshop_form.html', {
        'form': form,
        'form_title': 'Add Workshop',
        'submit_label': 'Create',
    })


@login_required
def workshop_edit_view(request, workshop_id):
    if not staff_only(request):
        return redirect('profile')

    workshop = get_object_or_404(Workshop, id=workshop_id)

    if request.method == "POST":
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid():
            form.save()
            return redirect('dashboard_workshop_list')
    else:
        form = WorkshopForm(instance=workshop)

    return render(request, 'dashboard/workshops/workshop_form.html', {
        'form': form,
        'form_title': f'Edit Workshop: {workshop.title}',
        'submit_label': 'Save',
    })


@login_required
def workshop_delete_view(request, workshop_id):
    if not staff_only(request):
        return redirect('profile')

    workshop = get_object_or_404(Workshop, id=workshop_id)

    if request.method == "POST":
        workshop.delete()
        return redirect('dashboard_workshop_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': workshop.title,
        'cancel_url_name': 'dashboard_workshop_list',
    })
