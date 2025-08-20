function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function show_provinsi_list() {
    try {
        var id_provinsi = document.getElementById('provinsi_id').value;
        $.ajax({
            type: "POST",
            url: $("#register-form").data('url_provinsi'),
            success: function(response) {
                $("select#id-provinsi").append(response.data);
                $('select#id-provinsi').val(id_provinsi);
            }
        });
    } catch(error){}
}
show_provinsi_list();

function show_kota_list(id_provinsi, id_kota_select, nama_kota) {
    try{
        var id_provinsi = document.getElementById('provinsi_id').value;
        var id_kota = document.getElementById('kota_id').value;
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#register-form").data('url_provinsi') + id_provinsi + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinsi
            },

            success: function(response) {
                // console.log(response.data);
                $("select#id-kota").html(response.data);
                document.getElementById("id-kota").value = id_kota;
                try {
                    document.getElementById("select2-id-kota-container").innerHTML = nama_kota;
                } catch(error){}
            }
        });
    } catch(error){}
}
show_kota_list();

function show_kecamatan_list(id_kota, id_kecamatan_select, nama_kecamatan) {
    try {
        var id_kecamatan = document.getElementById('kecamatan_id').value;
        var id_kota = document.getElementById('kota_id').value;
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#register-form").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },

            success: function(response) {
                // console.log(response.data);
                $("select#id-kecamatan").html(response.data);
                document.getElementById("id-kecamatan").value = id_kecamatan;
                try {
                    document.getElementById("select2-id-kecamatan-container").innerHTML = nama_kecamatan;
                } catch(error){}
            }
        });
    } catch(error){}
}
show_kecamatan_list();

function show_desa_list(id_kecamatan, id_desa_select, nama_desa) {
    try {
        var id_kecamatan = document.getElementById('kecamatan_id').value;
        var id_desa = document.getElementById('desa_id').value;
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#register-form").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },

            success: function(response) {
                // console.log(response.data);
                $("select#id-desa").html(response.data);
                document.getElementById("id-desa").value = id_desa;
                try {
                    document.getElementById("select2-id-desa-container").innerHTML = nama_desa;
                } catch(error){}
            }
        });
    } catch(error){}
}
show_desa_list();

function show_kode_pos_list(id_provinces, id_kota, id_kecamatan, id_desa, id_kode_pos_select, kode_pos) {
    try {
        var id_provinces = document.getElementById('provinsi_id').value;
        var id_kota = document.getElementById('kota_id').value;
        var id_kecamatan = document.getElementById('kecamatan_id').value;
        var id_desa = document.getElementById('desa_id').value;
        var id_kode_pos = document.getElementById('kode-pos_id').value;

        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#register-form").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },

            success: function(response) {
                // console.log(response.data);
                $("select#id-kode_pos").html(response.data);
                document.getElementById("id-kode_pos").value = id_kode_pos;
                try {
                    document.getElementById("select2-id-kode_pos-container").innerHTML = kode_pos;
                } catch(error){}
            }
        });
    } catch(error){}
}
show_kode_pos_list();

$(document).on('change', '#id-provinsi', function(e){
	var id_provinces = $(this).val();
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: "application/json",
        url: $("#register-form").data('url_provinsi') + id_provinces + '/kota/',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            provinsi_id: id_provinces
        },

        success: function(response) {
            // // console.log(response.data);
            $("select#id-kota").html(response.data);
            getAjaxKota();
        }
    });
});


$("#id-kota").change(getAjaxKota);
function getAjaxKota() {
    var id_kota = $("#id-kota").val();
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: "application/json",
        url: $("#register-form").data('url_provinsi') + id_kota + '/kecamatan/',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            kota_id: id_kota
        },
        success: function(response) {
            $("select#id-kecamatan").html(response.data);
            getAjaxKecamatan();
        }
    });
}

$("#id-kecamatan").change(getAjaxKecamatan);
function getAjaxKecamatan() {
    var id_kecamatan = $("#id-kecamatan").val();
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: "application/json",
        url: $("#register-form").data('url_provinsi') + id_kecamatan + '/desa/',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            kecamatan_id: id_kecamatan
        },
        success: function(response) {
            $("select#id-desa").html(response.data);
            getAjaxDesa();
        }
    });
}

$("#id-desa").change(getAjaxDesa);
function getAjaxDesa() {
        var id_provinces = $("#id-provinsi").val();
        var id_kota = $("#id-kota").val();
        var id_kecamatan = $("#id-kecamatan").val();
        var id_desa = $("#id-desa").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#register-form").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },
            success: function(response) {
                $("select#id-kode_pos").html(response.data);
            }
        });
    }