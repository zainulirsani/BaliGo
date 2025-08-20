def ambil_data_gudang(data):
    if data.provinsi_gudang:
        data_provinsi_gudang = data.provinsi_gudang.nama_provinsi
        id_provinsi_gudang = data.provinsi_gudang.id
    else:
        data_provinsi_gudang = ''
        id_provinsi_gudang = ''

    if data.kota_gudang:
        data_kota_gudang = data.kota_gudang.nama_kota
        id_kota_gudang = data.kota_gudang.id
    else:
        data_kota_gudang = ''
        id_kota_gudang = ''

    if data.kecamatan_gudang:
        data_kecamatan_gudang = data.kecamatan_gudang.nama_kecamatan
        id_kecamatan_gudang = data.kecamatan_gudang.id
    else:
        data_kecamatan_gudang = ''
        id_kecamatan_gudang = ''

    if data.desa_gudang:
        data_desa_gudang = data.desa_gudang.nama_desa
        id_desa_gudang = data.desa_gudang.id
    else:
        data_desa_gudang = ''
        id_desa_gudang = ''

    if data.kode_pos_gudang:
        data_kode_pos_gudang = data.kode_pos_gudang.kode_pos
        id_kode_pos_gudang = data.kode_pos_gudang.id
    else:
        data_kode_pos_gudang = ''
        id_kode_pos_gudang = ''


    data = {
        'id': data.id, 
        'id_gudang': data.id_gudang, 
        'nama_gudang': data.nama_gudang, 
        'no_tlp': data.no_tlp, 
        'alamat': data.alamat, 
        'titik_lokasi': data.titik_lokasi, 
        'radius': data.radius, 
        'id_provinsi_gudang': id_provinsi_gudang,
        'provinsi_gudang': data_provinsi_gudang,
        'id_kota_gudang': id_kota_gudang, 
        'kota_gudang': data_kota_gudang, 
        'id_kecamatan_gudang': id_kecamatan_gudang, 
        'kecamatan_gudang': data_kecamatan_gudang, 
        'id_desa_gudang': id_desa_gudang, 
        'desa_gudang': data_desa_gudang, 
        'id_kode_pos_gudang': id_kode_pos_gudang,
        'kode_pos_gudang': data_kode_pos_gudang,
    }

    return data