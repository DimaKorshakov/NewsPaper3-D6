from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from .models import News, UsersSubscribed, Category
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from datetime import date
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from NewsPaper3.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.models import Site
from .management.commands.runapscheduler import weekly_mail


@receiver(post_save, sender=News)
def notify_managers(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.header} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'News changed for {instance.header} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.description
    )


@login_required
def subscribe(request):
    user = request.user
    subscribers_group = Group.objects.get(name='subscribers')
    if not request.user.groups.filter(name='subscribes').exists():
        subscribers_group.user_set.add(user)
    return redirect('/')


@receiver(post_save, sender=News)
def mail_to_subscribers(sender, instance, created, **kwargs):
    try:
        news = instance
        cat = news.cat.get().id
        header = news.header
        description = news.description[:50]
        current_site = Site.objects.get_current()
        news_link = f"http://{current_site.name}{reverse('details', args=(news.id,))}"
        subscribers_list = UsersSubscribed.objects.filter(category=cat)
        for each in subscribers_list:
            hello_text = f'Здравствуй, {each.user}. Новая статья в твоём любимом разделе!\n'
            html_content = render_to_string('mail_to_subscribers.html',
                                            {'header': header, 'description': description, 'hello_text': hello_text,
                                             'news_link': news_link})
            msg = EmailMultiAlternatives(
                subject=f'{header}',
                body=hello_text + description,
                from_email=EMAIL_HOST_USER,
                to=[each.user.email],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()

    except ObjectDoesNotExist:
        pass


@receiver(weekly_mail)
def weekly_mail(sender, **kwargs):
    categories = Category.objects.all()
    current_site = Site.objects.get_current()
    site_link = f"http://{current_site.name}"
    for category in categories:
        subscribers_list = UsersSubscribed.objects.filter(category=category)
        news = News.objects.filter(cat=category).filter(creation_date_time__week=date.today().isocalendar()[1] - 1)
        if news.count() > 0:
            for each in subscribers_list:
                hello_text = f'Здравствуй, {each.user}. Подборка статей за неделю в твоём любимом разделе {category}!\n'
                header = 'Подборка статей за неделю'
                html_content = render_to_string('weekly_mail.html',
                                                {'header': header, 'hello_text': hello_text, 'news': news,
                                                 'category': category, 'site_link': site_link})
                msg = EmailMultiAlternatives(
                    subject=f'{header}',
                    body=hello_text,
                    from_email=EMAIL_HOST_USER,
                    to=[each.user.email],
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()


# @login_required
# def unsubscribe(request):
#     user = request.user
#     subscribe_group = Group.objects.get(name='unsubscribe')
#     if request.user.groups.filter(name='unsubscribe').exists():
#         subscribe_group.user_set.delete(user)
#     return redirect('/')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
