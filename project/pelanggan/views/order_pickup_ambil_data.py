def ambil_data(order):
    if order.provinsi_pengirim:
        data_provinsi_pengirim = order.provinsi_pengirim.nama_provinsi
        id_provinsi_pengirim = order.provinsi_pengirim.id
    else:
        data_provinsi_pengirim = ''
        id_provinsi_pengirim = ''

    if order.id_toko:
        data_outlet_order = order.id_toko.nama_toko
        id_outlet_order = order.id_toko.id
    else:
        data_outlet_order = ''
        id_outlet_order = ''

    if order.id_gudang:
        data_gudang_order = order.id_gudang.nama_gudang
        id_gudang_order = order.id_gudang.id
    else:
        data_gudang_order = ''
        id_gudang_order = ''

    if order.kota_pengirim:
        data_kota_pengirim = order.kota_pengirim.nama_kota
        id_kota_pengirim = order.kota_pengirim.id
    else:
        data_kota_pengirim = ''
        id_kota_pengirim = ''

    if order.kecamatan_pengirim:
        data_kecamatan_pengirim = order.kecamatan_pengirim.nama_kecamatan
        id_kecamatan_pengirim = order.kecamatan_pengirim.id
    else:
        data_kecamatan_pengirim = ''
        id_kecamatan_pengirim = ''

    if order.desa_pengirim:
        data_desa_pengirim = order.desa_pengirim.nama_desa
        id_desa_pengirim = order.desa_pengirim.id
    else:
        data_desa_pengirim = ''
        id_desa_pengirim = ''

    if order.kode_pos_pengirim:
        data_kode_pos_pengirim = order.kode_pos_pengirim.kode_pos
        id_kode_pos_pengirim = order.kode_pos_pengirim.id
    else:
        data_kode_pos_pengirim = ''
        id_kode_pos_pengirim = ''

    #=======================================================================
    
    if order.provinsi_penerima:
        data_provinsi_penerima = order.provinsi_penerima.nama_provinsi
        id_provinsi_penerima = order.provinsi_penerima.id
    else:
        data_provinsi_penerima = ''
        id_provinsi_penerima = ''

    if order.id_toko2:
        data_outlet_penerimaan = order.id_toko2.nama_toko
        id_outlet_penerimaan = order.id_toko2.id
    else:
        data_outlet_penerimaan = ''
        id_outlet_penerimaan = ''

    if order.id_gudang2:
        data_gudang_penerima = order.id_gudang2.nama_gudang
        id_gudang_penerima = order.id_gudang2.id
    else:
        data_gudang_penerima = ''
        id_gudang_penerima = ''

    if order.kota_penerima:
        data_kota_penerima = order.kota_penerima.nama_kota
        id_kota_penerima = order.kota_penerima.id
    else:
        data_kota_penerima = ''
        id_kota_penerima = ''

    if order.kecamatan_penerima:
        data_kecamatan_penerima = order.kecamatan_penerima.nama_kecamatan
        id_kecamatan_penerima = order.kecamatan_penerima.id
    else:
        data_kecamatan_penerima = ''
        id_kecamatan_penerima = ''

    if order.desa_penerima:
        data_desa_penerima = order.desa_penerima.nama_desa
        id_desa_penerima = order.desa_penerima.id
    else:
        data_desa_penerima = ''
        id_desa_penerima = ''

    if order.kode_pos_penerima:
        data_kode_pos_penerima = order.kode_pos_penerima.kode_pos
        id_kode_pos_penerima = order.kode_pos_penerima.id
    else:
        data_kode_pos_penerima = ''
        id_kode_pos_penerima = ''
    #============================================
    if order.id_pengemasan:
        data_pengemasan = order.id_pengemasan.nama_pengemasan
        id_pengemasan = order.id_pengemasan.id
        tarif_pengemasan = order.id_pengemasan.tarif
    else:
        data_pengemasan = ''
        id_pengemasan = ''
        tarif_pengemasan = ''

    if order.jenis_pengiriman:
        data_layanan = order.jenis_pengiriman.nama_layanan
        id_layanan = order.jenis_pengiriman.id
    else:
        data_layanan = ''
        id_layanan = ''

    if order.satuan:
        data_satuan = order.satuan.nama_satuan
        id_satuan = order.satuan.id
    else:
        data_satuan = ''
        id_satuan = ''

    if order.keterangan_cancel:
        keterangan_cancel = order.keterangan_cancel
    else:
        keterangan_cancel = ''

    if order.extra_tarif_pengirim:
        data_extra_tarif_pengirim = order.extra_tarif_pengirim
    else:
        data_extra_tarif_pengirim = ''

    if order.extra_tarif_penerima:
        data_extra_tarif_penerima = order.extra_tarif_penerima
    else:
        data_extra_tarif_penerima = ''

    if order.keterangan_extra_tarif:
        data_keterangan_extra_tarif = order.keterangan_extra_tarif
    else:
        data_keterangan_extra_tarif = ''


    data = {
        'id': order.id ,

        'id_order': order.id_order, 
        'outlet_order': data_outlet_order,
        'id_outlet_order': id_outlet_order, 
        'gudang_order': data_gudang_order,
        'id_gudang_order': id_gudang_order,
            
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
        
        'nama_penerima': order.nama_penerima,
        'no_tlp_penerima': order.no_tlp_penerima,
        'email_penerima': order.email_penerima,
        'alamat_penerima': order.alamat_penerima,
        'alamat_pengirim_alt': order.alamat_pengirim_alt,
                
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
        'gudang_penerimaan': data_gudang_penerima,
        'id_gudang_penerimaan': id_gudang_penerima,
        'jenis_barang': order.jenis_barang,
        'jumlah_barang': order.jumlah,
        'detail_barang': order.detail_barang,
        'satuan': data_satuan,
        'id_satuan':id_satuan,
        'pengemasan': data_pengemasan,
        'id_pengemasan': id_pengemasan,
        'layanan': data_layanan,
        'id_layanan': id_layanan,
        'berat': order.berat,
        'tarif_berat': order.tarif_berat,
        'tarif_kilometer': order.tarif_kilometer,
        'tarif_gudang': order.tarif_gudang,
        'tarif_layanan': order.tarif_layanan,
        'tarif_pengemasan': tarif_pengemasan,
        'total_tarif': order.total_tarif,
        'status': order.status,
        'created_at': order.created_at,
        'extra_tarif_pengirim': data_extra_tarif_pengirim,
        'extra_tarif_penerima': data_extra_tarif_penerima,
        'keterangan_extra_tarif': data_keterangan_extra_tarif,
    }
    return data

def ambil_rute(order):
    if order.id_toko:
        data_outlet_1 = order.id_toko.nama_toko
        data_outlet_1_id = order.id_toko.id
        data_outlet_1_lokasi = order.id_toko.titik_lokasi
        data_outlet_1_alamat = order.id_toko.alamat
        data_outlet_1_kontak = order.id_toko.kontak
    else:
        data_outlet_1 = ''
        data_outlet_1_id = ''
        data_outlet_1_lokasi = ''
        data_outlet_1_alamat = ''
        data_outlet_1_kontak = ''

    if order.id_toko2:
        data_outlet_2 = order.id_toko2.nama_toko
        data_outlet_2_id = order.id_toko2.id
        data_outlet_2_lokasi = order.id_toko2.titik_lokasi
        data_outlet_2_alamat = order.id_toko2.alamat
        data_outlet_2_kontak = order.id_toko2.kontak
    else:
        data_outlet_2 = ''
        data_outlet_2_id = ''
        data_outlet_2_lokasi = ''
        data_outlet_2_alamat = ''
        data_outlet_2_kontak = ''

    if order.id_gudang:
        data_gudang_1 = order.id_gudang.nama_gudang
        data_gudang_1_id = order.id_gudang.id
        data_gudang_1_lokasi = order.id_gudang.titik_lokasi
        data_gudang_1_alamat = order.id_gudang.alamat
        data_gudang_1_kontak = order.id_gudang.no_tlp
    else:
        data_gudang_1 = ''
        data_gudang_1_id = ''
        data_gudang_1_lokasi = ''
        data_gudang_1_alamat = ''
        data_gudang_1_kontak = ''

    if order.id_gudang2:
        data_gudang_2 = order.id_gudang2.nama_gudang
        data_gudang_2_id = order.id_gudang2.id
        data_gudang_2_lokasi = order.id_gudang2.titik_lokasi
        data_gudang_2_alamat = order.id_gudang2.alamat
        data_gudang_2_kontak = order.id_gudang2.no_tlp
    else:
        data_gudang_2 = ''
        data_gudang_2_id = ''
        data_gudang_2_lokasi = ''
        data_gudang_2_alamat = ''
        data_gudang_2_kontak = ''

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
    }
    return data