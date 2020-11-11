from django.contrib import messages
from django.shortcuts import render
from django.utils.safestring import mark_safe
from friendship.models import Friend


def homepage_view(request):
    context = {
    }
    if request.user.is_authenticated:
        friendship_requests = Friend.objects.requests(request.user)
        for frq in friendship_requests:
            msg = "{0} wants to be friends with you! <a href='#' id='frq_accept' onclick='accept_frq(\"{1}\");'>Accept</a> | <a id='frq_reject' href='#'>Reject</a>".format(frq.from_user, frq.id)
            messages.info(request, mark_safe(msg))
        context['frqs'] = friendship_requests
    return render(request, "portal/homepage.html", context=context)
