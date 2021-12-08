
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from core.models import Department, DeptUser, Order, OrderProcess, Organization, Seller
from core.common_functions import next_process, prev_process
import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import requests
from django.contrib.sites.models import Site


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
            order=instance, pipeline_node=instance.current_node)
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


# @receiver(post_save, sender=Organization)
# def log_in_chain(sender, instance, created, **kwargs):
#     if created:
#         body = {
#             "$class": "spp.organization.Organization",
#             "organizationID": instance.id,
#             "organizationEmail": instance.email,
#             "organizationName": instance.title,
#             "organizationPhoneNumber": instance.phone,
#             "organizationBuisnessName": instance.title
#         }

#         r = requests.post("http://10.40.56.149:3000/api/spp.organization.Organization",
#                           data=body)


# @receiver(post_save, sender=Department)
# def log_in_chain(sender, instance, created, **kwargs):
#     if created:

#         body = {
#             "$class": "spp.organizationDepartment.organizationDepartment",
#             "organizationDepatmentID": instance.id,
#             "organizationDepatmentName": instance.title,
#             "organizationInfo": f"resource:spp.organization.Organization#{instance.org.pk}"
#         }
#         r = requests.post("http://10.40.56.149:3000/api/spp.organizationDepartment.organizationDepartment",
#                           data=body)


# @receiver(post_save, sender=DeptUser)
# def log_in_chain(sender, instance, created, **kwargs):
#     if created:
#         isAdmin = (instance.dept == None)
#         body = {
#             "$class": "spp.organizationUser.OrganizationUser",
#             "organizationUserID": instance.user.id,
#             "organizationUserEmail": instance.user.email,
#             "organizationUser_Name": instance.user.name,
#             "organizationUser_UserName": instance.user.username,
#             "organizationUserPhoneNumber": instance.phone,
#             "isAdmin": isAdmin
#         }
#         if not isAdmin:
#             body[
#                 "userDepartmentInfo"] = f"resource:spp.organizationDepartment.organizationDepartment#{instance.org.pk}"
#         r = requests.post("http://10.40.56.149:3000/api/spp.organizationUser.OrganizationUser",
#                           data=body)
#         if r.status_code != 200:
#             print(r.status_code, r.reason)


# @receiver(post_save, sender=Seller)
# def log_in_chain(sender, instance, created, **kwargs):
#     if created:
#         body = {
#             "$class": "spp.seller.Seller",
#             "sellerID": instance.user.id,
#             "sellerEmail": instance.user.email,
#             "sellerUserName": instance.user.username,
#             "sellerName": instance.user.name,
#             "sellerPhoneNumber": instance.phone,
#             "sellerBuisnessName": instance.bussiness_name
#         }
#         r = requests.post("http://10.40.56.149:3000/api/spp.seller.Seller",
#                           data=body)
#         if r.status_code != 200:
#             print(r.status_code, r.reason)


# @receiver(post_save, sender=Order)
# def log_in_chain(sender, instance, created, **kwargs):
#     if created:

#         body = {
#             "$class": "spp.orderCreation.Order",
#             "OrderID": instance.id,
#             "orderTitle": instance.title,
#             "orderDetails": instance.details,
#             "orderBudget": instance.budget,
#             "orderType": instance.type,
#             "userInfo": f"resource:spp.organizationUser.OrganizationUser#{instance.contact_user.pk}",
#             "organizationInfo": f"resource:spp.organization.Organization#{instance.org.pk}",
#             "isCompleted": instance.verdict
#         }
#         r = requests.post("http://10.40.56.149:3000/api/spp.seller.Seller",
#                           data=body)
#         if r.status_code != 200:
#             print(r.status_code, r.reason)
