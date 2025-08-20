def ambil_data(pengiriman):
    if pengiriman.provinsi_pengirim:
        data_provinsi_pengirim = pengiriman.provinsi_pengirim.nama_provinsi
        id_provinsi_pengirim = pengiriman.provinsi_pengirim.id
    else:
        data_provinsi_pengirim = ''
        id_provinsi_pengirim = ''

    if pengiriman.outlet_pengiriman:
        data_outlet_pengiriman = pengiriman.outlet_pengiriman.nama_toko
        id_outlet_pengiriman = pengiriman.outlet_pengiriman.id
    else:
        data_outlet_pengiriman = ''
        id_outlet_pengiriman = ''

    if pengiriman.kota_pengirim:
        data_kota_pengirim = pengiriman.kota_pengirim.nama_kota
        id_kota_pengirim = pengiriman.kota_pengirim.id
    else:
        data_kota_pengirim = ''
        id_kota_pengirim = ''

    if pengiriman.kecamatan_pengirim:
        data_kecamatan_pengirim = pengiriman.kecamatan_pengirim.nama_kecamatan
        id_kecamatan_pengirim = pengiriman.kecamatan_pengirim.id
    else:
        data_kecamatan_pengirim = ''
        id_kecamatan_pengirim = ''

    if pengiriman.desa_pengirim:
        data_desa_pengirim = pengiriman.desa_pengirim.nama_desa
        id_desa_pengirim = pengiriman.desa_pengirim.id
    else:
        data_desa_pengirim = ''
        id_desa_pengirim = ''

    if pengiriman.kode_pos_pengirim:
        data_kode_pos_pengirim = pengiriman.kode_pos_pengirim.kode_pos
        id_kode_pos_pengirim = pengiriman.kode_pos_pengirim.id
    else:
        data_kode_pos_pengirim = ''
        id_kode_pos_pengirim = ''

    #=======================================================================
    
    if pengiriman.provinsi_penerima:
        data_provinsi_penerima = pengiriman.provinsi_penerima.nama_provinsi
        id_provinsi_penerima = pengiriman.provinsi_penerima.id
    else:
        data_provinsi_penerima = ''
        id_provinsi_penerima = ''

    if pengiriman.outlet_penerimaan:
        data_outlet_penerimaan = pengiriman.outlet_penerimaan.nama_toko
        id_outlet_penerimaan = pengiriman.outlet_penerimaan.id
    else:
        data_outlet_penerimaan = ''
        id_outlet_penerimaan = ''

    if pengiriman.kota_penerima:
        data_kota_penerima = pengiriman.kota_penerima.nama_kota
        id_kota_penerima = pengiriman.kota_penerima.id
    else:
        data_kota_penerima = ''
        id_kota_penerima = ''

    if pengiriman.kecamatan_penerima:
        data_kecamatan_penerima = pengiriman.kecamatan_penerima.nama_kecamatan
        id_kecamatan_penerima = pengiriman.kecamatan_penerima.id
    else:
        data_kecamatan_penerima = ''
        id_kecamatan_penerima = ''

    if pengiriman.desa_penerima:
        data_desa_penerima = pengiriman.desa_penerima.nama_desa
        id_desa_penerima = pengiriman.desa_penerima.id
    else:
        data_desa_penerima = ''
        id_desa_penerima = ''

    if pengiriman.kode_pos_penerima:
        data_kode_pos_penerima = pengiriman.kode_pos_penerima.kode_pos
        id_kode_pos_penerima = pengiriman.kode_pos_penerima.id
    else:
        data_kode_pos_penerima = ''
        id_kode_pos_penerima = ''
    #============================================
    if pengiriman.pengemasan:
        data_pengemasan = pengiriman.pengemasan.nama_pengemasan
        id_pengemasan = pengiriman.pengemasan.id
    else:
        data_pengemasan = ''
        id_pengemasan = ''

    if pengiriman.detail_barang:
        data_detail_barang = pengiriman.detail_barang
    else:
        data_detail_barang = ''

    if pengiriman.layanan:
        data_layanan = pengiriman.layanan.nama_layanan
        id_layanan = pengiriman.layanan.id
    else:
        data_layanan = ''
        id_layanan = ''

    if pengiriman.pencatat:
        data_pencatat = pengiriman.pencatat.first_name
        id_pencatat = pengiriman.pencatat.id
    else:
        data_pencatat = ''
        id_pencatat = ''

    if pengiriman.pengemasan:
        if hasattr(pengiriman, 'tarif_pengemasan') and pengiriman.tarif_pengemasan :
            tarif_pengemasan = pengiriman.tarif_pengemasan
        else :
            tarif_pengemasan = pengiriman.pengemasan.tarif
    else:
        tarif_pengemasan = '0'
 
    if pengiriman.extra_tarif_pengirim:
        data_extra_tarif_pengirim = pengiriman.extra_tarif_pengirim
    else:
        data_extra_tarif_pengirim = '0'

    if pengiriman.extra_tarif_penerima:
        data_extra_tarif_penerima = pengiriman.extra_tarif_penerima
    else:
        data_extra_tarif_penerima = '0'

    if pengiriman.keterangan_extra_tarif:
        data_keterangan_extra_tarif = pengiriman.keterangan_extra_tarif
    else:
        data_keterangan_extra_tarif = ''

    if pengiriman.satuan:
        data_satuan = pengiriman.satuan.nama_satuan
        id_satuan = pengiriman.satuan.id
    else:
        data_satuan = ''
        id_satuan = ''



    data = {
        'id': pengiriman.id ,

        'id_pengiriman': pengiriman.id_pengiriman, 
        'outlet_pengiriman': data_outlet_pengiriman,
        'id_outlet_pengiriman': id_outlet_pengiriman, 
        'nama_pengirim': pengiriman.nama_pengirim, 
        'no_telp_pengirim': pengiriman.no_telp_pengirim, 
        'email_pengirim': pengiriman.email_pengirim, 
        'alamat_pengirim': pengiriman.alamat_pengirim, 
            
        'provinsi_pengirim': data_provinsi_pengirim,
        'id_provinsi_pengirim': id_provinsi_pengirim,
        'kota_pengirim': data_kota_pengirim,
        'id_kota_pengirim': id_kota_pengirim,
        'kecamatan_pengirim': data_kecamatan_pengirim,
        'id_kecamatan_pengirim': id_kecamatan_pengirim,
        'desa_pengirim': data_desa_pengirim,
        'id_desa_pengirim': id_desa_pengirim,
        'kode_pos_pengirim': data_kode_pos_pengirim,
        'id_kode_pos_pengirim': id_kode_pos_pengirim,
        
        'nama_penerima': pengiriman.nama_penerima,
        'no_telp_penerima': pengiriman.no_telp_penerima,
        'email_penerima': pengiriman.email_penerima,
        'alamat_penerima': pengiriman.alamat_penerima,
                
        'provinsi_penerima': data_provinsi_penerima,
        'id_provinsi_penerima': id_provinsi_penerima,
        'kota_penerima': data_kota_penerima,
        'id_kota_penerima': id_kota_penerima,
        'kecamatan_penerima': data_kecamatan_penerima,
        'id_kecamatan_penerima': id_kecamatan_penerima,
        'desa_penerima': data_desa_penerima,
        'id_desa_penerima': id_desa_penerima,
        'kode_pos_penerima': data_kode_pos_penerima,
        'id_kode_pos_penerima': id_kode_pos_penerima,
            
        'outlet_penerimaan': data_outlet_penerimaan,
        'id_outlet_penerimaan': id_outlet_penerimaan,
        'jenis_barang': pengiriman.jenis_barang,
        'detail_barang': data_detail_barang,
        'pengemasan': data_pengemasan,
        'id_pengemasan': id_pengemasan,
        'layanan': data_layanan,
        'id_layanan': id_layanan,
        'berat': pengiriman.berat,
        'jumlah': pengiriman.jumlah,
        'data_satuan': data_satuan,
        'id_satuan': id_satuan,
        'pencatat': data_pencatat,
        'id_pencatat': id_pencatat,
        'tarif_berat': pengiriman.tarif_berat,
        'tarif_kilometer': pengiriman.tarif_kilometer,
        'tarif_gudang': pengiriman.tarif_gudang,
        'tarif_layanan': pengiriman.tarif_layanan,
        'tarif_pengemasan': tarif_pengemasan,
        'total_tarif': pengiriman.total_tarif,
        'tarif_lain' : pengiriman.tarif_lain,
        'extra_tarif_pengirim': data_extra_tarif_pengirim,
        'extra_tarif_penerima': data_extra_tarif_penerima,
        'keterangan_extra_tarif': data_keterangan_extra_tarif,

        'created_at': pengiriman.created_at,
        'qr_code': '{% qr_from_text "'+pengiriman.id_pengiriman+'" size="M" %}',
    }
    return data

def ambil_rute(log_pengiriman):
    if log_pengiriman.rute_pengiriman_outlet:
        data_outlet_1 = log_pengiriman.rute_pengiriman_outlet.nama_toko
        data_outlet_1_id = log_pengiriman.rute_pengiriman_outlet.id
        data_outlet_1_lokasi = log_pengiriman.rute_pengiriman_outlet.titik_lokasi
        data_outlet_1_alamat = log_pengiriman.rute_pengiriman_outlet.alamat
        data_outlet_1_kontak = log_pengiriman.rute_pengiriman_outlet.kontak
    else:
        data_outlet_1 = ''
        data_outlet_1_id = ''
        data_outlet_1_lokasi = ''
        data_outlet_1_alamat = ''
        data_outlet_1_kontak = ''

    if log_pengiriman.rute_pengiriman_outlet_akhir:
        data_outlet_2 = log_pengiriman.rute_pengiriman_outlet_akhir.nama_toko
        data_outlet_2_id = log_pengiriman.rute_pengiriman_outlet_akhir.id
        data_outlet_2_lokasi = log_pengiriman.rute_pengiriman_outlet_akhir.titik_lokasi
        data_outlet_2_alamat = log_pengiriman.rute_pengiriman_outlet_akhir.alamat
        data_outlet_2_kontak = log_pengiriman.rute_pengiriman_outlet_akhir.kontak
    else:
        data_outlet_2 = ''
        data_outlet_2_id = ''
        data_outlet_2_lokasi = ''
        data_outlet_2_alamat = ''
        data_outlet_2_kontak = ''

    if log_pengiriman.rute_pengiriman_gudang:
        data_gudang_1 = log_pengiriman.rute_pengiriman_gudang.nama_gudang
        data_gudang_1_id = log_pengiriman.rute_pengiriman_gudang.id
        data_gudang_1_lokasi = log_pengiriman.rute_pengiriman_gudang.titik_lokasi
        data_gudang_1_alamat = log_pengiriman.rute_pengiriman_gudang.alamat
        data_gudang_1_kontak = log_pengiriman.rute_pengiriman_gudang.no_tlp
    else:
        data_gudang_1 = ''
        data_gudang_1_id = ''
        data_gudang_1_lokasi = ''
        data_gudang_1_alamat = ''
        data_gudang_1_kontak = ''

    if log_pengiriman.rute_pengiriman_gudang_akhir:
        data_gudang_2 = log_pengiriman.rute_pengiriman_gudang_akhir.nama_gudang
        data_gudang_2_id = log_pengiriman.rute_pengiriman_gudang_akhir.id
        data_gudang_2_lokasi = log_pengiriman.rute_pengiriman_gudang_akhir.titik_lokasi
        data_gudang_2_alamat = log_pengiriman.rute_pengiriman_gudang_akhir.alamat
        data_gudang_2_kontak = log_pengiriman.rute_pengiriman_gudang_akhir.no_tlp
    else:
        data_gudang_2 = ''
        data_gudang_2_id = ''
        data_gudang_2_lokasi = ''
        data_gudang_2_alamat = ''
        data_gudang_2_kontak = ''

    status_pengiriman = log_pengiriman.status_pengiriman
    kurir = log_pengiriman.id_kurir
    if kurir :
        kurir = kurir.id
    

    data = {
        'outlet_1': {
            'id': data_outlet_1_id,
            'nama': data_outlet_1,
            'alamat': data_outlet_1_alamat,
            'titik_lokasi': data_outlet_1_lokasi,
            'kontak': data_outlet_1_kontak,
        },
        'outlet_2': {
            'id': data_outlet_2_id,
            'nama': data_outlet_2,
            'alamat': data_outlet_2_alamat,
            'titik_lokasi': data_outlet_2_lokasi,
            'kontak': data_outlet_2_kontak,
        },
        'gudang_1': {
            'id': data_gudang_1_id,
            'nama': data_gudang_1,
            'alamat': data_gudang_1_alamat,
            'titik_lokasi': data_gudang_1_lokasi,
            'kontak': data_gudang_1_kontak,
        },
        'gudang_2': {
            'id': data_gudang_2_id,
            'nama': data_gudang_2,
            'alamat': data_gudang_2_alamat,
            'titik_lokasi': data_gudang_2_lokasi,
            'kontak': data_gudang_2_kontak,
        },
        'status_pengiriman' : status_pengiriman,
        'kurir' : kurir
    }
    return data

def ambil_kurir(data):
    if data:
        id_kurir = data.id
        nama = data.first_name
        no_telp = data.no_telp
        penempatan = 'Tidak Diketahui'
        if data.penempatan_toko :
            penempatan = data.penempatan_toko.nama_toko
        elif data.penempatan_gudang :
            penempatan = data.penempatan_gudang.nama_gudang

    else:
        id_kurir = ''
        nama = ''
        no_telp = ''
        penempatan = ''

    data = {
        'id': id_kurir,
        'nama': nama,
        'kontak': no_telp,
        'penempatan': penempatan
    }
    return data

def ambil_status(data):
    if data:
        status = data.status_pengiriman
    else:
        status = ''

    data = {
        'data': status
    }
    return data