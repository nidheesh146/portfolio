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

        send_mail(
            subject='New Contact Form Submission',
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # send to yourself
            fail_silently=False,
        )
        messages.success(request,'Your message has been sent!')
        return redirect('index_view')

    return render(request, 'contact.html')  
