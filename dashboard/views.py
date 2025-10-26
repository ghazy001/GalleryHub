from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
from django.db.models import Q

# Only staff/superusers can access this

@login_required
def dashboard_view(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('profile')
    return render(request, 'dashboard/index.html')


@login_required
def user_list_view(request):
    # only staff/superuser allowed
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('')

    # optional: search by username or email with ?q=something
    q = request.GET.get("q", "")
    if q:
        users = User.objects.filter(
            Q(username__icontains=q) | Q(email__icontains=q)
        ).order_by('id')
    else:
        users = User.objects.all().order_by('id')

    context = {
        "users": users,
        "search_query": q,
    }
    return render(request, 'dashboard/users.html', context)


@login_required
def user_ban_toggle_view(request, user_id):
    # only staff/superuser allowed
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('profile')

    # Only allow POST (safety: no GET side effects)
    if request.method != "POST":
        return redirect('dashboard_user_list')

    target = get_object_or_404(User, id=user_id)

    # Safety rule: don't ban yourself
    if target.id == request.user.id:
        messages.error(request, "You cannot ban yourself.")
        return redirect('dashboard_user_list')

    # Flip ban status
    target.is_banned = not target.is_banned
    target.save()

    if target.is_banned:
        messages.warning(request, f"{target.username} is now banned.")
    else:
        messages.success(request, f"{target.username} is now unbanned.")

    return redirect('dashboard_user_list')


@login_required
def user_delete_view(request, user_id):
    # only staff/superuser allowed
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('profile')

    # Only allow POST deletes
    if request.method != "POST":
        return redirect('dashboard_user_list')

    target = get_object_or_404(User, id=user_id)

    # Safety rule: don't delete yourself
    if target.id == request.user.id:
        messages.error(request, "You cannot delete your own account.")
        return redirect('dashboard_user_list')

    username = target.username
    target.delete()
    messages.error(request, f"User '{username}' has been deleted.")

    return redirect('dashboard_user_list')