
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from core.models import Order, OrderProcess
from core.common_functions import next_process, prev_process
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


@receiver(post_save, sender=OrderProcess)
def verdict_process(sender, instance, created, **kwargs):
    if instance.verdict == OrderProcess.accept:
        next_process(instance)
    elif instance.verdict == OrderProcess.reject:
        prev_process(instance)


@receiver(post_save, sender=Order)
def generate_qr(sender, instance, created, **kwargs):
    if created:
        new_instance = OrderProcess(
            order=instance, pipeline_node=instance.current_node)
        new_instance.save()
    if instance.verdict == Order.accept and not instance.qr_code:
        img = qrcode.make(
            "192.168.1.11:2000/order_delivered/" + str(instance.pk))
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        image = InMemoryUploadedFile(img_io, field_name=None, name="qr_code.png",
                                     content_type='image/png', size=img_io.tell, charset=None)
        instance.qr_code = image
        instance.save()
