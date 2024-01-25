# flake8: noqa E501
from django_apscheduler.models import DjangoJobExecution

from django.contrib.auth.models import User
from whiteboard.models import Post, Category

from datetime import timedelta, datetime, time
from django.utils import timezone

from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.core.mail import  EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string


def delete_old_job_executions(max_age=604_800):
    """
        This job deletes all apscheduler job executions older
        than `max_age` from the database.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def testing_job(message=None):
    if message is not None:
        print(message)
    print(f'Job is done, scheduler work. {timezone.now().ctime()}')


def now_notice_create_post(fields):
    subscriber_users = fields.category.values_list(
        'subscribers',
        'subscribers__email',
    ).order_by('subscribers').distinct()
    subscriber_users_gen = ((id, email) for id, email in subscriber_users if id is not None)
    messages = []
    for user_id, email in subscriber_users_gen:
        user_full_name = User.objects.get(pk=user_id).get_full_name()
        subject = fields.header
        body = fields.text if len(fields.text) < 51 else fields.text[:50] + '...'
        from_email = DEFAULT_FROM_EMAIL
        to = email
        context = {
            'header': subject,
            'author': str(fields.author),
            'username': user_full_name,
            'text': body,
            'url': fields.get_absolute_url()
        }
        html_context = render_to_string(
            './email/newsletter_new_news_detail.html', context
        )
        msg = EmailMultiAlternatives(
            subject= subject,
            body=body,
            from_email=from_email,
            to=[to]
        )
        msg.attach_alternative(html_context, 'text/html')
        messages.append(msg)
    with get_connection(fail_silently=False) as connection:
        connection.send_messages(messages)


def week_notice_added_new_posts():
    current_date = datetime.now().date()
    midnight = time(0,0)
    end_week = timezone.make_aware(datetime.combine(current_date, midnight))
    # записи за предыдущие семь дней
    post_list = Post.objects.filter(time__gte=end_week - timedelta(days=7)).filter(time__lt=end_week)
    # получение категорий этих статей
    category_qs = post_list.values('category', 'category__name').order_by('category').distinct()
    category_gen = ((cat.get('category'), cat.get('category__name')) for cat in category_qs)
    for cat_id, cat_name in category_gen:
        email_list = list(
            Category.objects.filter(pk=cat_id).values_list('subscribers__email', flat=True)
        )
        context = {
            'title': f'Еженедельная подборка новостей в категории { cat_name.lower() }.',
            # генерируем контент для text/html части письма
            'news': post_list.filter(category=cat_id)
        }
        html_context = render_to_string('./email/newsletter_new_news_table.html', context)
        # генерируем контент для text/plain части письма
        post_gen = (p for p in context.get('news').values(
            'id',
            'header',
            'author__user__first_name',
            'author__user__last_name',
            'time',
            'text',
            )
        )
        context.update(message_plain=f'{context.get("title")}\n\n {"—":—<118} \n')
        thead_header = '| Заголовок'.ljust(38, ' ')
        thead_author = f'{"| Автор":<26}{"[дата]":<19}'
        thead_link = f'{"| Ссылка":<36}|\n'
        thead = f'{context.get("message_plain")}{thead_header}{thead_author}{thead_link}'
        context.update(message_plain=thead)
        for post in post_gen:
            header = f'| {post.get("header")[:35]:<36}'
            author = f'{post.get("author__user__first_name")} {post.get("author__user__last_name")}'
            author = f'| {author[:24]:<24}[{post.get("time"):%d-%m-%Y %H:%M}] '
            link = f'| http://127.0.0.1:8000/news/{post.get("id"):<7}|\n'
            trow = f'{context.get("message_plain")}{header}{author}{link}'
            context.update(message_plain=trow)
        context.update(message_plain=f'{context.get("message_plain")}{" —":—<118} \n')
        # print(context.get('message_plain'))
        with get_connection(fail_silently=False) as connection:
            messages = []
            for recipient in email_list:
                msg = EmailMultiAlternatives(
                    subject=context.get('title'),
                    body=context.get('message_plain'),
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[recipient],
                    connection=connection,
                )
                msg.attach_alternative(html_context, 'text/html')
                messages.append(msg)
            connection.send_messages(messages)
