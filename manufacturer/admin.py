from django.contrib import admin
from .models import Batch,BatchDistribution,Drug

# Register your models here.
admin.site.register(Batch)
admin.site.register(BatchDistribution)
admin.site.register(Drug)