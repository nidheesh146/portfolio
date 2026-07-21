from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request,'index.html')


from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Message from {name} <{email}>:\n\n{message}"

        def send_email_task():
            try:
                send_mail(
                    subject='New Contact Form Submission',
                    message=full_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send email: {e}")

        import threading
        email_thread = threading.Thread(target=send_email_task)
        email_thread.start()

        messages.success(request, 'Your message is being sent!')
        return redirect('index_view')

    return render(request, 'contact.html')  
