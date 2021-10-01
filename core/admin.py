from django.contrib import admin
from core.models import *
import importlib
import inspect


class CustomModelAdminMixin(object):

    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if not (field.name in ("id", "password", "last_login", "logo", "details", "qr_code", "end_date", "end_time"))]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


class modelAdmin(CustomModelAdminMixin, admin.ModelAdmin):

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)


# Register your models here.
# admin.site.register(User, modelAdmin)
# admin.site.register(Organization, modelAdmin)
for name, cls in inspect.getmembers(importlib.import_module("core.models"), inspect.isclass):
    if name not in ("AbstractBaseUser", "BaseUserManager", "UserManager", "PermissionsMixin"):
        admin.site.register(cls, modelAdmin)
