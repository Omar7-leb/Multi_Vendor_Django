from django.shortcuts import render
from vendor.models import Vendor
from .models import Message
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def vendors(request):
    vs = Vendor.objects.all()
    return render(request, "chat/vendors.html", {"vendors":vs})


def text_vendor(request, id):
    room_name = "c-{}v-{}".format(request.user.id,id)
    messages = Message.objects.filter(room_name=room_name)

    return render(request, "chat/room.html", {"room_name": room_name, "messages":messages, "vendor":id, "customer":request.user.id})