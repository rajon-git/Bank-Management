from django.urls import path
from .views import depositeMoneyView, WithdrawMoneyView, TransactionReportView, LoanRequestView, LoanListView

urlpatterns = [
    path("deposite/", depositeMoneyView.as_view(), name="deposite_money")
    path("report/", TransactionReportView.as_view(), name="transaction_report")
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money")
    path("loan_request/", LoanRequestView.as_view(), name="loan_request")
    path("loans/", LoanListView.as_view(), name="loan_list")
    path("loan/<int:loan_id>/", PayLoanView.as_view(), name="deposite_money")

]
