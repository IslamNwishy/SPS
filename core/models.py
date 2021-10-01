from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid

# Create your models here.


class UserManager(BaseUserManager):
    """
    class manager for providing a User(AbstractBaseUser) full control
    on this objects to create all types of User and this roles.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        pass data  to '_create_user' for creating normal_user .
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        pass data to '_create_user' for creating super_user .
        """
        if email is None:
            raise TypeError('Users must have an email address.')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=500)
    is_staff = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Organization(models.Model):
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(unique=True, max_length=500)
    commercial_id = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=20)
    admin = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="org")
    logo = models.ImageField(upload_to="org_logo")

    def __str__(self) -> str:
        return self.title


class Department(models.Model):
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=500)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="depts")

    def __str__(self) -> str:
        return self.title


class DeptUser(models.Model):
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    dept = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="dept_user")


class Document(models.Model):
    rfq, approve_req, review_req, contract = "1", "2", "3", "4"

    REQUESTS = [
        (rfq, "Request For Quotation"),
        (approve_req, "Approval Request"),
        (review_req, "Request for Review"),
        (contract, "Final Contract"),
    ]
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="docs")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="org_docs")
    # type = models.CharField(
    #     max_length=2, choices=REQUESTS)

    def __str__(self) -> str:
        return self.title
# class DocumentFields(models.Model):
#     key=models.CharField(max_length=200)
#     value


class Pipeline(models.Model):
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="pipelines")

    def __str__(self) -> str:
        return self.name


class PipelineNode(models.Model):
    offers, cancel, review = False, False, True

    BEHAVIOUR = [
        (cancel, "Cancel"),
        (review, "Return For Review")
    ]

    STATE = [
        (offers, "Waiting for Offers"),
        (review, "A Department is Reviewing the Order")
    ]

    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="nodes")
    dept = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    node_number = models.PositiveIntegerField()
    rejection_behaviour = models.BooleanField(
        default=cancel, choices=BEHAVIOUR)
    generates_document = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True)
    state = models.BooleanField(choices=STATE, default=review)

    def __str__(self) -> str:
        return str(self.pipeline) + "::" + str(self.node_number)

    def next(self):
        try:
            next_node = self.pipeline.nodes.get(
                node_number=self.node_number + 1)
        except:
            return None
        return next_node

    def prev(self):
        try:
            prev = self.pipeline.nodes.get(
                node_number=self.node_number - 1)
        except:
            return None
        return prev

    def is_last(self):
        if(self.next()):
            return False
        return True


class Order(models.Model):
    accept, reject, unkown = True, False, None
    pending, on_delivery, delivered = None, False, True
    VERDICT = [
        (accept, "Accepted"),
        (reject, "Rejected"),
        (unkown, "In Pipeline")
    ]
    STATUS = [
        (pending, "Offer not Chosen"),
        (on_delivery, "Waiting for Delivery"),
        (delivered, "Delivered")
    ]
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    verdict = models.BooleanField(
        choices=VERDICT, default=unkown, null=True, blank=True)
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="pipe_orders")
    current_node = models.ForeignKey(
        PipelineNode, on_delete=models.CASCADE, related_name="node_orders")
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="orders")
    title = models.CharField(max_length=200)
    details = models.TextField()
    budget = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    type = models.CharField(max_length=100)  # project, product, supply, etc..
    contact_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    end_time = models.TimeField()
    completion = models.BooleanField(
        choices=STATUS, default=pending, null=True, blank=True)
    qr_code = models.ImageField(
        upload_to="order_qr_codes", null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class OrderProcess(models.Model):
    accept, reject, unkown = True, False, None
    VERDICT = [
        (accept, "Accepted"),
        (reject, "Rejected"),
        (unkown, "In Pipeline")
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pipeline_node = models.ForeignKey(PipelineNode, on_delete=models.CASCADE)
    verdict = models.BooleanField(
        choices=VERDICT, default=unkown, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    checked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)


class Offer(models.Model):
    id = models.UUIDField(
        auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=200)
    vendor_email = models.EmailField()
    vendor_phone = models.CharField(max_length=20)
    details = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
