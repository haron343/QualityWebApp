from django.contrib import admin
from .models import Carrier,Notes,Report
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX, CSV
# Register your models here.
admin.site.register(Carrier)




class ReportResource(resources.ModelResource):
    class Meta:
        model = Report
        import_id_fields = ('id',)

    def import_data(self, dataset, **kwargs):
        # تخصيص طريقة الاستيراد هنا
        return super().import_data(dataset, **kwargs)

    def export(self, queryset=None, *args, **kwargs):
        # تخصيص طريقة التصدير هنا
        return super().export(queryset, *args, **kwargs)

class NotesResource(resources.ModelResource):
    class Meta:
        model = Notes
        import_id_fields = ('id',)

    def import_data(self, dataset, **kwargs):
        # تخصيص طريقة الاستيراد هنا
        return super().import_data(dataset, **kwargs)

    def export(self, queryset=None, *args, **kwargs):
        # تخصيص طريقة التصدير هنا
        return super().export(queryset, *args, **kwargs)

class ReportAdmin(ExportActionModelAdmin):
    resource_class = ReportResource

class NotesAdmin(ExportActionModelAdmin):
    resource_class = NotesResource

admin.site.register(Report, ReportAdmin)
admin.site.register(Notes, NotesAdmin)