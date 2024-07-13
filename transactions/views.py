from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositeForm, WithDrawForm, LoanRequestForm
from .constants import DEPOSIT, WITHDRAWL, LOAN, LOAN_PAID
from django.contrib import messages

# Create your views here.

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = ''
    model = Transaction
    title = ''
    success_url = ''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' : self.title
        })
        return super().get_context_data(**kwargs)
    

class depositeMoneyView(TransactionCreateMixin):
    form_class = DepositeForm
    title = 'Deposite'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request, f"{amount} BDT was deposited to your account succeffully")
        return super().form_valid(form)