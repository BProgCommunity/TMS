from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PropertyType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    floor = models.IntegerField()
    number = models.CharField(max_length=50)
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    no_ktp = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ElectricityType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class LeaseType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number_of_days = models.IntegerField()

    def __str__(self):
        return self.name
    

class Lease(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    lease_type = models.ForeignKey(LeaseType, on_delete=models.CASCADE)  # Added lease_type field
    start_date = models.DateField()
    end_date = models.DateField()
    is_payed = models.BooleanField(default=False)
    electricity_type = models.ForeignKey(ElectricityType, on_delete=models.CASCADE, null=True, blank=True)
    watt = models.IntegerField()

    def __str__(self):
        return f"{self.tenant.name}'s Lease at {self.property.name} - {self.watt}W"

    def save(self, *args, **kwargs):
        # Check if the tenant has any unpaid leases
        unpaid_leases = Lease.objects.filter(tenant=self.tenant, is_payed=False).exists()
        if unpaid_leases:
            raise ValueError(f"Tenant {self.tenant.name} cannot add more leases until the previous one is paid.")
        
        super(Lease, self).save(*args, **kwargs)


class Troubleshoot(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.property.name}"


class TroubleshootImage(models.Model):
    id = models.AutoField(primary_key=True)
    troubleshoot = models.ForeignKey(Troubleshoot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='troubleshoot_images/')

    def __str__(self):
        return self.image.name
    

class ElectricityBill(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Electricity Bill - {self.value}"


class WaterBill(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Water Bill - {self.value}"


class MaintenanceBill(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Maintenance Bill - {self.value}"


class PenaltyBill(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Penalty Bill - {self.value}"


class TroubleshootBill(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - Troubleshoot Bill - {self.value}"
    

class Tax(models.Model):  # Added Tax model
    id = models.AutoField(primary_key=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.percent}% Tax"


class PayedType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
       

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    tenant_name = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=30, decimal_places=2)
    electricity_type = models.ForeignKey(ElectricityType, on_delete=models.CASCADE)
    electricity_bill = models.DecimalField(max_digits=30, decimal_places=2)
    water_bill = models.DecimalField(max_digits=30, decimal_places=2)
    maintenance_bill = models.DecimalField(max_digits=30, decimal_places=2)
    penalty_bill = models.DecimalField(max_digits=30, decimal_places=2)
    troubleshoot_bill = models.DecimalField(max_digits=30, decimal_places=2)
    tax_bill = models.DecimalField(max_digits=30, decimal_places=2)
    sub_total_bill = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    payed_type = models.ForeignKey(PayedType, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField()
    payed_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Transaction - {self.id}"