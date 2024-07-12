from django import forms 
from .models import Transaction 

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super.__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositeForm(TransactionForm):
    def clean_ammount(self): # filter amount field
        min_deposite_ammount = 100
        amount = self.cleaned_data.get('amount')

        if amount < min_deposite_ammount:
            raise forms.ValidationError(
                f'You need to deposite at least (min_deposite_ammount) BDT'
            )
        return amount

class WithDrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at leat {min_withdraw_amount} BDT'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} BDT'
            )
        
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} BDT in your account. You can not withdraw more than your balance'
            )
        return amount
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.changed_data.get('amount')
        return amount

