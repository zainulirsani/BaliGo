from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from .views.oauth_SSO import oauth_redirect,oauth_callback, dashboard_SSO

urlpatterns = [
	path('', LoginView.as_view(), name="login"),
	path('logout/', logout, name="logout"),
	path('register/', RegisterView.as_view(), name="register"),
    
	path('oauth/redirect/', csrf_exempt(oauth_redirect), name='oauth_redirect'),
    path('oauth/callback/', csrf_exempt(oauth_callback), name='oauth_callback'),
    path('dashboard_SSO/', dashboard_SSO, name='dashboard_SSO'),

	path('dashboard/', DashboardView.as_view(), name='dashboard'),

	path('profile/', ProfileView.as_view(), name='profile'),
	path('profile/update/', ProfileView.as_view(), name='profile_update'),

	path('personil/', csrf_exempt(PersonilView.as_view()), name='personil'),
	path('personil/delete/', PersonilDelete.as_view(), name='personil_delete'),
	path('personil/detail/', PersonilDetail.as_view(), name='personil_detail'),
	path('personil/update/', PersonilDetail.as_view(), name='personil_update'),
	path('personil/activated/', PersonilActivate.as_view(), name='personil_activated'),

	path('pelanggan/', csrf_exempt(PelangganView.as_view()), name='pelanggan'),
	path('pelanggan/detail/', PelangganDetail.as_view(), name='pelanggan_detail'),
	path('pelanggan/update/', PelangganDetail.as_view(), name='pelanggan_update'),
	path('pelanggan/delete/', PelangganDelete.as_view(), name='pelanggan_delete'),
	path('pelanggan/arsip/', PelangganArsip.as_view(), name='pelanggan_arsip'),
	path('pelanggan/unarsip/', PelangganUnarsip.as_view(), name='pelanggan_unarsip'),
	path('api/track/', PelangganTrackAPIView.as_view(), name='api_pelanggan_track'),

	path('pelanggan/select2/', PelangganCari.as_view(), name='pelanggan_select2'),

	path('toko/', TokoView.as_view(), name='toko'),
	path('toko/delete/', TokoDelete.as_view(), name='toko_delete'),
	path('toko/update/', TokoUpdate.as_view(), name='toko_update'),
	path('toko/arsip/', TokoArsip.as_view(), name='toko_arsip'),
	path('toko/unarsip/', TokoUnarsip.as_view(), name='toko_unarsip'),
	path('toko/list/<str:id>/', csrf_exempt(ListOutletView.as_view()), name='list_toko'),
	path('toko/penerima/list/<str:id>/', csrf_exempt(ListOutletPenerimaView.as_view()), name='list_toko_penerima'),
	path('toko/nearest/<str:lat>/<str:lon>/', csrf_exempt(calculate_last_outlet.as_view()), name='toko_nearest'),
	path('api/toko/', TokoAPIView.as_view(), name='api_toko'),
	path('api/toko/select2/', TokoToSelect2.as_view(), name='toko_select2'),

	path('toko/<str:lat>/<str:lon>/', csrf_exempt(NearestOutlet.as_view()), name='toko_terdekat'),
	
	path('gudang/', csrf_exempt(GudangView.as_view()), name='gudang'),
	path('gudang/detail/', GudangDetail.as_view(), name='gudang_detail'),
	path('gudang/update/', GudangDetail.as_view(), name='gudang_update'),
	path('gudang/delete/', GudangDelete.as_view(), name='gudang_delete'),
	path('gudang/arsip/', GudangArsip.as_view(), name='gudang_arsip'),
	path('gudang/unarsip/', GudangUnarsip.as_view(), name='gudang_unarsip'),
	path('gudang/pengirim/list/<str:id>/', csrf_exempt(ListGudangView.as_view()), name='list_gudang_pengirim'),
	path('gudang/penerima/list/<str:id>/', csrf_exempt(ListGudangPenerimaView.as_view()), name='list_gudang_penerima'),
	path('gudang/data/', csrf_exempt(GetAllGudang.as_view()), name='gudang_data'),
	path('gudang/province/', csrf_exempt(GetGudangByProvince.as_view()), name='gudang_province'),
	path('api/gudang/', GudangAPIView.as_view(), name='api_gudang'),
	path('api/gudang/select2/', GudangToSelect2.as_view(), name='gudang_select2'),

	path('gudang/<str:lat>/<str:lon>/', csrf_exempt(NearestGudang.as_view()), name='gudang_terdekat'),

	path('tentang/', TentangView.as_view(), name='tentang'),
	path('tentang/<str:id>/update/', TentangView.as_view(), name='tentang_update'),

	path('kontak/', KontakView.as_view(), name='kontak'),
	path('kontak/<str:id>/update/', KontakView.as_view(), name='kontak_update'),

	path('pesan/', csrf_exempt(PesanView.as_view()), name='pesan'),
	path('pesan/<str:id>/delete/', csrf_exempt(PesanDelete.as_view()), name='pesan_delete'),
	path('pesan/<str:id>/balas/', csrf_exempt(PesanBalas.as_view()), name='pesan_balas'),

	path('order_pickup/', csrf_exempt(OrderPickupView.as_view()), name='order_pickup'),
	path('order_pickup/cek_outlet_gudang_by_kecamatan', csrf_exempt(OrderPickupPilihOutletGudangManual.as_view()), name='order_pickup_cek_manual'),
	path('order_pickup/list_outlet/', OrderPickupOutlet.as_view(), name='pickup_list_outlet'),
	path('order_pickup/list_outlet/<str:id>/detail/', OrderPickupOutletList.as_view(), name='pickup_list_outlet_order'),
	path('order_pickup/list_outlet/<str:id>/detail/history/', OrderPickupOutletHistoryList.as_view(), name='pickup_list_outlet_order_history'),
	path('order_pickup/list_outlet/order/<str:id>/', OrderPickupOutletDetail.as_view(), name='pickup_list_outlet_detail'),

	path('order_pickup/list_gudang/', OrderPickupGudang.as_view(), name='pickup_list_gudang'),
	path('order_pickup/list_gudang/<str:id>/detail/', OrderPickupGudangList.as_view(), name='pickup_list_gudang_order'),
	path('order_pickup/list_gudang/order/<str:id>/', OrderPickupGudangDetail.as_view(), name='pickup_list_gudang_detail'),

	# Order Pickup For Admin Outlet
	path('adm_outlet/order/', AdminOutletOrderView.as_view(), name='adm_outlet_order'),
	path('adm_outlet/order_history/', AdminOutletOrderHistoryView.as_view(), name='adm_outlet_order_history'),
	path('adm_outlet/order/detail/', AdminOutletOrderDetail.as_view(), name='adm_outlet_order_detail'),
	path('adm_outlet/order/update/', AdminOutletOrderDetail.as_view(), name='adm_outlet_order_update'),

	path('kurir/', csrf_exempt(KurirView.as_view()), name='kurir'),
	path('kurir/delete/', KurirDelete.as_view(), name='kurir_delete'),
	path('kurir/detail/', KurirDetail.as_view(), name='kurir_detail'),
	path('kurir/update/', KurirDetail.as_view(), name='kurir_update'),
	path('kurir/arsip/', KurirArsip.as_view(), name='kurir_arsip'),
	path('kurir/unarsip/', KurirUnarsip.as_view(), name='kurir_unarsip'),
	path('kurir/activated/', KurirActivate.as_view(), name='kurir_activated'),
	path('kurir/outlet/', KurirListByOutlet.as_view(), name='kurir_outlet'),

	path('kendaraan/', KendaraanView.as_view(), name='kendaraan'),
	path('kendaraan/delete/', KendaraanDelete.as_view(), name='kendaraan_delete'),
	path('kendaraan/detail/', KendaraanDetail.as_view(), name='kendaraan_detail'),
	path('kendaraan/update/', KendaraanDetail.as_view(), name='kendaraan_update'),
	path('kendaraan/arsip/', KendaraanArsip.as_view(), name='kendaraan_arsip'),
	path('kendaraan/unarsip/', KendaraanUnarsip.as_view(), name='kendaraan_unarsip'),

	path('pengemasan/', PengemasanView.as_view(), name='pengemasan'),
	path('pengemasan/delete/', PengemasanDelete.as_view(), name='pengemasan_delete'),
	path('pengemasan/detail/', PengemasanDetail.as_view(), name='pengemasan_detail'),
	path('pengemasan/update/', PengemasanDetail.as_view(), name='pengemasan_update'),
	path('api/pengemasan/', PengemasanAPIView.as_view(), name='api_pengemasan'),
	path('api/pengemasan/select2/', PengemasanToSelect2.as_view(), name='pengemasan_select2'),
	path('api/pengemasan/select2/<str:id_pengemasan>/', PengemasanDetailAPI.as_view(), name='pengemasan_detail_api'),

	path('layanan/', LayananView.as_view(), name='layanan'),
	path('layanan/delete/', LayananDelete.as_view(), name='layanan_delete'),
	path('layanan/detail/', LayananDetail.as_view(), name='layanan_detail'),
	path('layanan/update/', LayananDetail.as_view(), name='layanan_update'),
	path('layanan/list/', csrf_exempt(SemuaTarifLayanan.as_view()), name='layanan_list'),
	path('api/layanan/', LayananAPIView.as_view(), name='api_layanan'),
	path('api/layanan/select2/', LayananToSelect2.as_view(), name='layanan_select2'),

	path('tarif_gudang/', csrf_exempt(TarifGudangView.as_view()), name='tarif_gudang'),
	path('tarif_gudang/<str:id>/delete/', csrf_exempt(TarifGudangDelete.as_view()), name='tarif_gudang_delete'),
	path('tarif_gudang/<str:id>/detail/', csrf_exempt(TarifGudangDetail.as_view()), name='tarif_gudang_detail'),
	path('tarif_gudang/<str:id>/update/', csrf_exempt(TarifGudangDetail.as_view()), name='tarif_gudang_update'),
	path('tarif_gudang/<str:id_gudang_1>/<str:id_gudang_2>/', csrf_exempt(HitungTarifGudang.as_view()), name='hitung_tarif_gudang'),

	path('tarif_kilometer/', csrf_exempt(TarifKilometerView.as_view()), name='tarif_kilometer'),
	path('tarif_kilometer/<str:id>/delete/', csrf_exempt(TarifKilometerDelete.as_view()), name='tarif_kilometer_delete'),
	path('tarif_kilometer/<str:id>/detail/', csrf_exempt(TarifKilometerDetail.as_view()), name='tarif_kilometer_detail'),
	path('tarif_kilometer/<str:id>/update/', csrf_exempt(TarifKilometerDetail.as_view()), name='tarif_kilometer_update'),
	path('tarif_kilometer/<str:kilometer>/harga/', csrf_exempt(HitungTarifKilometer.as_view()), name='harga_tarif_kilometer'),

	path('tarif_berat/', csrf_exempt(TarifBeratView.as_view()), name='tarif_berat'),
	path('tarif_berat/<str:id>/delete/', csrf_exempt(TarifBeratDelete.as_view()), name='tarif_berat_delete'),
	path('tarif_berat/<str:id>/detail/', csrf_exempt(TarifBeratDetail.as_view()), name='tarif_berat_detail'),
	path('tarif_berat/<str:id>/update/', csrf_exempt(TarifBeratDetail.as_view()), name='tarif_berat_update'),
	path('tarif_berat/<str:berat>/harga/', csrf_exempt(HitungTarifBerat.as_view()), name='harga_tarif_berat'),

	path('tarif_layanan/', TarifLayananView.as_view(), name='tarif_layanan'),
	path('tarif_layanan/delete/', TarifLayananDelete.as_view(), name='tarif_layanan_delete'),
	path('tarif_layanan/detail/', TarifLayananDetail.as_view(), name='tarif_layanan_detail'),
	path('tarif_layanan/update/', TarifLayananDetail.as_view(), name='tarif_layanan_update'),
	path('tarif_layanan/<str:id_layanan>/harga/', csrf_exempt(HitungTarifLayanan.as_view()), name='harga_tarif_layanan'),

	path('pengiriman/cek_outlet_gudang_by_kecamatan', csrf_exempt(PengirimanPilihOutletGudangManual.as_view()), name='pengiriman_cek_manual'),
	path('pengiriman/', csrf_exempt(PengirimanView.as_view()), name='pengiriman'),
	path('pengiriman/<str:id>/bukti_tanda_terima/', csrf_exempt(PengirimanTandaTerima.as_view()), name='pengiriman_bukti_tanda_terima'),
	path('pengiriman/<str:id>/delete/', csrf_exempt(PengirimanDelete.as_view()), name='pengiriman_delete'),
	path('pengiriman/<str:id>/detail/', csrf_exempt(PengirimanDetail.as_view()), name='pengiriman_detail'),
	path('pengiriman/<str:id>/update/', csrf_exempt(PengirimanDetail.as_view()), name='pengiriman_update'),
	path('pengiriman/<str:id>/arsip/', csrf_exempt(PengirimanArsip.as_view()), name='pengiriman_arsip'),
	path('pengiriman/<str:id>/unarsip/', csrf_exempt(PengirimanUnarsip.as_view()), name='pengiriman_unarsip'),
	path('pengiriman/<str:id>/print_billing/', csrf_exempt(GenerateInvoicePdf.as_view()), name='pengiriman_print_billing'),
	path('pengiriman/<str:id>/print_label/', csrf_exempt(GenerateLabelPdf.as_view()), name='pengiriman_print_label'),
	path('pengiriman/arsip/list/', csrf_exempt(PengirimanArsipView.as_view()), name='pengiriman_arsip_list'),
	path('pengiriman/update/pos', csrf_exempt(PengirimanPOS.as_view()), name='pengiriman_pos'),
	path('pos/list', csrf_exempt(PengirimanPOSView.as_view()), name="pos_list"),
	path('pos/report', csrf_exempt(PengirimanPOSReportView.as_view()), name="pos_report"),
  

	path('extra_cash/', ExtraCashView.as_view(), name='extra_cash'),
	path('extra_cash/delete/', ExtraCashDelete.as_view(), name='extra_cash_delete'),
	path('extra_cash/detail/', ExtraCashDetail.as_view(), name='extra_cash_detail'),
	path('extra_cash/update/', ExtraCashUpdate.as_view(), name='extra_cash_update'),
	path('extra_cash/activated/', ExtraCashActivate.as_view(), name='extra_cash_activate'),
	path('extra_cash/data/', GetExtraCash.as_view(), name='extra_cash_check'),

	path('satuan/', SatuanView.as_view(), name='satuan'),
	path('satuan/delete/', SatuanDelete.as_view(), name='satuan_delete'),
	path('satuan/detail/', SatuanDetail.as_view(), name='satuan_detail'),
	path('satuan/update/', SatuanDetail.as_view(), name='satuan_update'),
	path('satuan/arsip/', SatuanArsip.as_view(), name='satuan_asrip'),
	path('satuan/unarsip/', SatuanUnarsip.as_view(), name='satuan_unasrip'),
	path('api/satuan/', SatuanAPIView.as_view(), name='api_satuan'),
	path('satuan/select2/', SatuanToSelect2.as_view(), name='satuan_select2'),

	path('jenis_kiriman/', JenisKirimanView.as_view(), name='jenis_kiriman'),
	path('jenis_kiriman/delete/', JenisKirimanDelete.as_view(), name='jenis_kiriman_delete'),
	path('jenis_kiriman/detail/', JenisKirimanDetail.as_view(), name='jenis_kiriman_detail'),
	path('jenis_kiriman/update/', JenisKirimanDetail.as_view(), name='jenis_kiriman_update'),
	path('jenis_kiriman/arsip/', JenisKirimanArsip.as_view(), name='jenis_kiriman_asrip'),
	path('jenis_kiriman/unarsip/', JenisKirimanUnarsip.as_view(), name='jenis_kiriman_unasrip'),
	path('api/jenis_barang/', JenisKirimanAPIView.as_view(), name='api_jenis_kiriman'),
	path('jenis_kiriman/select2/', JenisKirimanToSelect2.as_view(), name='jenis_kiriman_select2'),

	path('ajax/lokasi/', csrf_exempt(ProvinsiView.as_view()), name='list_provinsi'),
	path('ajax/lokasi/select2/', ProvinsiToSelect2.as_view(), name='provinsi_select2'),
	path('ajax/lokasi/<str:provinsi_id>/kota/', csrf_exempt(KotaView.as_view()), name='kota_di_provinsi'),
	path('ajax/lokasi/<str:kota_id>/kecamatan/', csrf_exempt(KecamatanView.as_view()), name='kecamatan_di_kota'),
	path('ajax/lokasi/<str:kecamatan_id>/desa/', csrf_exempt(DesaView.as_view()), name='desa_di_kecamatan'),
	path('ajax/lokasi/<str:provinsi_id>/<str:kota_id>/<str:kecamatan_id>/<str:desa_id>/kode/', csrf_exempt(KodePosView.as_view()), name='kodepos_di_desa'),
	path('ajax/apikey/', csrf_exempt(GetApiKey.as_view()), name='api_key'),
	path('ajax/lokasi_terkini/', csrf_exempt(LokasiUpdate.as_view()), name='current_location'),

]