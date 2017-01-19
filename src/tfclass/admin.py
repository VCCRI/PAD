from django.contrib import admin

from .models import  Peaks_db_file, Peaks_db


# This is to manage the admin page of the application
class Peaks_db_Admin(admin.ModelAdmin):
    list_display = ["protein", "origFile", "num_peaks", "labs"]

    class Meta:
        model = Peaks_db

admin.site.register(Peaks_db_file)
admin.site.register(Peaks_db, Peaks_db_Admin)
