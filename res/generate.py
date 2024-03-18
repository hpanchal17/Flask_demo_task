from random import randint
import uuid
from twilio.rest import Client

otp = randint(000000, 999999)

def generate_otp():
    otp = randint(100000, 999999)
    return str(otp)

def generate_uuid():
    return str(uuid.uuid4())


def send_otp_sms(phone, otp):
    account_sid = "AC473e99cabbba8d53c41650cadabc99135"
    auth_token = "b4ad87c0c6f779b6e11ad6310ab1422fq"
    verify_sid = "VA6fcd7cc847d35e9c51d4b1d28e0ffccda"    

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=phone, channel="sms")