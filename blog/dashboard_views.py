from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Article
from .forms import CategoryForm, ArticleForm

def staff_only(request):
    return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# ------------- CATEGORY CRUD -------------

@login_required
def category_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    categories = Category.objects.all().order_by('name')
    return render(request, 'dashboard/category/category_list.html', {
        'categories': categories,
    })


@login_required
def category_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm()

    return render(request, 'dashboard/category/category_form.html', {
        'form': form,
        'form_title': 'Add Category',
        'submit_label': 'Create',
    })


@login_required
def category_edit_view(request, category_id):
    if not staff_only(request):
        return redirect('profile')

    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/category/category_form.html', {
        'form': form,
        'form_title': f'Edit Category: {category.name}',
        'submit_label': 'Save',
    })


@login_required
def category_delete_view(request, category_id):
    if not staff_only(request):
        return redirect('profile')

    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        # Will raise ProtectedError if there are still articles using it
        category.delete()
        return redirect('dashboard_category_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': category.name,
        'cancel_url_name': 'dashboard_category_list',
    })


# ------------- ARTICLE CRUD -------------

@login_required
def article_list_view(request):
    if not staff_only(request):
        return redirect('profile')

    # show newest first
    articles = (
        Article.objects
        .select_related('category', 'author')
        .order_by('-published_at')
    )

    return render(request, 'dashboard/articles/article_list.html', {
        'articles': articles,
    })


@login_required
def article_create_view(request):
    if not staff_only(request):
        return redirect('profile')

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            if article.author_id is None:  # if not set by form
                article.author = request.user
            article.save()
            return redirect('dashboard_article_list')
    else:
        form = ArticleForm()

    return render(request, 'dashboard/articles/article_form.html', {
        'form': form,
        'form_title': 'Add Article',
        'submit_label': 'Create',
    })


@login_required
def article_edit_view(request, article_id):
    if not staff_only(request):
        return redirect('profile')

    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('dashboard_article_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'dashboard/articles/article_form.html', {
        'form': form,
        'form_title': f'Edit Article: {article.title}',
        'submit_label': 'Save',
    })


@login_required
def article_delete_view(request, article_id):
    if not staff_only(request):
        return redirect('profile')

    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        return redirect('dashboard_article_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': article.title,
        'cancel_url_name': 'dashboard_article_list',
    })
