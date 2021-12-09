
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from core.models import Department, DeptUser, Order, OrderProcess, Organization, Seller
from core.common_functions import next_process, prev_process
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import requests
from django.contrib.sites.models import Site

CHAIN_LINK = "http://192.168.1.102:3000"


@receiver(post_save, sender=OrderProcess)
def verdict_process(sender, instance, created, **kwargs):
    if not instance.generated_doc:
        if instance.verdict == OrderProcess.accept:
            next_process(instance)
        elif instance.verdict == OrderProcess.reject:
            prev_process(instance)


@receiver(post_save, sender=Order)
def generate_qr(sender, instance, created, **kwargs):
    if created:
        new_instance = OrderProcess(
            order=instance, pipeline_node=instance.current_node, checked_by=instance.contact_user)
        new_instance.save()
    if instance.verdict == Order.accept and not instance.qr_code:
        current_site = Site.objects.get_current()
        print(current_site.domain)
        img = qrcode.make(
            current_site.domain + str(instance.pk))
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        image = InMemoryUploadedFile(img_io, field_name=None, name="qr_code.png",
                                     content_type='image/png', size=img_io.tell, charset=None)
        instance.qr_code = image
        instance.save()


def log_data_to_chain(body, path, created):
    if created:
        r = requests.post(CHAIN_LINK+path,
                          data=body)
    else:
        r = requests.put(CHAIN_LINK+path,
                         data=body)

    if r.status_code != 200:
        print(r.status_code, r.reason)


@receiver(post_save, sender=Organization)
def log_in_chain(sender, instance, created, **kwargs):
    body = {
        "$class": "spp.organization.Organization",
        "organizationID": instance.id,
        "organizationEmail": instance.email,
        "organizationName": instance.title,
        "organizationPhoneNumber": instance.phone,
        "organizationBuisnessName": instance.title
    }

    log_data_to_chain(body, "/api/spp.organization.Organization", created)


@receiver(post_save, sender=Department)
def log_in_chain(sender, instance, created, **kwargs):
    body = {
        "$class": "spp.organizationDepartment.organizationDepartment",
        "organizationDepatmentID": instance.id,
        "organizationDepatmentName": instance.title,
        "organizationInfo": f"resource:spp.organization.Organization#{instance.org.pk}"
    }
    log_data_to_chain(
        body, "/api/spp.organizationDepartment.organizationDepartment", created)


@receiver(post_save, sender=DeptUser)
def log_in_chain(sender, instance, created, **kwargs):
    isAdmin = (instance.dept == None)
    body = {
        "$class": "spp.organizationUser.OrganizationUser",
        "organizationUserID": instance.user.id,
        "organizationUserEmail": instance.user.email,
        "organizationUser_Name": instance.user.name,
        "organizationUser_UserName": instance.user.username,
        "organizationUserPhoneNumber": instance.phone,
        "organizationInfo": f"resource:spp.organization.Organization#{instance.org.pk}",
        "isAdmin": isAdmin
    }

    log_data_to_chain(
        body, "/api/spp.organizationUser.OrganizationUser", created)


@receiver(post_save, sender=Seller)
def log_in_chain(sender, instance, created, **kwargs):
    body = {
        "$class": "spp.seller.Seller",
        "sellerID": instance.user.id,
        "sellerEmail": instance.user.email,
        "sellerUserName": instance.user.username,
        "sellerName": instance.user.name,
        "sellerPhoneNumber": instance.phone,
        "sellerBuisnessName": instance.bussiness_name
    }
    log_data_to_chain(body, "/api/spp.seller.Seller", created)


@receiver(post_save, sender=Order)
def log_in_chain(sender, instance, created, **kwargs):
    body = {
        "$class": "spp.orderCreation.Order",
        "OrderID": instance.id,
        "orderTitle": instance.title,
        "orderDetails": instance.details,
        "orderBudget": instance.budget,
        "orderType":  instance.type,
        "userInfo": f"resource:spp.organizationUser.OrganizationUser#{instance.contact_user.pk}",
        "organizationInfo": f"resource:spp.organization.Organization#{instance.org.pk}",
        "verdict": instance.verdict
    }

    log_data_to_chain(body, "/api/spp.orderCreation.Order", created)


@receiver(post_save, sender=OrderProcess)
def log_in_chain(sender, instance, created, **kwargs):
    body = {
        "$class": "spp.orderCreation.OrderState",
        "OrderStateID": instance.id,
        "orderInfo": f"resource:spp.orderCreation.Order#{instance.order.pk}",
        "userInfo": f"resource:spp.organizationUser.OrganizationUser#{instance.checked_by.pk}",
        "departmentInfo": f"resource:spp.organizationDepartment.organizationDepartment#{instance.pipeline_node.dept.pk}",
        "verdict": instance.verdict
    }
    log_data_to_chain(body, "/api/spp.orderCreation.OrderState", created)
