from django.contrib import admin
from .models import PropertyType, Property, Tenant, ElectricityType, LeaseType, Lease, Troubleshoot, TroubleshootImage, ElectricityBill, WaterBill, MaintenanceBill, PenaltyBill, TroubleshootBill, Tax, PayedType, Transaction

# Register your models here.
admin.site.register(PropertyType)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(ElectricityType)
admin.site.register(LeaseType)
admin.site.register(Lease)
admin.site.register(Troubleshoot)
admin.site.register(TroubleshootImage)
admin.site.register(ElectricityBill)
admin.site.register(WaterBill)
admin.site.register(MaintenanceBill)
admin.site.register(PenaltyBill)
admin.site.register(TroubleshootBill)
admin.site.register(Tax)
admin.site.register(PayedType)
admin.site.register(Transaction)