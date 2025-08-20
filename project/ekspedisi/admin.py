from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Pengiriman)
admin.site.register(LogPengiriman)
admin.site.register(OrderPickup)
admin.site.register(Satuan)
admin.site.register(TarifGudang)
admin.site.register(TarifKilometer)
admin.site.register(TarifLayanan)
admin.site.register(TarifBerat)
admin.site.register(Pengemasan)
admin.site.register(PesanPelanggan)
admin.site.register(Layanan)
admin.site.register(ExtraCash)
admin.site.register(Kendaraan)
admin.site.register(Kontak)
admin.site.register(Tentang)

admin.site.register(MapsApi)
@admin.register(Provinsi)
@admin.register(Kota)
@admin.register(Kecamatan)
@admin.register(Desa)
@admin.register(KodePos)
@admin.register(Toko)
@admin.register(Gudang)

class ProvinsiAdmin(ImportExportModelAdmin):
    pass

class KotaAdmin(ImportExportModelAdmin):
    pass

class KecamatanAdmin(ImportExportModelAdmin):
    pass

class DesaAdmin(ImportExportModelAdmin):
    pass

class KodePos(ImportExportModelAdmin):
    pass

class Toko(ImportExportModelAdmin):
    pass

class Gudang(ImportExportModelAdmin):
    pass