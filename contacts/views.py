from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id = user_id)
            if has_contacted:
                messages.error(request,"YOu have already made an enquiry to this listing")
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        send_mail(
            'Property Listing Enquiry',
            "An Enquiry has been sent to " + listing + ' sign in to admin panel to respond',
            'dhirajhouses@gmail.com',
            [realtor_email,'dhirajdev2001@gmail.com'],
            fail_silently=False,
            auth_user=None, auth_password=None, connection=None, html_message=None

        )



        messages.success(request, 'Your request has been Submitted, a realtor will get back to you Shortly!')
        return redirect('/listings/'+listing_id)

