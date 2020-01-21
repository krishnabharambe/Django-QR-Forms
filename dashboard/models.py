from django.db import models

# Create your models here.

class QREvent(models.Model):
    title = models.CharField(max_length=10801)
    description = models.TextField()
    status = models.CharField(max_length=256)
    disabledesc = models.CharField(max_length=256)
    feeamount = models.CharField(max_length=50)
    enablepayment = models.CharField(max_length=50)

class QRForm(models.Model):
    eventid = models.CharField(max_length=64)
    fullname = models.CharField(max_length=512)
    noofmembers = models.CharField(max_length=64)
    gender = models.CharField(max_length=512)
    college = models.CharField(max_length=512)
    collegeaddress = models.CharField(max_length=512)
    address = models.CharField(max_length=512)
    contact = models.CharField(max_length=512)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=512)
    groupmembers= models.CharField(max_length=4000)
    mailsent= models.CharField(max_length=15)

class Eventpay(models.Model):
    clientid = models.CharField(max_length=64)
    CURRENCY = models.CharField(max_length=512)
    GATEWAYNAME = models.CharField(max_length=512)
    RESPMSG = models.CharField(max_length=512)
    BANKNAME = models.CharField(max_length=512)
    PAYMENTMODE = models.CharField(max_length=512)
    MID = models.CharField(max_length=512)
    RESPCODE = models.CharField(max_length=512)
    TXNID = models.CharField(max_length=512)
    TXNAMOUNT = models.CharField(max_length=512)
    ORDERID = models.CharField(max_length=512)
    STATUS = models.CharField(max_length=512)
    BANKTXNID = models.CharField(max_length=512)
    TXNDATE = models.CharField(max_length=512)
