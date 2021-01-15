from django.contrib import admin
from django.core.paginator import Paginator
from django.utils.functional import cached_property
from .models import Titlebasics

# Register your models here.
'''
class DumbPaginator(Paginator):
    """
    Paginator that does not count the rows in the table.
    """
    @cached_property
    def count(self):
        return 9999999999

#@admin.register(Titlebasics)

class TitlebasicsAdmin(admin.ModelAdmin):
    paginator = DumbPaginator
    model = Titlebasics
    show_full_result_count = False
 
admin.site.register(Titlebasics, TitlebasicsAdmin)
'''