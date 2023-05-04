from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView, View

from NewsPaper3.settings import EMAIL_HOST_USER
from .models import News, Category, UsersSubscribed
from .forms import DummyForm
from .filters import NewsFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsList(LoginRequiredMixin, ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'newses'  #
    # form_class = DummyForm
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = DummyForm()
        return context

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     form.save()
        header = request.POST['header']
        description = request.POST['description']
        cat = request.POST['cat']
        subscribers_list = UsersSubscribed.objects.filter(category=cat)
        for each in subscribers_list:
            print(each)
            hello_text = f'Здравствуй, {each.user}. Новая статья в твоём любимом разделе!\n'
            html_content = render_to_string('mail_to_subscribers.html',
                                            {'header': header, 'description': description, 'hello_text': hello_text, })
            msg = EmailMultiAlternatives(
                subject=f'{header}',
                body=hello_text + description[:50],
                from_email=EMAIL_HOST_USER,
                to=[each.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        # send_mail(
        #     subject='test',
        #     message='Здравствуй , Новая статья в твоём любимом разделе',
        #     from_email='',
        #     recipient_list=['']
        # )
        #
        return super().get(request, *args, **kwargs)


class Search(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'news'  #
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = News.objects.all()


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    # form_class = DummyForm
    permission_required = ('news3.add_news',)
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    form_class = DummyForm
    permission_required = ('news3.add_news',)
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = News.objects.all()
    success_url = '/news/'
    permission_required = ('news3.delete_news',)


class CategoryView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class CatsView(DetailView):
    template_name = 'cats.html'
    queryset = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['newses'] = News.objects.all()
        context['is_not_subscribers'] = not self.request.user.groups.filter(name='subscribers').exists()
        return context


class SubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'subscribe.html'
    model = UsersSubscribed
    context_object_name = 'subscribe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        UsersSubscribed.objects.create(user=self.request.user, category=Category.objects.get(pk=context['pk']))
        context['subscribed'] = Category.objects.get(pk=context['pk'])
        return context


class UnSubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'unsubscribe.html'
    model = UsersSubscribed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        UsersSubscribed.objects.filter(user=self.request.user, category=Category.objects.get(pk=context['pk'])).delete()
        context['unsubscribed'] = Category.objects.get(pk=context['pk'])
        return context
