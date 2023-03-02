from django.db import models
from enum import Enum
from admincontrol.models import User
import datetime
from django.dispatch import receiver
# Create your models here.


class Condition(Enum):
    NEW = 'New'
    GOOD = 'Good'
    UNUSABLE = 'Not usable'
    REQUIREREPAIR = 'Requires Repairment'
    LOST = 'Lost'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AssetLocation(Enum):
    DEPARTMENT_A = 'Department A (room 1)'
    KITCHEN = 'room 4'
    STORE_1 = 'room 5'
    GARRAGE = 'Garrage'
    OFFICE_PREMISES = 'office premises'
    GANDAKI_OFFICE = 'gandaki office'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class AssetPool(Enum):
    A = ["Building", "structure", "similar other structures of permanent nature"]
    B = ["Computer", "data processing equipment",
         "furniture", "fixture and office equipment"]
    C = ["Automobiles", "buses and mini-buses"]
    D = [
        "Construction and excavation equipment", "the depreciable properties not included in elsewhere including Sub-section (3) of Section 17",
        "Sub-section (3) of Section 18", "Sub-section (3) of this Schedule"]
    E = ["Intangible properties except the depreciable properties mentioned in category 'D'"]

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Vendor(models.Model):
    vendor_no = models.CharField(
        max_length=100, default=None, null=True, unique=True)
    name_of_vendor = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=500)
    contact_no = models.CharField(max_length=50)
    pan_no = models.IntegerField(default=None, blank=True)
    status = models.CharField(max_length=100, default='true')

    def __str__(self):
        return self.name_of_vendor


class Specifications(models.Model):
    brand = models.CharField(
        max_length=100, blank=True)
    Model_no = models.CharField(max_length=100, blank=True)
    year_of_manufacture = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=100, blank=True)
    warranty_period = models.CharField(max_length=100, blank=True)
    other_specs = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.Model_no


class Product(models.Model):
    name_of_asset = models.CharField(max_length=100)
    asset_code = models.CharField(
        max_length=100, default=None, null=True, unique=True)
    supporting_gear = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField()
    date_of_purchase = models.CharField(max_length=100)
    rate_per_unit = models.FloatField(max_length=100)
    condition_of_asset = models.CharField(max_length=50)
    assets_pool = models.CharField(max_length=500)
    asset_location = models.CharField(max_length=500)
    purpose_of_asset = models.CharField(max_length=500)
    date_of_update = models.CharField(max_length=100, blank=True)
    product_category = models.CharField(max_length=200)
    availale_status = models.CharField(max_length=10, default="true")
    status = models.CharField(max_length=10, default="true")
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True)
    specifications = models.ForeignKey(
        Specifications, on_delete=models.CASCADE, default=None, null=True)
    updated_by = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name_of_asset


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="produt_image/")

    def __str__(self):
        return self.product.name_of_asset


class Location(models.Model):
    location_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='true')

    def __str__(self):
        return self.location_name


class AssestAssign(models.Model):
    nameofstaff = models.CharField(max_length=100)
    purpose = models.CharField(max_length=300)
    date_of_issue = models.DateField(default=datetime.datetime.now, blank=True)
    estimated_date_of_return = models.DateField()
    asset_info = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    asset_verified_by = models.ForeignKey(User,
                                          on_delete=models.CASCADE)
    token = models.CharField(max_length=100, blank=True)


class AssestReturn(models.Model):
    nameofstaffreturningasset = models.CharField(max_length=100)
    asset_verified_by = models.CharField(max_length=100)
    asset_release_by = models.CharField(max_length=100)
    asset_issued_in = models.DateField()
    expected_date_of_return_of_such_asset = models.DateField()
    date_of_return = models.DateField(
        default=datetime.datetime.now, blank=True)
    did_return_all = models.CharField(max_length=50, blank=True)
    asset_code = models.CharField(max_length=100, blank=True)
    asset_name = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=100, blank=True)


@receiver(models.signals.post_save, sender=Product)
def id_generator(sender, instance, **kwargs):
    name = instance.name_of_asset
    try:
        if name[3]:
            name = name[:3].upper()
    except:
        name = instance.name_of_asset

    fullname = f'{name}00{instance.id}'
    if not instance.asset_code:
        Product.objects.filter(id=instance.id).update(
            asset_code=fullname)


@receiver(models.signals.post_save, sender=Vendor)
def id_generator(sender, instance, **kwargs):
    name = instance.name_of_vendor
    try:
        if name[3]:
            name = name[:3].upper()
    except:
        name = instance.name_of_vendor

    fullname = f'{name}00{instance.id}'
    if not instance.vendor_no:
        Vendor.objects.filter(id=instance.id).update(
            vendor_no=fullname)
