from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            body = render_to_string('subscription_email.txt', form.cleaned_data)

            mail.send_mail('Confirmação de Inscrição',
                           body,
                           'contato@eventex.com',
                           ['contato@eventex.com', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com sucesso')

            return HttpResponseRedirect('/subscription/')
        else:
            return render(request, 'subscription_form.html', {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscription_form.html', context)
