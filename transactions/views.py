from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositeForm, WithDrawForm, LoanRequestForm
from .constants import DEPOSIT, WITHDRAWL, LOAN, LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db import Sum

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
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithDrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWL}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance -= amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request, f"Successfully withdraw from your account {amount} BDT")
        return super().form_valid(form)
    

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request for Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(account = self.request.user.account , transaction_type = 3, loan_approve=True).count()

        if current_loan_count > 3:
            return HttpResponse("You have cross your limit")
        messages.success(self.request, f"Loan request for {amount} BDT have been successfully send to the admin")
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = ""
    model = Transaction 
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account= self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%y-%m-%d").date()

            # queryset = queryset.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date)

            self.balance = Transaction.objects.filter(timestamp_date_gte = start_date, timestamp_date_lte = end_date).aggregate(Sum('amount'))['amount_sum']

        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account' : self.request.user.account
        })
        return context