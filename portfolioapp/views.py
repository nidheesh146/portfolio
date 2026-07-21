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
            import requests
            try:
                resend_api_key = getattr(settings, 'RESEND_API_KEY', '')
                if not resend_api_key:
                    print("Failed to send email: RESEND_API_KEY is not configured in settings.")
                    return
                
                headers = {
                    'Authorization': f'Bearer {resend_api_key}',
                    'Content-Type': 'application/json',
                }
                
                data = {
                    "from": "onboarding@resend.dev",
                    "to": [settings.EMAIL_HOST_USER], # Send it to your own email
                    "subject": "New Portfolio Contact Form Submission",
                    "text": full_message,
                }
                
                response = requests.post('https://api.resend.com/emails', headers=headers, json=data)
                response.raise_for_status()
                print("Email sent successfully via Resend!")
            except Exception as e:
                print(f"Failed to send email via Resend: {e}")

        import threading
        email_thread = threading.Thread(target=send_email_task)
        email_thread.start()

        messages.success(request, 'Your message is being sent!')
        return redirect('index_view')

    return render(request, 'contact.html')  
