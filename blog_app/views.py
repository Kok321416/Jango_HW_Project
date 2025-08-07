from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import F
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_app/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_app/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = F('views_count') + 1
        obj.save()
        obj.refresh_from_db()
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog_app/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog_app:blogpost_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog_app/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse_lazy('blog_app:blogpost_detail', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog_app/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog_app:blogpost_list')

