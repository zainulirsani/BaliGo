def ambil_data_toko(data):
    if data.provinsi_toko:
        data_provinsi_toko = data.provinsi_toko.nama_provinsi
        id_provinsi_toko = data.provinsi_toko.id
    else:
        data_provinsi_toko = ''
        id_provinsi_toko = ''

    if data.kota_toko:
        data_kota_toko = data.kota_toko.nama_kota
        id_kota_toko = data.kota_toko.id
    else:
        data_kota_toko = ''
        id_kota_toko = ''

    if data.kecamatan_toko:
        data_kecamatan_toko = data.kecamatan_toko.nama_kecamatan
        id_kecamatan_toko = data.kecamatan_toko.id
    else:
        data_kecamatan_toko = ''
        id_kecamatan_toko = ''

    if data.desa_toko:
        data_desa_toko = data.desa_toko.nama_desa
        id_desa_toko = data.desa_toko.id
    else:
        data_desa_toko = ''
        id_desa_toko = ''

    if data.kode_pos_toko:
        data_kode_pos_toko = data.kode_pos_toko.kode_pos
        id_kode_pos_toko = data.kode_pos_toko.id
    else:
        data_kode_pos_toko = ''
        id_kode_pos_toko = ''


    data = {
        'id': data.id, 
        'id_toko': data.id_toko, 
        'nama_toko': data.nama_toko, 
        'no_tlp': data.kontak, 
        'alamat': data.alamat, 
        'titik_lokasi': data.titik_lokasi, 
        'radius': data.radius, 
        'id_provinsi_toko': id_provinsi_toko,
        'provinsi_toko': data_provinsi_toko,
        'id_kota_toko': id_kota_toko, 
        'kota_toko': data_kota_toko, 
        'id_kecamatan_toko': id_kecamatan_toko, 
        'kecamatan_toko': data_kecamatan_toko, 
        'id_desa_toko': id_desa_toko, 
        'desa_toko': data_desa_toko, 
        'id_kode_pos_toko': id_kode_pos_toko,
        'kode_pos_toko': data_kode_pos_toko,
    }

    return data