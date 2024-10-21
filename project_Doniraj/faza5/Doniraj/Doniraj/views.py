from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Organization
from django.db.models import Max
#Author:Marija Stakic 2021/0320

def organizacije(request):
    organizations = Organization.objects.filter(accepted = True).all()
    return render(request, 'organizacije.html', {'organizations': organizations})

def organizacijaProfil(request):
    user_organization = Organization.objects.filter(user=request.user).first()
    return render(request, 'organizacijaProfil.html', {'user_organization': user_organization})

def organizacijaOglas(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    return render(request, 'organizacijaOglas.html', {'organization': organization})

@login_required
def inbox(request):
    chat_groups = request.user.chat_groups.filter(is_private=True)
    sorted_chat_groups = chat_groups.annotate(last_message_time=Max('chat_messages__created')).order_by('-last_message_time')
    return render(request, 'inbox.html', {'sorted_chat_groups': sorted_chat_groups})



