from paynow import Paynow
import random
import time

paynow = Paynow(
    '15115', 
    '9506d267-ce8e-4464-ab92-d1ae7a7c3c97',
    'https://www.paynow.co.zw/Payment/BillPaymentLink/?q=aWQ9MTUxODYmYW1vdW50PTEyMC4wMCZhbW91bnRfcXVhbnRpdHk9MC4wMCZsPTE%3d', 
    'http://google.com'
)



def make_payment(reason, phone_number, email, amount):
    print('Reason: ', reason )
    print('phone_number: ', phone_number )
    print('email: ', email )
    print('amount: ', amount )


    payment = paynow.create_payment(random.randint(1, 1000000000000), email)
    payment.add(reason, amount)
    response = paynow.send_mobile(payment, phone_number, 'ecocash')

    print('Response: ', response)

    try:
        if(response.success):
                i = 0
                while i < 60:
                    poll_url = response.poll_url
                    print("Poll Url: ", poll_url)
                    status = paynow.check_transaction_status(poll_url)
                    print("Payment Status: ", status.status)
                    if status.status == 'paid':
                        return {'status': status.status}
                    if status.status == 'cancelled':
                        return {'status': status.status}
                    
                    time.sleep(1)
                    i += 1
                    if i == 60:
                        return {'status': status.status}
    except:
        
        return {'status': 'system_error'}


