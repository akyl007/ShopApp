from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MessageForm
from .models import Messenger, Chat


def indexMessenger(request):
    return render(request, 'messenger/index.html')


@login_required
def chat_view(request):
    User = get_user_model()

    admin = get_object_or_404(User, is_superuser=True)

    # Поиск существующего диалога
    chat = Chat.objects.filter(
        Q(user=request.user, admin=admin) |
        Q(user=admin, admin=request.user)
    ).first()

    # Если диалог не найден, создаем новый
    if not chat:
        chat = Chat.objects.create(
            user=request.user,
            admin=admin,
            name=f"Chat between {request.user.username} and {admin.username}"
        )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('messenger:chat_view')
    else:
        form = MessageForm()

    messages = Messenger.objects.filter(chat=chat)

    context = {
        'user': request.user,
        'chat': chat,
        'messages': messages,
        'form': form
    }
    return render(request, 'messenger/index.html', context)


@login_required

def admin_chat_view(request):
    admin = get_object_or_404(get_user_model(), is_superuser=True)
    chats = Chat.objects.filter(admin=admin)

    # Получение сообщений для отображения
    messages = Messenger.objects.filter(chat__in=chats).order_by('created_at')

    context = {
        'admin': admin,
        'chats': chats,
        'messages': messages,
    }
    return render(request, 'messenger/admin_chat.html', context)


def is_admin(user):
    return user.is_superuser

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Пользователь либо админ, либо участник чата
    if request.user != chat.user and not is_admin(request.user):
        return redirect('some_error_page')  # Или другое действие

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Messenger.objects.create(
                chat=chat,
                sender=request.user,
                message=message_text
            )
        return redirect('messenger:admin_chat_view' if request.user.is_superuser else 'messenger:chat_view',
                        chat_id=chat_id)
