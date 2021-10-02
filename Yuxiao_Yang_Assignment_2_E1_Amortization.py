### Assignment_2_E1_Amortization
## Yuxiao_Yang

# User Inputs Setting :
##"principal","minimium expected payment","interest",and "extra payment"##

Original_principal = input('Please Enter the Principal ?') 
minimium_expected_payment = input('Please Enter the minimium expected payment ?')
interest_rate = input('Please Enter the Interest Rate ?')
extra_payment =input('Please Enter the Extra_Payment ?')



# when Month=1, Begin P =principal, when Month >1, Begin P = End P of last month

month = list[range(1,181)]
if month == 1:
    Begin_principal = Original_principal
elif month > 1: 
    Begin_principal = End_principal
      
Interest =  Begin_principal * interest_rate / 12

payment = minimium_expected_payment

Payment_applied = minimium_expected_payment - Interest + extra_payment    

End_principal = Begin_principal - Payment_applied 



# Formatted Output
from prettytable import PrettyTable
x = PrettyTable()
print(x)

##
for field_name in x. fild_names
x.field_names = ['Month','Begin Principal','Payment','Interest','Extra Payment,','Applied Payment','End Principal']
x.add_column ('Month',list[range(1,181)])
x.add_column('Begin Principal',[Begin_principal])
x.add_column('Payment',[payment])
x.add_column('Interest',[Interest])
x.add_column('Extra Payment',[payment])
x.add_column('Applied Payment',[Payment_applied])
x.add_column('End Principal',[End_principal])





