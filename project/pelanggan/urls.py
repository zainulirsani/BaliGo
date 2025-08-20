from django.urls import path
from pelanggan.views import *
from ekspedisi.views import PengirimanAPI, CekTarifAPI, GetLocationDetail, CekTarifPelangganAPI, PengemasanAPIView, PengirimanPOSAPI, OrderPickupAPI, OrderPickupPelangganAPI, PengirimanStatusTerkini, LayananAPIView, SatuanAPIView, TokoAPIView, PaketInvoice
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	path('', HomeView.as_view(), name="customer_home"),
	path('page_not_found/', Page_404.as_view(), name='page_not_found'),
	path('login/', PelangganLoginView.as_view(), name="customer_login"),
	path('register/', PelangganRegisterView.as_view(), name="customer_register"),
	path('activate/<uidb64>/<token>/',PelangganRegisterActivateView.as_view(), name='customer_activate'),
	path('reset/', PelangganResetPassword.as_view(), name='customer_reset_v1'),
	path('reset/<uidb64>/<token>/',PelangganResetPasswordActionView.as_view(), name='customer_reset'),
	path('reset/password/',PelangganResetPasswordAction2View.as_view(), name='customer_reset_password'),
	path('logout/', PelangganLogout, name="customer_logout"),
	path('tentang/', PelangganTentangView.as_view(), name="customer_tentang"),
	path('tentang/api/', PelangganTentangAPI.as_view(), name="customer_tentang_api"),
	path('kontak/', PelangganKontakView.as_view(), name="customer_kontak"),
	path('tarif/', PelangganTarifView.as_view(), name="customer_tarif"),
	path('track/', PelangganTrackView.as_view(), name="customer_track"),
	path('order/', PelangganOrderView.as_view(), name="customer_order"),
	path('order/customer/detail/<str:id>/', PelangganOrderBilling.as_view(), name='orderpickup_detail_pelanggan'),
	path('order/customer/', PelangganOrderBilling.as_view(), name='orderpickup_pelanggan'),
	path('order/<str:id>/print_billing/', csrf_exempt(GenerateInvoicePdf.as_view()), name='order_print_billing'),
	path('order/<str:id>/print_label/', csrf_exempt(GenerateLabelPdf.as_view()), name='order_print_label'),
	path('order_pengiriman/', OrderPengirimanView.as_view(), name="customer_order_pengiriman"),
	path('order_pengiriman_done/', OrderPengirimanDoneView.as_view(), name="customer_order_pengiriman_done"),
	path('order_history/', PelangganOrderHistoryView.as_view(), name="customer_order_history"),
	path('order/login/', PelangganOrderLogin.as_view(), name="customer_order_login"),
	path('order/update', PelangganOrderUpdate.as_view(), name="customer_order_update"),
	path('order/cancel/', csrf_exempt(PelangganOrderCancel.as_view()), name="customer_order_cancel"),
	path('order/delete/', csrf_exempt(PelangganOrderDelete.as_view()), name="customer_order_delete"),
	path('order/<str:id>/detail/', PelangganOrderDetail.as_view(), name="customer_order_detail"),
	path('live_track/', csrf_exempt(PelangganLiveTrack.as_view()), name="customer_live_track"),
	path('profile/', PelangganProfileView.as_view(), name="customer_profile"),

	path('api/pengiriman/', csrf_exempt(PengirimanAPI.as_view()), name="api_pengiriman"),
	path('api/pengiriman/pos', csrf_exempt(PengirimanPOSAPI.as_view()), name="api_pos_pengiriman"),
	path('api/pengiriman/status_terkini', csrf_exempt(PengirimanStatusTerkini.as_view()), name='api_pengiriman_status'),
	path('api/pengiriman/status_update', csrf_exempt(PengirimanStatusTerkini.as_view()), name='api_pengiriman_update'),
  path('api/pengiriman/get_invoice_paket', csrf_exempt(PaketInvoice.as_view()), name='api_pengiriman_get_invoice'),

	path('api/cek_tarif/', csrf_exempt(CekTarifAPI.as_view()), name="api_cek_tarif"),
	path('api/tarif/cek/', csrf_exempt(CekTarifPelangganAPI.as_view()), name="api_cek_tarif"),

	path('api/pengemasan/', csrf_exempt(PengemasanAPIView.as_view()), name='api_pengemasan'),
	path('api/layanan/', csrf_exempt(LayananAPIView.as_view()), name='api_layanan_pelanggan'),
	path('api/satuan/', csrf_exempt(SatuanAPIView.as_view()), name='api_satuan'),
	path('api/outlet/', csrf_exempt(TokoAPIView.as_view()), name='api_outlet'),

	path('api/order_pickup/', csrf_exempt(OrderPickupAPI.as_view()), name="api_order_pickup"),
	path('api/pelanggan/order_pickup/', csrf_exempt(OrderPickupPelangganAPI.as_view()), name="api_order_pickup"),
	path('api/pelanggan/rute/', csrf_exempt(GetLocationDetail.as_view()), name="api_order_pickup"),


	path('api/select2/provinsi/', csrf_exempt(APIProvinsi.as_view()), name="api_provinsi"),
	path('api/select2/kota/<str:provinsi_id>/', csrf_exempt(APIKota.as_view()), name="api_kota"),
	path('api/select2/kecamatan/<str:kota_id>/', csrf_exempt(APIKecamatan.as_view()), name="api_kecamatan"),
	path('api/select2/desa/<str:kecamatan_id>/', csrf_exempt(APIDesa.as_view()), name="api_desa"),
	path('api/select2/kodepos/<str:provinsi_id>/<str:kota_id>/<str:kecamatan_id>/<str:desa_id>/', csrf_exempt(APIKodePos.as_view()), name="api_kodepos"),
	path('api/select2/kodepos/<str:provinsi_id>/<str:kota_id>/<str:kecamatan_id>/', csrf_exempt(APIKodePos2.as_view()), name="api_kodepos2"),
]