from django.db import models
from accounts.models import User
import uuid
from datetime import date
# Create your models here.
class PropertyDetail(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property',default=None,null=True)
    property_name=models.CharField(max_length=200)
    email=models.EmailField(default=None,null=True)
    tenant_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    bhk=models.IntegerField()
    age=models.IntegerField()
    phone_number=models.CharField(max_length=10)
    rent=models.CharField(max_length=10)
    rent_date=models.DateField(null=True)
    adhar_num=models.CharField(max_length=12)
    adhar_pic=models.FileField(upload_to="adhar_card",null=True)
    #property_pic=models.FileField(upload_to="Propery_image", null=True)
    rent_due_date=models.IntegerField(default=True)
    is_tenant_active=models.BooleanField(default=True)
    is_paid=models.BooleanField(default=False)
    rent_token=models.CharField(max_length=100,default=uuid.uuid4)
    owner_rent_token_paid=models.CharField(max_length=100,default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.owner.email 
class Image(models.Model):
    property=models.ForeignKey(PropertyDetail,on_delete=models.CASCADE,related_name='images')
    property_pic=models.FileField(upload_to="Property_image", null=True)

class property_to_excel(models.Model):
    file=models.FileField(upload_to="propertyfile",null=True)
