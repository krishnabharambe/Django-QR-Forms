from django.shortcuts import render, redirect
from .models import QREvent as QRevent, QRForm,Eventpay
import pyqrcode
from pyqrcode import QRCode
import os
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
from .render import Render
from django.contrib.auth.models import User, auth
# Create your views here.

MERCHANT_KEY = 'dYun1Nv#r_J5oc0#'

def index(request):
    return render(request, 'dashboard/index.html')


def qreventmanager(request):
    qrevents = QRevent.objects.all()
    return render(request, 'dashboard/qreventmanager.html', {'qrevents': qrevents})


def qreventmanager_manger(request):
    return render(request, 'dashboard/qreventmanager_manger.html')


def qreventmanager_edit(request, id):
    if request.method == 'POST':
        qr = QRevent.objects.get(pk=id)
        qr.title = request.POST['title']
        qr.description = request.POST['description']
        qr.status = request.POST['status']
        qr.disabledesc = request.POST['disableddesc']
        qr.save()
        return redirect('qreventmanager')
    else:
        qrevent = QRevent.objects.get(pk=id)
        return render(request, 'dashboard/qreventmanager_edit.html', {'qrevent': qrevent})


def qreventmanager_delete(request, id):
    if request.method == 'POST':
        qr = QRevent.objects.get(pk=id)
        qr.delete()
        return redirect('qreventmanager')
    else:
        qrevent = QRevent.objects.get(pk=id)
        return render(request, 'dashboard/qreventmanager_delete.html', {'qrevent': qrevent})


def qreventmanager_dwn(request, id):
    qr = QRevent.objects.get(pk=id)
    s = 'http://127.0.0.1:8000/dashboard/qreventmanager/' + str(qr.id)
    url = pyqrcode.create(s)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url.svg(os.path.join(BASE_DIR, 'static') +
            "/qrcode/"+str(qr.id)+".svg", scale=8)
    return render(request, 'dashboard/qreventmanager_dwn.html', {'QR': qr})


def qreventmanager_create(request):
    if request.method == 'POST':
        qr = QRevent()
        qr.title = request.POST['title']
        qr.description = request.POST['description']
        qr.status = request.POST['status']
        qr.disabledesc = request.POST['disableddesc']
        qr.save()
        return redirect('qreventmanager')

    else:
        return render(request, 'dashboard/qreventmanager_create.html')


def qrevent_createform(request, id):
    if request.method == 'POST':
        if 'setenablepayment' in request.POST:
            QR = QRevent.objects.get(pk=id)
            QR.enablepayment = request.POST['enablepayment']
            QR.save()
            return redirect('qrevent_createform', id=id)
        if 'setfee' in request.POST:
            QR = QRevent.objects.get(pk=id)
            QR.feeamount = request.POST['feeamount']
            QR.save()
            return redirect('qrevent_createform', id=id)
        if 'disablefee' in request.POST:
            QR = QRevent.objects.get(pk=id)
            QR.enablepayment = '0'
            QR.save()
            return redirect('qrevent_createform', id=id)
    else:
        QR = QRevent.objects.get(pk=id)
        return render(request, 'dashboard/qrevent_createform.html', {'QR': QR})


def qrevent_client(request, id):
    if request.method == 'POST':
        QRF = QRForm()
        QRF.eventid = str(id)
        QRF.fullname = request.POST['fullname'] 
        QRF.noofmembers = request.POST['noofmembers'] 
        QRF.gender = request.POST['gender'] 
        QRF.college = request.POST['college'] 
        QRF.collegeaddress = request.POST['collegeaddress'] 
        QRF.address = request.POST['address'] 
        QRF.contact = request.POST['contact'] 
        QRF.email = request.POST['email'] 
        QRF.subject = request.POST['subject'] 
        QRF.groupmembers = request.POST['groupmembers'] 
        QREinstance = QRF.save()

        QRE = QRevent.objects.get(pk=id)
        if QRE.enablepayment == '1':
            # move towards payments
            return redirect('clientpay',eid=id,cid=QRF.pk)
        else:
            return redirect('printpage',eid=id,cid=QRF.pk)
    else:
        QRE = QRevent.objects.get(pk=id)
        return render(request, 'dashboard/client.html', {'QRE': QRE})

def printpage(request,eid,cid):
    QRF = QRForm.objects.get(pk=cid)
    QRE = QRevent.objects.get(pk=eid)
    if QRE.enablepayment == '1':
        EPS = Eventpay.objects.filter(clientid=cid)
        return render(request,'dashboard/printpage.html',{'QRE':QRE,'QRF':QRF,'EPS':EPS})
    else:
        return render(request,'dashboard/printpage.html',{'QRE':QRE,'QRF':QRF})

def finalprint(request,eid,cid):
    QRF = QRForm.objects.get(pk=cid)
    QRE = QRevent.objects.get(pk=eid)
    if QRE.enablepayment == '1':
        EPS = Eventpay.objects.filter(clientid=cid)
        return Render.render('dashboard/printpage.html',{'QRE':QRE,'QRF':QRF,'EPS':EPS})
    else:
        return Render.render('dashboard/printpage.html',{'QRE':QRE,'QRF':QRF})

def clientpay(request,eid,cid):
    if request.method == 'POST':
        QRE = QRevent.objects.get(pk=eid)
        param_dict = {

                'MID': 'lSjRuh38953433535881',
                'ORDER_ID': str(cid),
                'TXN_AMOUNT': str(QRE.feeamount),
                'CUST_ID': str(cid),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/dashboard/payconfirm/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'dashboard/paytm.html', {'param_dict': param_dict})
    else:
        QRF = QRForm.objects.get(pk=cid)
        QRE = QRevent.objects.get(pk=eid)
        return render (request,'dashboard/clientpay.html',{'QRE':QRE,'QRF':QRF})

@csrf_exempt
def payconfirm(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    QRF=QRForm.objects.get(pk=response_dict['ORDERID'])
    EP = Eventpay()
    EP.clientid = response_dict['ORDERID']
    EP.CURRENCY = response_dict['CURRENCY']
    EP.GATEWAYNAME = response_dict['GATEWAYNAME']
    EP.RESPMSG = response_dict['RESPMSG']
    EP.BANKNAME = response_dict['BANKNAME']
    EP.PAYMENTMODE = response_dict['PAYMENTMODE']
    EP.MID = response_dict['MID']
    EP.RESPCODE = response_dict['RESPCODE']
    EP.TXNID = response_dict['TXNID']
    EP.TXNAMOUNT = response_dict['TXNAMOUNT']
    EP.ORDERID = response_dict['ORDERID']
    EP.STATUS = response_dict['STATUS']
    EP.BANKTXNID = response_dict['BANKTXNID']
    EP.TXNDATE = response_dict['TXNDATE']
    EP.save()
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'dashboard/paymentstatus.html', {'response': response_dict,'QRF':QRF})

def qreventmanager_entries(request,id):
    QRFS = QRForm.objects.filter(eventid=id)
    return render(request,'dashboard/qreventmanager_entries.html',{'QRFS':QRFS})

def logout(request):
    auth.logout(request)
    return redirect('/')     

def trackmail(request,eid,cid):
    if request.method == 'POST':
        if 'sentmail' in request.POST:
            QRF = QRForm.objects.get(pk=cid)
            QRF.mailsent = '1'
            QRF.save()
            # sent mail
            return redirect('qreventmanager_entries',id=eid)
        if 'resentmail' in request.POST:
            QRF = QRForm.objects.get(pk=cid)
            QRF.mailsent = Str(QRF.mailsent + 1)
            QRF.save()
            # sent mail
            return redirect('qreventmanager_entries',id=eid)
    else:
        return redirect('qreventmanager_entries',id=eid)