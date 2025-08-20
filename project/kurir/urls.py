from django.urls import path
from kurir.views import *
from ekspedisi.views.log_pengiriman import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('', KurirLoginView.as_view(), name="kurir_login"),
	# Dashboard
	path('kurir_dashboard', KurirDashboardView.as_view(), name="kurir_dashboard"),
	path('kurir_dashboard_detail', KurirDashboardDetailView.as_view(), name="kurir_dashboard_detail"),
	# Order Pickup
	path('kurir_order_pickup', KurirOrderPickupView.as_view(), name="kurir_order_pickup"),
	# Pengiriman
	path('kurir_pengiriman', KurirPengirimanView.as_view(), name="kurir_pengiriman"),
	path('kurir_pengiriman_detail/<str:id>', KurirPengirimanDetailView.as_view(), name="kurir_pengiriman_detail"),
	path('kurir_pengiriman_detail_view/<str:id>', KurirPengirimanDetailViewReadOnly.as_view(), name="kurir_pengiriman_detail_view"),

	path('kurir_order_detail/<str:id>', KurirOrderDetailView.as_view(), name="kurir_order_detail"),
	path('kurir_order_detail_view/<str:id>', KurirOrderDetailViewReadOnly.as_view(), name="kurir_order_detail_view"),
	path('kurir_update_status', KurirUpdateStatus.as_view(), name="kurir_update_status"),
	path('kurir_update_status_qr', KurirUpdateStatusQR.as_view(), name="kurir_update_status_qr"),
	path('kurir_update_status_sampai', KurirUpdateStatusSampai.as_view(), name="kurir_update_status_sampai"),
	path('kurir_update_status_kirim', KurirUpdateStatusKirim.as_view(), name="kurir_update_status_kirim"),
	path('kurir_update_status_paket/ttd', KurirUpdateStatusTTD.as_view(), name="kurir_update_status_paket_ttd"),
	path('kurir_update_lokasi_terkini', KurirUpdateLokasiTerkini.as_view(), name="kurir_update_lokasi_terkini"),

	path('kurir_update_order', KurirUpdateOrderView.as_view(), name="kurir_update_order"),
	# Cek Tarif
	path('kurir_tarif_gudang', KurirTarifGudangView.as_view(), name="kurir_tarif_gudang"),
	path('kurir_tarif_kilometer', KurirTarifKilometerView.as_view(), name="kurir_tarif_kilometer"),
	path('kurir_tarif_berat', KurirTarifBeratView.as_view(), name="kurir_tarif_berat"),
	path('kurir_tarif_layanan', KurirTarifLayananView.as_view(), name="kurir_tarif_layanan"),

	path('logout/', KurirLogout, name="kurir_logout"),
]