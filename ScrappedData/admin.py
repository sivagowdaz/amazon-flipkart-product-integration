from django.contrib import admin
from . models import FlipkartData, AmezonData, Compare
from . models import PdfFiles
# Model registration for admin pannel.

admin.site.register(FlipkartData)
admin.site.register(AmezonData)
admin.site.register(Compare)
admin.site.register(PdfFiles)
