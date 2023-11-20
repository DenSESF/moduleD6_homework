from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from whiteboard.models import Post, Category

from django.contrib.auth.models import User


@receiver(m2m_changed, sender=Post.category.through)
def notify_add_new_news(sender, instance, action, reverse, pk_set, *args, **kwargs):
    print(f'Signals:m2m_changed:{action}')
    if action == 'post_add':
        category = Category.objects.filter(pk__in=pk_set)
        email_list = list(category.values_list('subscribers__email', flat=True).distinct())
        # text = instance.preview()
        text = instance.text
        if text.count(' ') > 20:
            text = text.split(' ', 20)
            if len(text) > 20:
                text.pop()
                text.append('...')
            text = ' '.join(text)
        context = {
            'category_names': ', '.join(category.values_list('name', flat=True)),
            'text': text,
            'header': instance.header,
            'time': instance.time,
            'author': instance.author.user.get_full_name(),
            'url': instance.get_absolute_url(),
        }
        html_context = render_to_string('./email/newsletter_new_news_detail.html', context)
        with get_connection(fail_silently=False) as connection:
            messages = []
            for recipient in email_list:
                msg = EmailMultiAlternatives(
                    subject=context['header'],
                    body=context['text'],
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[recipient],
                    connection=connection,
                )
                msg.attach_alternative(html_context, 'text/html')
                messages.append(msg)
            connection.send_messages(messages)


# @receiver(post_save, sender=Post)
# def notify_save_post_model(sender, instance, created, *args, **kwargs):
#     if created:
#         print('Signals:Post created')
#     else:
#         print('Signals:Post updated')

@receiver(post_save, sender=User)
def greeting_new_user(sender, instance, created, *args, **kwargs):
    if created:
        username = instance.username
        email = instance.email
        context = {
            'username': username,
            'email': email
        }
        body = f'Вы использовали для регистрации { email }.\n \
            Для завершения регистрации дождитесь письма с верификацией электронной почты.'
        html_context = render_to_string('./email/greeting_new_users.html', context)
        with get_connection(fail_silently=False) as connection:
            msg = EmailMultiAlternatives(
                subject=f'Добро пожаловать, {username}!',
                body=body,
                from_email=DEFAULT_FROM_EMAIL,
                to=[email],
                connection=connection,
            )
            msg.attach_alternative(html_context, 'text/html')
            msg.send()
