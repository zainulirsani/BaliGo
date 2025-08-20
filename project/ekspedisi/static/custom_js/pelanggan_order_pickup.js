$(document).ready(function() {
    function formatDate(date) {
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        var ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        hours = hours < 10 ? '0'+hours : hours;
        minutes = minutes < 10 ? '0'+minutes : minutes;
        seconds = seconds < 10 ? '0'+seconds : seconds;
        var strTime = hours + ':' + minutes + ':' + seconds + `-${ampm}`;
        // return (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "  " + strTime;
        return date.getFullYear() + "-" + ("0" + (date.getMonth()+1)).slice(-2) + "-" + date.getDate() + " " + strTime;
    }

    var csrfToken = getCookie('csrftoken');

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

    $("#createOrderForm")[0].reset();

    $('#modal_order').on('shown.bs.modal', function(e) {
        // Saat Modal terbuka sembunyakan tombol menu yang berhimpitan dengan tombol close modal
        document.getElementsByClassName('mobile-nav-toggle')[0].style.display = 'none';
    });

    $('#modal_order').on('hidden.bs.modal', function(e) {
        // saat modal tertutup
        document.getElementsByClassName('mobile-nav-toggle')[0].style.display = 'block';
    });


    $('#modal_cancel').on('shown.bs.modal', function(e) {
        // Saat Modal terbuka sembunyakan tombol menu yang berhimpitan dengan tombol close modal
        document.getElementsByClassName('mobile-nav-toggle')[0].style.display = 'none';
    });

    $('#modal_cancel').on('hidden.bs.modal', function(e) {
        // saat modal tertutup
        document.getElementsByClassName('mobile-nav-toggle')[0].style.display = 'block';
    });

    // ================================ Bagian Satuan ======================================
    $('#inputSatuan').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_satuan'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false, 
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Pilih Satuan',
        language: "id"
    });

    // ================================ END Bagian Satuan ==================================


    // ================================ Bagian Jenis barang/kiriman ======================================
    $('#id_jenis_barang').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_jenis_kiriman'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false, 
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                // console.log("JENIS BARANG",data);
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Pilih Jenis Barang',
        language: "id"
    });

    // ================================ END Bagian jenis barang/kiriman ==================================

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

    $(function() {
        $("input[name='no_tlp_penerima']").on('input', function(e) {
            $(this).val($(this).val().replace(/[^0-9]/g, ''));
        });
    });

    $(function() {
        $("input[name='berat']").on('input', function(e) {
            // $(this).val($(this).val().replace(/[^0-9]/g, ''));
        });
    });

    $(function() {
        $("input[name='jumlah']").on('input', function(e) {
            $(this).val($(this).val().replace(/[^0-9]/g, ''));
        });
    });

    



    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
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
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    function tampilkan_pesan(pesan, type) {
        Toast.fire({
            icon: type,
            title: pesan,
        });
    }

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        
    });

    // =====================================INITIALIZE============================================
    var api_key = $("#createOrderForm").data('api_open_route_service'); //API OPENROUTESERVICE

    var alamat_pengirim;
    var alamat_penerima;
    var lokasi_pengirim;
    var lokasi_penerima;
    var harga_pengemasan = 0;

    function getSelectedText(elementId) {
        var elt = document.getElementById(elementId);

        if (elt.selectedIndex == -1)
            return null;

        return elt.options[elt.selectedIndex].text;
    }

    function str2int(data) {
        if (data == '') {
            return 0;
        } else {
            return parseInt(data);
        }
    }


    $('#id_provinsi_pengirim').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_provinsi_select2'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false,
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Pilih Provinsi',
        language: "id"
    });
    $('#id_kota_pengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kota',
        language: "id"
    });
    $('#id_kecamatan_pengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kecamatan',
        language: "id"
    });
    $('#id_desa_pengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Desa',
        language: "id"
    });
    $('#id_kode_pos_pengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kode Pos',
        language: "id"
    });

    $('#id_provinsi_penerima').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_provinsi_select2'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false,
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Pilih Provinsi',
        language: "id"
    });
    $('#id_kota_penerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kota',
        language: "id"
    });
    $('#id_kecamatan_penerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kecamatan',
        language: "id"
    });
    $('#id_desa_penerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Desa',
        language: "id"
    });
    $('#id_kode_pos_penerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kode Pos',
        language: "id"
    });
    $('#id_jenis_pengiriman').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_layanan_select2'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false,
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Pilih Layanan Pengiriman',
        language: "id"
    });

    $('#id_id_pengemasan').select2({
        allowClear: true,
        ajax: {
            url: $("#createOrderForm").data('url_pengemasan'),
            dataType: "json",
            type: "GET",
            delay: 250,
            cache: false,
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1,
                }
            },
            processResults: function(data, params) {
                var page = params.page || 1;
                return {
                    results: $.map(data.results, function(item) {
                        return {
                            id: item.id,
                            text: item.text
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        theme: 'bootstrap4',
        placeholder: 'Tidak Perlu Pengemasan Lagi',
        language: "id"
    });

    function formatRupiah(angka, prefix) {
        if (angka.includes('.00')) {
            angka = angka.split('.00')[0];
        }
        var number_string = angka.replace(/[^,\d]/g, '').toString(),
            split = number_string.split(','),
            sisa = split[0].length % 3,
            rupiah = split[0].substr(0, sisa),
            ribuan = split[0].substr(sisa).match(/\d{3}/gi);

        // tambahkan titik jika yang di input sudah menjadi angka ribuan
        if (ribuan) {
            separator = sisa ? '.' : '';
            rupiah += separator + ribuan.join('.');
        }

        rupiah = split[1] != undefined ? rupiah + ',' + split[1] : rupiah;
        return prefix == undefined ? rupiah : (rupiah ? 'Rp. ' + rupiah : '');
    }

    function viewRupiah(input_id, output_id) {
        var input_number = document.getElementById(input_id).value;
        var output = formatRupiah(input_number, 'Rp. ');
        document.getElementById(output_id).value = output;
        document.getElementById(output_id).innerHTML = output;

    }

    function clear_rute_gudang() {
        document.getElementById('rute_gudang').innerHTML = "";
    }


    var table = $('#tabel_order').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "processing": true,
        "serverside": true,
        "ajax": {
            "url": $("#createOrderForm").data('url'),
            "type": "get"
        }
    });

    var table_pengiriman = $('#tabel_pengiriman').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "processing": true,
        "serverside": true,
        "ajax": {
            "url": $("#createOrderForm").data('url_pengiriman'),
            "type": "get"
        }
    });

    var table_history = $('#tabel_order_lama').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "processing": true,
        "serverside": true,
        "ajax": {
            "url": $("#createOrderForm").data('url_pengiriman_history'),
            "type": "get"
        }
    });

    //================================================= CREATE DATA (SHOW FORM) =================================
    $("#tambahOrder").click(function(e) {
        e.preventDefault();
        document.getElementById("title_modal").innerHTML = "Tambah Data Order";
        $("#createOrderForm :input").prop("disabled", false);
        $("#createOrderForm")[0].reset();

        alamat_pengirim = "";
        alamat_penerima = "";
        document.getElementById('custom-tabs-one-pengirim-tab').click();

        document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = 'Pilih Provinsi';
        document.getElementById("id_kota_pengirim").innerHTML = '';
        document.getElementById("id_kecamatan_pengirim").innerHTML = '';
        document.getElementById("id_desa_pengirim").innerHTML = '';
        document.getElementById("id_kode_pos_pengirim").innerHTML = '';

        document.getElementById("select2-id_provinsi_penerima-container").innerHTML = 'Pilih Provinsi';
        document.getElementById("id_kota_penerima").innerHTML = '';
        document.getElementById("id_kecamatan_penerima").innerHTML = '';
        document.getElementById("id_desa_penerima").innerHTML = '';
        document.getElementById("id_kode_pos_penerima").innerHTML = '';

        document.getElementById("select2-id_id_pengemasan-container").innerHTML = 'Tidak Perlu Pengemasan Lagi';
        document.getElementById("select2-id_jenis_pengiriman-container").innerHTML = '---------';

        document.getElementById("rute_gudang").innerHTML = '';
        document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '';
        
        document.getElementById("group_order_button").style.display = "block";
        document.getElementById("group_update_button").style.display = "none";
        document.getElementById("group_detail_button").style.display = "none";

        $("#nama_customer___").prop("disabled", true);
        $("#no_hp_customer___").prop("disabled", true);
        $("#email_customer___").prop("disabled", true);
        // $("#alamat_customer___").prop("disabled", true);

        try {
            var id_pelanggan = $('#id_customer').val();
            $.ajax({
                url: $("#createOrderForm").data('url_pelanggan') + 'detail/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id: id_pelanggan
                },
                type: 'get',
                success: function(response) {
                    if(typeof response === 'object' && response !== null){
                        // // console.log(response)
                        $_provinsi = null;
                        try {
                            // $('#id_provinsi_pengirim').val(null).trigger('change');
                            // $('#id_kota_pengirim').val(null).trigger('change');
                            // $('#id_kecamatan_pengirim').val(null).trigger('change');
                            // $('#id_desa_pengirim').val(null).trigger('change');
                            // $('#id_kode_pos_pengirim').val(null).trigger('change');
                            
                            // $_provinsi = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.provinsi : 0;
                            // if($_provinsi){
                            //     setTimeout(function(){
                            //         $('#id_provinsi_pengirim').val($_provinsi).trigger('change');
                            //     },200)
                            //     setTimeout(function(){
                            //         $('#id_kota_pengirim').val('').trigger('change');
                            //         $('#id_kecamatan_pengirim').val('').trigger('change');
                            //         $('#id_desa_pengirim').val('').trigger('change');
                            //         $('#id_kode_pos_pengirim').val('').trigger('change');
                            //     },400);
                            // }

                            // try {
                            //     $_kota = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kota : 0;
                            //     if($_kota){
                            //         setTimeout(function(){
                            //             $('#id_kota_pengirim').val($_kota).trigger('change');
                            //         },450);
                            //     }
                            //     setTimeout(function(){
                            //         $('#id_kecamatan_pengirim').val('').trigger('change');
                            //         $('#id_desa_pengirim').val('').trigger('change');
                            //         $('#id_kode_pos_pengirim').val('').trigger('change');
                            //     },650)
                            // } catch(error){}

                            // try {
                            //     $_kecamatan = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kecamatan : 0;
                            //     if($_kecamatan){
                            //         setTimeout(function(){
                            //             $('#id_kecamatan_pengirim').val($_kecamatan).trigger('change');
                            //         },700);
                            //     }
                            //     setTimeout(function(){
                            //         $('#id_desa_pengirim').val('').trigger('change');
                            //         $('#id_kode_pos_pengirim').val('').trigger('change');
                            //     },900)
                            // } catch(error){}

                            // try {
                            //     $_desa = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.desa : 0;
                            //     if($_desa){
                            //         setTimeout(function(){
                            //             $('#id_desa_pengirim').val($_desa).trigger('change');
                            //         },950);
                            //     }
                            //     setTimeout(function(){
                            //         $('#id_kode_pos_pengirim').val('').trigger('change');
                            //     },1150)
                            // } catch(error){}

                            // try {
                            //     $_kodepos = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kode_pos : 0;
                            //     if($_kodepos){
                            //         setTimeout(function(){
                            //             $('#id_kode_pos_pengirim').val($_kodepos).trigger('change');
                            //         },1200);
                            //     }
                            // } catch(error){}
                            // 
                            $('#id_provinsi_pengirim').val(response.data.detail_pelanggan.provinsi_id).trigger('change');
                            try {
                                document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = response.data.detail_pelanggan.provinsi__nama_provinsi;
                                // document.getElementById("id_provinsi_pengirim").innerHTML = '<option selected>' + response.data.detail_pelanggan.provinsi__nama_provinsi + '</option>';
                                // $("#id_provinsi_pengirim").val(response.data.detail_pelanggan.provinsi_id);
                            } catch(error){}
                            setTimeout(function(){
                                show_kota_list(response.data.detail_pelanggan.provinsi_id, 'pengirim', response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kota__nama_kota);
                                show_kecamatan_list(response.data.detail_pelanggan.kota_id, 'pengirim', response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.kecamatan__nama_kecamatan);
                                show_desa_list(response.data.detail_pelanggan.kecamatan_id, 'pengirim', response.data.detail_pelanggan.desa_id, response.data.detail_pelanggan.desa__nama_desa);
                                show_kode_pos_list(response.data.detail_pelanggan.provinsi_id, response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.desa_id, 'pengirim', response.data.detail_pelanggan.kode_pos_id, response.data.detail_pelanggan.kode_pos__kode_pos);
                            }, 800)
                        } catch(error){}
                    }
                },
                error : function(xhr){}
            });
        } catch(error){}

        $('#modal_order').modal('show');
    });

    // ================================================= CREATE DATA ACTION =====================================
    $("#createButton").click(function(e) {

        e.preventDefault();
        if($('#id_berat').val() == '0' || $('#id_berat').val() == 0 || $('#id_berat').val() == null){
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            });
    
            Toast.fire({
                icon: 'warning',
                title: 'Berat tidak boleh kosong'
            });
            return;
        }

        var serializeData = $("#createOrderForm")[0];
        serializeData = new FormData(serializeData);

        $.ajax({
            url: $("#createOrderForm").data('url'),
            data: serializeData,
            type: 'post',
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#modal_order').modal('hide');
                setTimeout(function() {
                    table.ajax.reload();
                    tampilkan_pesan(response.msg, response.type);
                }, 1000);
                // setTimeout(function(){
                //     location.reload()
                // },1300)
            },
            error: function(xhr, status, error) {
                // $('#modal_order').modal('hide');
                setTimeout(function() {
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                // $("#createOrderForm")[0].reset();
            },
        });
    });

    //================================================= EDIT DATA (SHOW FORM) =================================
    $('body').on('click', '.editOrder', function(e) {
        e.preventDefault();
        var id_order = $(this).data("id");
        $("#createOrderForm")[0].reset();
        // document.getElementsByClassName('nav-link')[0].click();
        // ambil_detail_data($("#createOrderForm").data('url') + id_order + '/detail/');

        $.ajax({
            url: id_order + '/detail/',
            type: 'get',
            success: function(response) {
                // console.log(response);
                document.getElementById('custom-tabs-one-pengirim-tab').click();
                // show_provinsi_list();
                show_kota_list(response.data.id_provinsi_pengirim, 'pengirim', response.data.id_kota_pengirim, response.data.kota_pengirim);
                show_kota_list(response.data.id_provinsi_penerima, 'penerima', response.data.id_kota_penerima, response.data.kota_penerima);
                show_kecamatan_list(response.data.id_kota_pengirim, 'pengirim', response.data.id_kecamatan_pengirim, response.data.kecamatan_pengirim);
                show_kecamatan_list(response.data.id_kota_penerima, 'penerima', response.data.id_kecamatan_penerima, response.data.kecamatan_penerima);
                show_desa_list(response.data.id_kecamatan_pengirim, 'pengirim', response.data.id_desa_pengirim, response.data.desa_pengirim);
                show_desa_list(response.data.id_kecamatan_penerima, 'penerima', response.data.id_desa_penerima, response.data.desa_penerima);
                show_kode_pos_list(response.data.id_provinsi_pengirim, response.data.id_kota_pengirim, response.data.id_kecamatan_pengirim, response.data.id_desa_pengirim, 'pengirim', response.data.id_kode_pos_pengirim, response.data.kode_pos_pengirim);
                show_kode_pos_list(response.data.id_provinsi_penerima, response.data.id_kota_penerima, response.data.id_kecamatan_penerima, response.data.id_desa_penerima, 'penerima', response.data.id_kode_pos_penerima, response.data.kode_pos_penerima);

                document.getElementById("id_kode_pos_pengirim").value = response.data.id_kode_pos_pengirim;
                document.getElementById("select2-id_kode_pos_pengirim-container").innerHTML = response.data.kode_pos_pengirim;

                document.getElementById("id_kode_pos_penerima").value = response.data.id_kode_pos_penerima;
                document.getElementById("select2-id_kode_pos_penerima-container").innerHTML = response.data.kode_pos_penerima;


                document.getElementById("id_edit").value = response.data.id;
                document.getElementById("id_provinsi_pengirim").value = response.data.id_provinsi_pengirim;
                document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = response.data.provinsi_pengirim;

                document.getElementById("id_nama_penerima").value = response.data.nama_penerima;
                document.getElementById("id_no_tlp_penerima").value = response.data.no_tlp_penerima;
                document.getElementById("id_email_penerima").value = response.data.email_penerima;
                document.getElementById("id_alamat_penerima").value = response.data.alamat_penerima;
                try {
                    document.getElementById("alamat_customer___").value = response.data.alamat_pengirim_alt;
                } catch(error){}

                document.getElementById("id_provinsi_penerima").value = response.data.id_provinsi_penerima;
                document.getElementById("select2-id_provinsi_penerima-container").innerHTML = response.data.provinsi_penerima;

                document.getElementById("id_outlet_pengiriman").value = response.data.id_outlet_order;
                document.getElementById("id_outlet_penerimaan").value = response.data.id_outlet_penerimaan;
                document.getElementById("id_gudang_pengiriman").value = response.rute.gudang_1.id;
                document.getElementById("id_gudang_penerimaan").value = response.rute.gudang_2.id;
                document.getElementById("id_order").value = response.data.id_order;

                // document.getElementById("id_jenis_barang").value = response.data.jenis_barang_id;
                // document.getElementById("select2-id_jenis_barang-container").innerHTML = response.data.jenis_barang;
                var option_jenisBarang = new Option(response.data.jenis_barang, response.data.jenis_barang_id, true, true);
                $("#id_jenis_barang").append(option_jenisBarang).trigger('change');

                var option_Layanan = new Option(response.data.layanan, response.data.id_layanan, true, true);
                $("#id_jenis_pengiriman").append(option_Layanan).trigger('change');

                // document.getElementById("inputSatuan").value = response.data.id_satuan;
                // document.getElementById("select2-inputSatuan-container").innerHTML = response.data.satuan;

                var option_Satuan = new Option(response.data.satuan, response.data.id_satuan, true, true);
                $("#inputSatuan").append(option_Satuan).trigger('change');

                document.getElementById("id_detail_barang").value = response.data.detail_barang;

                document.getElementById("id_id_pengemasan").value = response.data.id_pengemasan;
                document.getElementById("select2-id_id_pengemasan-container").innerHTML = response.data.pengemasan;

                document.getElementById("id_jenis_pengiriman").value = response.data.id_layanan;
                document.getElementById("select2-id_jenis_pengiriman-container").innerHTML = response.data.layanan;
                document.getElementById("id_berat").value = parseFloat(response.data.berat).toFixed(1).slice(-2) == ".0" ? parseFloat(response.data.berat).toFixed(0) : parseFloat(response.data.berat).toFixed(1);
                document.getElementById("inputJumlah").value = response.data.jumlah_barang;

                document.getElementById("id_tarif_berat").value = response.data.tarif_berat;
                document.getElementById("id_tarif_kilometer").value = response.data.tarif_kilometer;
                document.getElementById("id_tarif_gudang").value = response.data.tarif_gudang;
                document.getElementById("id_tarif_layanan").value = response.data.tarif_layanan;
                document.getElementById("id_tarif_pengemasan").value = response.data.tarif_pengemasan;
                document.getElementById("id_total_tarif").value = response.data.total_tarif;
                document.getElementById("id_extra_tarif_penerima").value = response.data.extra_tarif_penerima;
                document.getElementById("id_extra_tarif_pengirim").value = response.data.extra_tarif_pengirim;


                viewRupiah('id_tarif_berat', 'id_tarif_berat_tampil');
                viewRupiah('id_tarif_kilometer', 'id_tarif_kilometer_tampil');
                viewRupiah('id_tarif_gudang', 'id_tarif_gudang_tampil');
                viewRupiah('id_tarif_layanan', 'id_tarif_layanan_tampil');
                viewRupiah('id_tarif_pengemasan', 'id_tarif_pengemasan_tampil');
                viewRupiah('id_total_tarif', 'id_total_tarif_tampil');
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');

                var html_rute = '<h4>Rute Pengiriman:</h4><div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div></div>';

                document.getElementById("rute_gudang").innerHTML = html_rute;

                document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '<b><h3>Keterangan:</h3></b>' + response.data.keterangan_extra_tarif;


                document.getElementById("title_modal").innerHTML = "Edit Data Order";
                $("#createOrderForm :input").prop("disabled", false);
                document.getElementById("group_order_button").style.display = "none";
                document.getElementById("group_update_button").style.display = "block";
                document.getElementById("group_detail_button").style.display = "none";

                $("#nama_customer___").prop("disabled", true);
                $("#no_hp_customer___").prop("disabled", true);
                $("#email_customer___").prop("disabled", true);
                // $("#alamat_customer___").prop("disabled", true);

                $('#modal_order').modal('show');
            },
            error: function(xhr, status, error) {
                try {
                    $('.modal').modal('hide');
                } catch (error) {
                    // console.log(error);
                }
                setTimeout(function() {
                    var error_response = xhr.responseJSON || { 'msg': 'Terjadi Kesalahan yang tidak diketahui', 'type': 'error' };
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                $("#createOrderForm")[0].reset();
            }
        })

    });

    async function ambil_detail_data(url) {
        let resp_detail = await fetch(url);
        let response = await resp_detail.json();
        // show_provinsi_list();
        show_kota_list(response.data.id_provinsi_pengirim, 'pengirim', response.data.id_kota_pengirim, response.data.kota_pengirim);
        show_kota_list(response.data.id_provinsi_penerima, 'penerima', response.data.id_kota_penerima, response.data.kota_penerima);
        show_kecamatan_list(response.data.id_kota_pengirim, 'pengirim', response.data.id_kecamatan_pengirim, response.data.kecamatan_pengirim);
        show_kecamatan_list(response.data.id_kota_penerima, 'penerima', response.data.id_kecamatan_penerima, response.data.kecamatan_penerima);
        show_desa_list(response.data.id_kecamatan_pengirim, 'pengirim', response.data.id_desa_pengirim, response.data.desa_pengirim);
        show_desa_list(response.data.id_kecamatan_penerima, 'penerima', response.data.id_desa_penerima, response.data.desa_penerima);
        show_kode_pos_list(response.data.id_provinsi_pengirim, response.data.id_kota_pengirim, response.data.id_kecamatan_pengirim, response.data.id_desa_pengirim, 'pengirim', response.data.id_kode_pos_pengirim, response.data.kode_pos_pengirim);
        show_kode_pos_list(response.data.id_provinsi_penerima, response.data.id_kota_penerima, response.data.id_kecamatan_penerima, response.data.id_desa_penerima, 'penerima', response.data.id_kode_pos_penerima, response.data.kode_pos_penerima);
        document.getElementById("id_kode_pos_pengirim").value = response.data.id_kode_pos_pengirim;
        document.getElementById("select2-id_kode_pos_pengirim-container").innerHTML = response.data.kode_pos_pengirim;

        document.getElementById("id_kode_pos_penerima").value = response.data.id_kode_pos_penerima;
        document.getElementById("select2-id_kode_pos_penerima-container").innerHTML = response.data.kode_pos_penerima;

        document.getElementById("id_edit").value = response.data.id;
        document.getElementById("id_provinsi_pengirim").value = response.data.id_provinsi_pengirim;
        // document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = response.data.provinsi_pengirim;
        document.getElementById("id_provinsi_penerima").value = response.data.id_provinsi_penerima;
        // document.getElementById("select2-id_provinsi_penerima-container").innerHTML = response.data.provinsi_penerima;


        document.getElementById("id_nama_penerima").value = response.data.nama_penerima;
        document.getElementById("id_no_tlp_penerima").value = response.data.no_tlp_penerima;
        document.getElementById("id_email_penerima").value = response.data.email_penerima;
        document.getElementById("id_alamat_penerima").value = response.data.alamat_penerima;

        document.getElementById("id_outlet_pengiriman").value = response.data.id_outlet_order;
        document.getElementById("id_outlet_penerimaan").value = response.data.id_outlet_penerimaan;
        document.getElementById("id_gudang_pengiriman").value = response.rute.gudang_1.id;
        document.getElementById("id_gudang_penerimaan").value = response.rute.gudang_2.id;
        document.getElementById("id_order").value = response.data.id_order;


        document.getElementById("id_jenis_barang").value = response.data.jenis_barang_id.toString();
        // document.getElementById("select2-id_jenis_barang-container").innerHTML = response.data.jenis_barang;
        
        document.getElementById("id_detail_barang").value = response.data.detail_barang;

        document.getElementById("id_id_pengemasan").value = response.data.id_pengemasan;
        if (response.data.id_pengemasan == '') {
            document.getElementById("select2-id_id_pengemasan-container").innerHTML = 'Tidak Memerlukan Pengemasan Lagi';
        } else {
            document.getElementById("select2-id_id_pengemasan-container").innerHTML = response.data.pengemasan;
        }


        document.getElementById("id_jenis_pengiriman").value = response.data.id_layanan;
        document.getElementById("select2-id_jenis_pengiriman-container").innerHTML = response.data.layanan;
        document.getElementById("id_berat").value = parseFloat(response.data.berat).toFixed(1).slice(-2) == ".0" ? parseFloat(response.data.berat).toFixed(0) : parseFloat(response.data.berat).toFixed(1);
        document.getElementById("inputJumlah").value = response.data.jumlah_barang

        document.getElementById("id_tarif_berat").value = response.data.tarif_berat;
        document.getElementById("id_tarif_kilometer").value = response.data.tarif_kilometer;
        document.getElementById("id_tarif_gudang").value = response.data.tarif_gudang;
        document.getElementById("id_tarif_layanan").value = response.data.tarif_layanan;
        document.getElementById("id_tarif_pengemasan").value = response.data.tarif_pengemasan;
        document.getElementById("id_total_tarif").value = response.data.total_tarif;
        document.getElementById("id_extra_tarif_penerima").value = response.data.extra_tarif_penerima;
        document.getElementById("id_extra_tarif_pengirim").value = response.data.extra_tarif_pengirim;


        viewRupiah('id_tarif_berat', 'id_tarif_berat_tampil');
        viewRupiah('id_tarif_kilometer', 'id_tarif_kilometer_tampil');
        viewRupiah('id_tarif_gudang', 'id_tarif_gudang_tampil');
        viewRupiah('id_tarif_layanan', 'id_tarif_layanan_tampil');
        viewRupiah('id_tarif_pengemasan', 'id_tarif_pengemasan_tampil');
        viewRupiah('id_total_tarif', 'id_total_tarif_tampil');
        viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
        viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');

        var html_rute = '<h4>Rute Pengiriman:</h4><div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div></div>';

        html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div></div>';

        html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div></div>';

        html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div></div>';

        document.getElementById("rute_gudang").innerHTML = html_rute;

        document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '<b><h3>Keterangan:</h3></b>' + response.data.keterangan_extra_tarif;

        document.getElementById("title_modal").innerHTML = "Edit Data Order";
        $("#createOrderForm :input").prop("disabled", false);

        document.getElementById("group_order_button").style.display = "none";
        document.getElementById("group_update_button").style.display = "block";
        document.getElementById("group_detail_button").style.display = "none";
        $('#modal_order').modal('show');
        show_kode_pos_list(response.data.id_provinsi_pengirim, response.data.id_kota_pengirim, response.data.id_kecamatan_pengirim, response.data.id_desa_pengirim, 'pengirim', response.data.id_kode_pos_pengirim, response.data.kode_pos_pengirim);
        show_kode_pos_list(response.data.id_provinsi_penerima, response.data.id_kota_penerima, response.data.id_kecamatan_penerima, response.data.id_desa_penerima, 'penerima', response.data.id_kode_pos_penerima, response.data.kode_pos_penerima);

        document.getElementById("id_kode_pos_pengirim").value = response.data.id_kode_pos_pengirim;
        document.getElementById("select2-id_kode_pos_pengirim-container").innerHTML = response.data.kode_pos_pengirim;

        document.getElementById("id_kode_pos_penerima").value = response.data.id_kode_pos_penerima;
        document.getElementById("select2-id_kode_pos_penerima-container").innerHTML = response.data.kode_pos_penerima;

        document.getElementById("id_provinsi_pengirim").value = response.data.id_provinsi_pengirim;
        document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = response.data.provinsi_pengirim;

        document.getElementById("id_provinsi_penerima").value = response.data.id_provinsi_penerima;
        document.getElementById("select2-id_provinsi_penerima-container").innerHTML = response.data.provinsi_penerima;
        $("#nama_customer___").prop("disabled", true);
        $("#no_hp_customer___").prop("disabled", true);
        $("#email_customer___").prop("disabled", true);
        $("#alamat_customer___").prop("disabled", true);
        return response;
    }

    // ================================================ EDIT DATA ACTION ============================
    $("#updateButton").click(function(e) {

        e.preventDefault();
        var serializeData = $("#createOrderForm")[0];
        serializeData = new FormData(serializeData);

        $.ajax({
            url: $("#createOrderForm").data('url_update_order'),
            data: serializeData,
            type: 'post',
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#modal_order').modal('hide');
                setTimeout(function() {
                    table.ajax.reload();
                    tampilkan_pesan(response.msg, response.type);
                }, 1000);
                $("#createOrderForm")[0].reset();
            },
            error: function(xhr, status, error) {
                // try {
                //     $('.modal').modal('hide');
                // } catch (error) {
                //     // console.log(error);
                // }
                setTimeout(function() {
                    var error_response = xhr.responseJSON || { 'msg': 'Terjadi Kesalahan yang tidak diketahui', 'type': 'error' };
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                // $("#createOrderForm")[0].reset();
            }
        });
    });
    // ================================================ END EDIT DATA ACTION ========================

    //================================================= DETAIL DATA =================================
    $('body').on('click', '.detailOrder', function(e) {
        e.preventDefault();
        var id_order = $(this).data("id");
        $("#createOrderForm")[0].reset();
        // show_provinsi_list();
        $.ajax({
            url: id_order + '/detail/',
            type: 'get',
            success: function(response) {
                document.getElementById('custom-tabs-one-pengirim-tab').click();
                show_kota_list(response.data.id_provinsi_pengirim, 'pengirim', response.data.id_kota_pengirim, response.data.kota_pengirim);
                show_kota_list(response.data.id_provinsi_penerima, 'penerima', response.data.id_kota_penerima, response.data.kota_penerima);
                show_kecamatan_list(response.data.id_kota_pengirim, 'pengirim', response.data.id_kecamatan_pengirim, response.data.kecamatan_pengirim);
                show_kecamatan_list(response.data.id_kota_penerima, 'penerima', response.data.id_kecamatan_penerima, response.data.kecamatan_penerima);
                show_desa_list(response.data.id_kecamatan_pengirim, 'pengirim', response.data.id_desa_pengirim, response.data.desa_pengirim);
                show_desa_list(response.data.id_kecamatan_penerima, 'penerima', response.data.id_desa_penerima, response.data.desa_penerima);
                show_kode_pos_list(response.data.id_provinsi_pengirim, response.data.id_kota_pengirim, response.data.id_kecamatan_pengirim, response.data.id_desa_pengirim, 'pengirim', response.data.id_kode_pos_pengirim, response.data.kode_pos_pengirim);
                show_kode_pos_list(response.data.id_provinsi_penerima, response.data.id_kota_penerima, response.data.id_kecamatan_penerima, response.data.id_desa_penerima, 'penerima', response.data.id_kode_pos_penerima, response.data.kode_pos_penerima);

                document.getElementById("id_kode_pos_pengirim").value = response.data.id_kode_pos_pengirim;
                document.getElementById("select2-id_kode_pos_pengirim-container").innerHTML = response.data.kode_pos_pengirim;

                document.getElementById("id_kode_pos_penerima").value = response.data.id_kode_pos_penerima;
                document.getElementById("select2-id_kode_pos_penerima-container").innerHTML = response.data.kode_pos_penerima;


                document.getElementById("id_edit").value = response.data.id;
                document.getElementById("id_provinsi_pengirim").value = response.data.id_provinsi_pengirim;
                document.getElementById("select2-id_provinsi_pengirim-container").innerHTML = response.data.provinsi_pengirim;

                document.getElementById("id_nama_penerima").value = response.data.nama_penerima;
                document.getElementById("id_no_tlp_penerima").value = response.data.no_tlp_penerima;
                document.getElementById("id_email_penerima").value = response.data.email_penerima;
                document.getElementById("id_alamat_penerima").value = response.data.alamat_penerima;
                try {
                    document.getElementById("alamat_customer___").value = response.data.alamat_pengirim_alt;
                } catch(error){}

                document.getElementById("id_provinsi_penerima").value = response.data.id_provinsi_penerima;
                document.getElementById("select2-id_provinsi_penerima-container").innerHTML = response.data.provinsi_penerima;

                document.getElementById("id_outlet_pengiriman").value = response.data.id_outlet_order;
                document.getElementById("id_outlet_penerimaan").value = response.data.id_outlet_penerimaan;
                document.getElementById("id_gudang_pengiriman").value = response.rute.gudang_1.id;
                document.getElementById("id_gudang_penerimaan").value = response.rute.gudang_2.id;
                document.getElementById("id_order").value = response.data.id_order;

                document.getElementById("id_jenis_barang").value = response.data.jenis_barang_id;
                document.getElementById("select2-id_jenis_barang-container").innerHTML = response.data.jenis_barang;

                document.getElementById("inputSatuan").value = response.data.id_satuan;
                document.getElementById("select2-inputSatuan-container").innerHTML = response.data.satuan;

                document.getElementById("id_detail_barang").value = response.data.detail_barang;

                document.getElementById("id_id_pengemasan").value = response.data.id_pengemasan;
                document.getElementById("select2-id_id_pengemasan-container").innerHTML = response.data.pengemasan;

                document.getElementById("id_jenis_pengiriman").value = response.data.id_layanan;
                document.getElementById("select2-id_jenis_pengiriman-container").innerHTML = response.data.layanan;
                document.getElementById("id_berat").value = parseFloat(response.data.berat).toFixed(1).slice(-2) == ".0" ? parseFloat(response.data.berat).toFixed(0) : parseFloat(response.data.berat).toFixed(1);
                document.getElementById("inputJumlah").value = response.data.jumlah_barang;

                document.getElementById("id_tarif_berat").value = response.data.tarif_berat;
                document.getElementById("id_tarif_kilometer").value = response.data.tarif_kilometer;
                document.getElementById("id_tarif_gudang").value = response.data.tarif_gudang;
                document.getElementById("id_tarif_layanan").value = response.data.tarif_layanan;
                document.getElementById("id_tarif_pengemasan").value = response.data.tarif_pengemasan;
                document.getElementById("id_total_tarif").value = response.data.total_tarif;
                document.getElementById("id_extra_tarif_penerima").value = response.data.extra_tarif_penerima;
                document.getElementById("id_extra_tarif_pengirim").value = response.data.extra_tarif_pengirim;


                viewRupiah('id_tarif_berat', 'id_tarif_berat_tampil');
                viewRupiah('id_tarif_kilometer', 'id_tarif_kilometer_tampil');
                viewRupiah('id_tarif_gudang', 'id_tarif_gudang_tampil');
                viewRupiah('id_tarif_layanan', 'id_tarif_layanan_tampil');
                viewRupiah('id_tarif_pengemasan', 'id_tarif_pengemasan_tampil');
                viewRupiah('id_total_tarif', 'id_total_tarif_tampil');
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');

                var html_rute = '<h4>Rute Pengiriman:</h4><div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div></div>';

                html_rute = html_rute + '<div class="row"><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div></div>';

                document.getElementById("rute_gudang").innerHTML = html_rute;

                document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '<b><h3>Keterangan:</h3></b>' + response.data.keterangan_extra_tarif;


                document.getElementById("title_modal").innerHTML = "Detail Data Order";
                $("#createOrderForm :input").prop("disabled", true);
                document.getElementById("group_order_button").style.display = "none";
                document.getElementById("group_update_button").style.display = "none";
                document.getElementById("group_detail_button").style.display = "block";
                $('#modal_order').modal('show');
            },
            error: function(xhr, status, error) {
                try {
                    $('.modal').modal('hide');
                } catch (error) {
                    // console.log(error);
                }
                setTimeout(function() {
                    var error_response = xhr.responseJSON || { 'msg': 'Terjadi Kesalahan yang tidak diketahui', 'type': 'error' };
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                $("#createOrderForm")[0].reset();
            }
        })
    });

    // =========================================== BAGIAN Cancel Order View Prompt ============================
    $('body').on('click', '.cancelOrder', function(e) {
        e.preventDefault();
        var id = $(this).data("id");
        var id_order = $(this).data("nama");

        document.getElementById("id_cancel_order").value = id;
        document.getElementById("id_order_cancel").innerHTML = id_order;
        document.getElementById("id_keterangan_cancel").value = '';
        $('#modal_cancel').modal('show');
    });
    // =========================================== Bagian Cancel Order Action =================================
    $("#submit_cancel_order").click(function(e) {

        e.preventDefault();

        var id = document.getElementById("id_cancel_order").value;
        var keterangan = document.getElementById("id_keterangan_cancel").value;

        $.ajax({
            url: $("#cancelOrderForm").data('url') + 'cancel/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                id: id,
                keterangan: keterangan
            },

            success: function(response) {
                $('#modal_cancel').modal('hide');
                setTimeout(function() {
                    table.ajax.reload();
                    table_history.ajax.reload();
                    tampilkan_pesan(response.msg, response.type);
                }, 1000);
                $("#cancelOrderForm")[0].reset();
            },
            error: function(xhr, status, error) {
                try {
                    $('.modal').modal('hide');
                } catch (error) {
                    // console.log(error);
                }
                setTimeout(function() {
                    var error_response = xhr.responseJSON || { 'msg': 'Terjadi Kesalahan yang tidak diketahui', 'type': 'error' };
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                $("#cancelOrderForm")[0].reset();
            },
        });
    });

    // ========================================= Bagian Delete ========================================================
    $('body').on('click', '.deleteOrder', function() {
        var id_delete = $(this).data("id");
        var id_order = $(this).data("nama");
        Swal.fire({
            title: 'Anda yakin?',
            text: "Yakin menghapus Orderan dengan ID: " + id_order + "!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!',
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: $("#cancelOrderForm").data('url') + 'delete/',
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        id: id_delete
                    },
                    type: 'post',
                    dataType: 'json',
                    success: function(response) {
                        tampilkan_pesan(response.msg, response.type);
                        table.ajax.reload();
                    },
                    error: function(xhr, status, error) {
                        try {
                            $('.modal').modal('hide');
                        } catch (error) {
                            // console.log(error);
                        }
                        setTimeout(function() {
                            var error_response = xhr.responseJSON || { 'msg': 'Terjadi Kesalahan yang tidak diketahui', 'type': 'error' };
                            tampilkan_pesan(error_response.msg, error_response.type);
                        }, 1000)
                    }
                });

            }
        })
    });


    // ========================================= GET COORDINATE MODULE =================================================
    async function get_loc_degree(alamat_pengirim, alamat_penerima) {
        // console.log("ASAL", alamat_pengirim, "TUJUAN", alamat_penerima)
        try {
            var url_api_geo = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=";
            var extra_cash_pengirim = 'Tidak Kena';
            var extra_cash_penerima = 'Tidak Kena';

            var t_arr = alamat_pengirim.split(',');
            var r_arr = alamat_penerima.split(',');

            var loc_pengirim;
            var loc_penerima;

            //fetch all gudang
            const response_gudang = await fetch($("#createOrderForm").data('url_gudang'));
            const data_gudang = await response_gudang.json();
            var gudangs = data_gudang.data;


            //Pencarian Titik Lokasi Untuk Pengirim
            // const T_response_1 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[0].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
            const T_response_1 = await fetch(url_api_geo + alamat_pengirim + "&size=1&country=IDN");
            const data_pengirim = await T_response_1.json();
            if (data_pengirim.features.length <= 0) {
                const T_response_2 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[2].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
                const data_pengirim = await T_response_2.json();
                if (data_pengirim.features.length <= 0) {
                    const T_response_3 = await fetch(url_api_geo + t_arr[2].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
                    const data_pengirim = await T_response_3.json();
                    if (data_pengirim.features.length <= 0) {
                        const T_response_4 = await fetch(url_api_geo + t_arr[3].trim() + "&size=1&country=IDN");
                        const data_pengirim = await T_response_4.json();
                        if (data_pengirim.features.length <= 0) {

                        } else {
                            loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                            extra_cash_pengirim = 'kabupaten';
                        }
                    } else {
                        loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                        extra_cash_pengirim = 'kota';
                    }
                } else {
                    loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                    extra_cash_pengirim = 'kecamatan';
                }

            } else {
                loc_pengirim = data_pengirim.features[0].geometry.coordinates;
            }


            //Pencarian Titik Lokasi Untuk Penerima
            // const R_response_1 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[0].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
            const R_response_1 = await fetch(url_api_geo + alamat_penerima + "&size=1&country=IDN");
            const data_penerima = await R_response_1.json();
            if (data_penerima.features.length <= 0) {
                const R_response_2 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[2].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
                const data_penerima = await R_response_2.json();
                if (data_penerima.features.length <= 0) {
                    const R_response_3 = await fetch(url_api_geo + r_arr[2].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
                    const data_penerima = await R_response_3.json();
                    if (data_penerima.features.length <= 0) {
                        const R_response_4 = await fetch(url_api_geo + r_arr[3].trim() + "&size=1&country=IDN");
                        const data_penerima = await R_response_4.json();
                        if (data_penerima.features.length <= 0) {

                        } else {
                            loc_penerima = data_penerima.features[0].geometry.coordinates;
                            extra_cash_penerima = 'kabupaten';
                        }
                    } else {
                        loc_penerima = data_penerima.features[0].geometry.coordinates;
                        extra_cash_penerima = 'kota';
                    }
                } else {
                    loc_penerima = data_penerima.features[0].geometry.coordinates;
                    extra_cash_penerima = 'kecamatan';
                }

            } else {
                loc_penerima = data_penerima.features[0].geometry.coordinates;
            }
            var html_keterangan = '';
            var html_keterangan_2 = '';

            // console.log("LOC PENGIRIM", loc_pengirim, "LOC PENERIMA", loc_penerima);
            // console.log("EXTRA CASH PENGIRIM", extra_cash_pengirim, 'EXTRA CASH PENERIMA', extra_cash_penerima);

            if (extra_cash_penerima != 'Tidak Kena') {
                const response_extra_cash_penerima = await fetch($("#createOrderForm").data('url_extra_cash') + '?wilayah=' + extra_cash_penerima);
                const data_ec_penerima = await response_extra_cash_penerima.json();
                document.getElementById("id_extra_tarif_penerima").value = data_ec_penerima.harga;
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
                html_keterangan += 'Alamat Penerima Paket Kena Extra Cash (' + data_ec_penerima.wilayah + ')';
            } else {
                html_keterangan += 'Alamat Penerima Tidak Kena Extra Cash';
                document.getElementById("id_extra_tarif_penerima").value = '0';
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
            }

            // Perlu karena paket dijemput kurir
            if (extra_cash_pengirim != 'Tidak Kena') {
                const response_extra_cash_pengirim = await fetch($("#createOrderForm").data('url_extra_cash') + '?wilayah=' + extra_cash_pengirim);
                const data_ec_pengirim = await response_extra_cash_pengirim.json();
                document.getElementById("id_extra_tarif_pengirim").value = data_ec_pengirim.harga;
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');
                html_keterangan_2 += '& Alamat Pengirim Paket Kena Extra Cash (' + data_ec_pengirim.wilayah + ')';
            } else {
                html_keterangan_2 += ' & Alamat Pengirim Tidak Kena Extra Cash';
                document.getElementById("id_extra_tarif_pengirim").value = '0';
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');
            }

            document.getElementById("id_keterangan_extra_tarif").value = html_keterangan + html_keterangan_2;
            document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '<b><h3>Keterangan:</h3></b>' + html_keterangan + '<br>' + html_keterangan_2;

            clear_rute_gudang();
            // console.log('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima);
            tampilkan_pesan('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima, 'info');
            // outlet_dan_gudang_yang_dilalui(gudangs, loc_penerima, loc_pengirim);

            outlet_dan_gudang_yang_dilalui_2(gudangs, loc_penerima, loc_pengirim, t_arr[0], r_arr[0]);
        } catch (e) {
            tampilkan_pesan(e.message + ", please check connection and refresh", 'error');
            return;
        } 
    }

    function get_loc_degree_old(alamat_pengirim, alamat_penerima) {
        var data_penerima;
        var data_pengirim;
        var data_gudang;

        var url_geocode_1 = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=" + alamat_pengirim + "&size=1&country=IDN";
        var url_geocode_2 = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=" + alamat_penerima + "&size=1&country=IDN";

        $.ajax({
                type: "GET",
                url: $("#createOrderForm").data('url_gudang'),
                success: function(response) {
                    data_gudang = response.data;
                    // console.log("Sukses Ambil data Gudang");
                }

            })
            .done(function() {
                $.ajax({
                        type: "GET",
                        url: url_geocode_1,
                        success: function(data) {
                            // console.log('get_loc_degree_HASIL', data);
                            if (data.features.length) {
                                data_pengirim = data.features[0].geometry.coordinates;
                                // console.log("Sukses Ambil data pengirim");
                            } else {
                                tampilkan_pesan('Rute Pengiriman tidak ditemukan', 'error');
                                clear_rute_gudang();
                                return;
                            }
                        }
                    })
                    .done(function() {
                        $.ajax({
                                type: "GET",
                                url: url_geocode_2,
                                success: function(data) {
                                    if (data.features.length) {
                                        data_penerima = data.features[0].geometry.coordinates;
                                    } else {
                                        tampilkan_pesan('Rute Penerima tidak ditemukan', 'error');
                                        clear_rute_gudang();
                                        return;
                                    }
                                }
                            })
                            .done(function() {
                                // Call Function for hitung tarif here
                                // console.log(data_penerima); //lon, lat
                                // console.log(data_pengirim); //lon, lat
                                // var center = getLatLngCenter(data_penerima[1],data_penerima[0], data_pengirim[1], data_pengirim[0]);
                                // console.log(data_gudang);
                                // // console.log(data_gudang[0].titik_lokasi); //"lat,lon"
                                outlet_dan_gudang_yang_dilalui(data_gudang, data_penerima, data_pengirim);

                            });
                    });
            });
    }
    // ========================================= END GET COORDINATE MODULE =============================================

    // ========================================= MODUL HITUNG JARAK ====================================================

    function hitung_jarak(lat1, lon1, lat2, lon2) {
        var R = 6371; // Radius of the earth in km
        var dLat = deg2rad(lat2 - lat1); // deg2rad below
        var dLon = deg2rad(lon2 - lon1);
        var a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = R * c; // Distance in km
        return d * 1000; //return meter
    }

    function deg2rad(deg) {
        return deg * (Math.PI / 180);
    }

    function indexOfSmallest(a) {
        return a.indexOf(Math.min.apply(Math, a));
    }

    function string_to_arr(text) {
        var data = text.split(",");
        return data;
    }

    function rad2degr(rad) {
        return rad * 180 / Math.PI;
    }

    function degr2rad(degr) {
        return degr * Math.PI / 180;
    }

    function getLatLngCenter(lat1, lon1, lat2, lon2) {
        var sumX = 0;
        var sumY = 0;
        var sumZ = 0;
        var lat = 0;
        var lng = 0;

        for (var i = 0; i < 2; i++) {
            if (i == 0) {
                lat = degr2rad(lat1);
                lng = degr2rad(lon1);
            } else {
                lat = degr2rad(lat2);
                lng = degr2rad(lon2);
            }

            // sum of cartesian coordinates
            sumX += Math.cos(lat) * Math.cos(lng);
            sumY += Math.cos(lat) * Math.sin(lng);
            sumZ += Math.sin(lat);
        }

        var avgX = sumX / 2;
        var avgY = sumY / 2;
        var avgZ = sumZ / 2;

        // convert average x, y, z coordinate to latitude and longtitude
        var lng = Math.atan2(avgY, avgX);
        var hyp = Math.sqrt(avgX * avgX + avgY * avgY);
        var lat = Math.atan2(avgZ, hyp);

        return ([rad2degr(lat), rad2degr(lng)]);
    }
    // ========================================= END MODUL HITUNG JARAK ================================================

    // ========================================= MODUL PERHITUNGAN TARIF GUDANG ========================================
    function total_tarif_gudang(id_gudang_1, id_gudang_2) {
        $.ajax({
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_tarif_gudang') + id_gudang_1 + '/' + id_gudang_2 + '/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                id_gudang_1: id_gudang_1,
                id_gudang_2: id_gudang_2
            },
            success: function(response) {
                if (response.data == '0') {
                    document.getElementById("id_tarif_gudang").value = '0';
                    // document.getElementById("tarifGudang").innerHTML = 'Rp. 0';
                } else {
                    document.getElementById("id_tarif_gudang").value = response.data.tarif;
                    viewRupiah('id_tarif_gudang', 'id_tarif_gudang_tampil');
                    // document.getElementById("tarifGudang").innerHTML = 'Rp. ' + response.data.tarif;
                }

            },
            error: function(xhr, status, error) {
                // console.log(xhr);
            }
        }).done(function() {
            hitung_total();
        });
    }

    // ========================================= END MODUL PERHITUNGAN TARIF GUDANG ====================================

    // ========================================= MODUL PERHITUNGAN TARIF KILOMETER =====================================
    function total_tarif_kilometer(kilometer) {
        $.ajax({
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createOrderForm").data('url_kilometer') + kilometer + '/harga/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    kilometer: kilometer
                },

                success: function(response) {
                    // // console.log(response.data);
                    document.getElementById("id_tarif_kilometer").value = response.harga;
                    viewRupiah('id_tarif_kilometer', 'id_tarif_kilometer_tampil');

                    // document.getElementById("tarifKilometer").innerHTML = 'Rp. ' + response.harga;
                }
            })
            .done(function() {
                hitung_total();
            });
    }
    // ========================================= END MODUL PERHITUNGAN TARIF KILOMETER =================================

    // ========================================= MODUL PERHITUNGAN TARIF berat ========================================
    id_berat.oninput = function() {
        var berat = $(this).val();
        setTimeout(function(){
            if (!berat) {
                berat = 0;
            }

            try {
                var beratCekOns = parseFloat("0" +parseFloat(berat).toFixed(1).slice(-2));
                // console.log("BERAT ONS", beratCekOns)
                if(beratCekOns >= 0.1)
                    berat = Math.floor(parseFloat(berat)) + 1;
                else 
                    berat = (parseInt(berat).toFixed(0))
            } catch(error){
                // console.log(error);
                berat = Math.round(parseFloat(berat));
            }

            setTimeout(function(){
                try{
                    $("#id_berat").prop('disabled', true);
                    // $("#id_berat").val(berat);
                } catch(error){}
            },0)

            setTimeout(function(){
                // console.log("BERAT NIH BRO", berat);
                $("#id_berat").prop('disabled', false);
                $.ajax({
                    type: "GET",
                    dataType: 'json',
                    contentType: "application/json",
                    url: $("#createOrderForm").data('url_berat') + berat + '/harga/',
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        berat: berat
                    },

                    success: function(response) {
                        // // console.log(response.data);
                        document.getElementById("id_tarif_berat").value = response.harga;
                        viewRupiah('id_tarif_berat', 'id_tarif_berat_tampil');
                        // document.getElementById("tarifberat").innerHTML = 'Rp. ' + response.harga;
                    }
                }).done(function() {
                    hitung_total();
                });
            },0)

        },200)

    };
    // ========================================= END MODUL PERHITUNGAN TARIF berat ====================================

    // ========================================= MODUL PERHITUNGAN TARIF LAYANAN =======================================
    $("#id_jenis_pengiriman").change(function() {
        var id_layanan = $(this).val();
        if (!id_layanan) {
            id_layanan = 0;
        }
        $.ajax({
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_layanan') + id_layanan + '/harga/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                id_layanan: id_layanan
            },

            success: function(response) {
                // // console.log(response.data);
                document.getElementById("id_tarif_layanan").value = response.harga;
                viewRupiah('id_tarif_layanan', 'id_tarif_layanan_tampil');
                // document.getElementById("tarifLayanan").innerHTML = 'Rp. ' + response.harga;
            }
        }).done(function() {
            hitung_total();
        });

    });
    // ========================================= END MODUL PERHITUNGAN TARIF LAYANAN ===================================

    // ========================================= MODUL PERHITUNGAN TARIF Pengemasan (Packing) =======================================

    $("#id_id_pengemasan").change(function() {
        var id_pengemasan = $(this).val();
        if (!id_pengemasan) {
            id_pengemasan = 0;
            harga_pengemasan = 0;
            document.getElementById("id_tarif_pengemasan").value = '';
            viewRupiah('id_tarif_pengemasan', 'id_tarif_pengemasan_tampil');
            hitung_total();
        }
        if (id_pengemasan != 0) {
            $.ajax({
                type: "POST",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createOrderForm").data('url_pengemasan_detail') + id_pengemasan + '/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id_pengemasan: id_pengemasan
                },

                success: function(response) {
                    // // console.log(response.data);
                    document.getElementById("id_tarif_pengemasan").value = response.data.tarif;
                    viewRupiah('id_tarif_pengemasan', 'id_tarif_pengemasan_tampil');
                    harga_pengemasan = str2int(response.data.tarif);
                    // document.getElementById("tarifLayanan").innerHTML = 'Rp. ' + response.harga;
                }
            }).done(function() {
                hitung_total();
            });
        } else {

        }


    });
    // ========================================= END MODUL PERHITUNGAN TARIF Pengemasan (Packing) ===================================

    // ========================================= MODUL PERHITUNGAN TOTAL TARIF =========================================
    function hitung_total() {
        var t_layanan = document.getElementById("id_tarif_layanan").value;
        var t_berat = document.getElementById("id_tarif_berat").value;
        var t_kilometer = document.getElementById("id_tarif_kilometer").value;
        var t_gudang = document.getElementById("id_tarif_gudang").value;
        var t_extra_cash_t = document.getElementById("id_extra_tarif_pengirim").value;
        var t_extra_cash_r = document.getElementById("id_extra_tarif_penerima").value;

        var n_layanan = str2int(t_layanan);
        var n_berat = str2int(t_berat);
        var n_kilometer = str2int(t_kilometer);
        var n_gudang = str2int(t_gudang);
        var n_extra_cash_t = str2int(t_extra_cash_t);
        var n_extra_cash_r = str2int(t_extra_cash_r);

        var total_tarif = n_layanan + n_berat + n_kilometer + n_gudang + harga_pengemasan + n_extra_cash_t + n_extra_cash_r;
        // console.log(n_layanan);

        document.getElementById("id_total_tarif").value = total_tarif;
        viewRupiah('id_total_tarif', 'id_total_tarif_tampil');
        // document.getElementById("tarifTotal").innerHTML = 'Rp. ' + total_tarif;

    }
    // ========================================= END MODUL PERHITUNGAN TOTAL TARIF =====================================

    // ========================================= PENCARIAN RUTE ========================================================
    function outlet_dan_gudang_yang_dilalui(data_gudang, data_penerima, data_pengirim) {
        var gd_penerima = []; //Array penampung jarak penerima dengan semua gudang
        var gd_pengirim = []; //Array penampung jarak pengirim dengan semua Gudang
        var id_gudang_terdekat_penerima;
        var id_gudang_terdekat_pengirim;

        var jarak_penerima = 0;
        var jarak_pengirim = 0;
        for (var i = 0; i < data_gudang.length; i++) {
            var loc_gudang = string_to_arr(data_gudang[i].titik_lokasi);
            jarak_penerima = hitung_jarak(loc_gudang[0], loc_gudang[1], data_penerima[1], data_penerima[0]);
            jarak_pengirim = hitung_jarak(loc_gudang[0], loc_gudang[1], data_pengirim[1], data_pengirim[0]);

            gd_penerima.push(jarak_penerima);
            gd_pengirim.push(jarak_pengirim);
        }

        var idx_terdekat_penerima = indexOfSmallest(gd_penerima); //index array dengan nilai terkecil di data jarak penerima
        var idx_terdekat_pengirim = indexOfSmallest(gd_pengirim); //index array dengan nilai terkecil di data jarak pengirim

        id_gudang_terdekat_pengirim = data_gudang[idx_terdekat_pengirim].id;
        id_gudang_terdekat_penerima = data_gudang[idx_terdekat_penerima].id;

        document.getElementById("id_gudang_pengiriman").value = id_gudang_terdekat_pengirim;
        document.getElementById("id_gudang_penerimaan").value = id_gudang_terdekat_penerima;

        var html_rute = "";
        var html_outlet_pengiriman = "";
        var html_outlet_penerimaan = "";

        var lokasi_outlet_penerima;
        var lokasi_outlet_pengirim;

        var jarak_total = 0;
        var jarak_pengirim = 0;
        var jarak_penerima = 0;


        $.ajax({
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createOrderForm").data('url_toko') + 'nearest/' + data_pengirim[1] + '/' + data_pengirim[0] + '/',
                success: function(response) {
                    // console.log(response);
                    html_outlet_pengiriman = response.data_html;
                    lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon
                    document.getElementById("id_outlet_pengiriman").value = response.data.id;

                },
                error: function(xhr, status, error) {
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                }

            })
            .done(function() {

                if (idx_terdekat_pengirim != null) {
                    html_rute = '<b><h3>Rute Pengiriman:</h3></b>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data_gudang[idx_terdekat_pengirim].titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data_gudang[idx_terdekat_pengirim].nama_gudang + ' | Alamat: ' + data_gudang[idx_terdekat_pengirim].alamat + '</small></p></div>';
                }
                if (idx_terdekat_penerima != null) {
                    html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data_gudang[idx_terdekat_penerima].titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data_gudang[idx_terdekat_penerima].nama_gudang + ' | Alamat: ' + data_gudang[idx_terdekat_penerima].alamat + '</small></p></div>';
                }
                $.ajax({
                        type: "GET",
                        url: $("#createOrderForm").data('url_toko') + 'nearest/' + data_penerima[1] + '/' + data_penerima[0] + '/',
                        success: function(response) {
                            // console.log(response);
                            html_outlet_penerimaan = response.data_html;
                            lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                            document.getElementById("id_outlet_penerimaan").value = response.data.id;

                        },
                        error: function(xhr, status, error) {
                            var error_response = xhr.responseJSON;
                            tampilkan_pesan(error_response.msg, error_response.type);
                        }

                    })
                    .done(function() {
                        html_rute = html_rute + html_outlet_penerimaan;
                        document.getElementById('rute_gudang').innerHTML = html_rute;
                        tampilkan_pesan("Berhasil Mencari Rute", "success");

                        var url_api_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_penerima[0] + "," + data_penerima[1] + "&end=" + lokasi_outlet_penerima[1] + "," + lokasi_outlet_penerima[0];
                        var url_api_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_pengirim[0] + "," + data_pengirim[1] + "&end=" + lokasi_outlet_pengirim[1] + "," + lokasi_outlet_pengirim[0];

                        $.ajax({
                            type: "GET",
                            url: url_api_penerima,
                            success: function(data) {
                                jarak_penerima = data.features[0].properties.summary.distance;
                                // console.log(jarak_penerima);
                            },
                            error: function(xhr, status, error) {
                                // if API not found route (length of route) calculate range manualy
                                jarak_penerima = hitung_jarak(data_penerima[1], data_penerima[0], lokasi_outlet_penerima[0], lokasi_outlet_penerima[1]);
                            },
                            complete: function() {
                                $.ajax({
                                    type: "GET",
                                    url: url_api_pengirim,
                                    success: function(data) {
                                        jarak_pengirim = data.features[0].properties.summary.distance;
                                        // console.log(jarak_pengirim);
                                    },
                                    error: function(xhr, status, error) {
                                        // if API not found route (length of route) calculate range manualy
                                        jarak_pengirim = hitung_jarak(data_pengirim[1], data_pengirim[0], lokasi_outlet_pengirim[0], lokasi_outlet_pengirim[1]);
                                    },
                                    complete: function() {
                                        jarak_total = (jarak_pengirim + jarak_penerima) / 1000;
                                        // console.log(jarak_total);

                                        // call function to calculate tarif kilometer;
                                        total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                        total_tarif_kilometer(jarak_total);

                                    }
                                });
                            }
                        });
                    });
            });
    }

    async function get_loc_degree_manual(alamat_pengirim, alamat_penerima) {
        // console.log("ASAL", alamat_pengirim, "TUJUAN", alamat_penerima)
        try {
            var url_api_geo = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=";
            var extra_cash_pengirim = 'Tidak Kena';
            var extra_cash_penerima = 'Tidak Kena';

            var t_arr = alamat_pengirim.split(',');
            var r_arr = alamat_penerima.split(',');

            var loc_pengirim;
            var loc_penerima;

            //fetch all gudang
            const response_gudang = await fetch($("#createOrderForm").data('url_gudang'));
            const data_gudang = await response_gudang.json();
            var gudangs = data_gudang.data;


            //Pencarian Titik Lokasi Untuk Pengirim
            // const T_response_1 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[0].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
            const T_response_1 = await fetch(url_api_geo + alamat_pengirim + "&size=1&country=IDN");
            const data_pengirim = await T_response_1.json();
            if (data_pengirim.features.length <= 0) {
                const T_response_2 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[2].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
                const data_pengirim = await T_response_2.json();
                if (data_pengirim.features.length <= 0) {
                    const T_response_3 = await fetch(url_api_geo + t_arr[2].trim() + ',' + t_arr[3].trim() + "&size=1&country=IDN");
                    const data_pengirim = await T_response_3.json();
                    if (data_pengirim.features.length <= 0) {
                        const T_response_4 = await fetch(url_api_geo + t_arr[3].trim() + "&size=1&country=IDN");
                        const data_pengirim = await T_response_4.json();
                        if (data_pengirim.features.length <= 0) {

                        } else {
                            loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                            extra_cash_pengirim = 'kabupaten';
                        }
                    } else {
                        loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                        extra_cash_pengirim = 'kota';
                    }
                } else {
                    loc_pengirim = data_pengirim.features[0].geometry.coordinates;
                    extra_cash_pengirim = 'kecamatan';
                }

            } else {
                loc_pengirim = data_pengirim.features[0].geometry.coordinates;
            }


            //Pencarian Titik Lokasi Untuk Penerima
            // const R_response_1 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[0].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
            const R_response_1 = await fetch(url_api_geo + alamat_penerima + "&size=1&country=IDN");
            const data_penerima = await R_response_1.json();
            if (data_penerima.features.length <= 0) {
                const R_response_2 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[2].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
                const data_penerima = await R_response_2.json();
                if (data_penerima.features.length <= 0) {
                    const R_response_3 = await fetch(url_api_geo + r_arr[2].trim() + ',' + r_arr[3].trim() + "&size=1&country=IDN");
                    const data_penerima = await R_response_3.json();
                    if (data_penerima.features.length <= 0) {
                        const R_response_4 = await fetch(url_api_geo + r_arr[3].trim() + "&size=1&country=IDN");
                        const data_penerima = await R_response_4.json();
                        if (data_penerima.features.length <= 0) {

                        } else {
                            loc_penerima = data_penerima.features[0].geometry.coordinates;
                            extra_cash_penerima = 'kabupaten';
                        }
                    } else {
                        loc_penerima = data_penerima.features[0].geometry.coordinates;
                        extra_cash_penerima = 'kota';
                    }
                } else {
                    loc_penerima = data_penerima.features[0].geometry.coordinates;
                    extra_cash_penerima = 'kecamatan';
                }

            } else {
                loc_penerima = data_penerima.features[0].geometry.coordinates;
            }
            var html_keterangan = '';
            var html_keterangan_2 = '';

            // console.log("LOC PENGIRIM", loc_pengirim, "LOC PENERIMA", loc_penerima);
            // console.log("EXTRA CASH PENGIRIM", extra_cash_pengirim, 'EXTRA CASH PENERIMA', extra_cash_penerima);

            if (extra_cash_penerima != 'Tidak Kena') {
                const response_extra_cash_penerima = await fetch($("#createOrderForm").data('url_extra_cash') + '?wilayah=' + extra_cash_penerima);
                const data_ec_penerima = await response_extra_cash_penerima.json();
                document.getElementById("id_extra_tarif_penerima").value = data_ec_penerima.harga;
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
                html_keterangan += 'Alamat Penerima Paket Kena Extra Cash (' + data_ec_penerima.wilayah + ')';
            } else {
                html_keterangan += 'Alamat Penerima Tidak Kena Extra Cash';
                document.getElementById("id_extra_tarif_penerima").value = '0';
                viewRupiah('id_extra_tarif_penerima', 'id_extra_tarif_penerima_tampil');
            }

            // Perlu karena paket dijemput kurir
            if (extra_cash_pengirim != 'Tidak Kena') {
                const response_extra_cash_pengirim = await fetch($("#createOrderForm").data('url_extra_cash') + '?wilayah=' + extra_cash_pengirim);
                const data_ec_pengirim = await response_extra_cash_pengirim.json();
                document.getElementById("id_extra_tarif_pengirim").value = data_ec_pengirim.harga;
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');
                html_keterangan_2 += '& Alamat Pengirim Paket Kena Extra Cash (' + data_ec_pengirim.wilayah + ')';
            } else {
                html_keterangan_2 += ' & Alamat Pengirim Tidak Kena Extra Cash';
                document.getElementById("id_extra_tarif_pengirim").value = '0';
                viewRupiah('id_extra_tarif_pengirim', 'id_extra_tarif_pengirim_tampil');
            }

            document.getElementById("id_keterangan_extra_tarif").value = html_keterangan + html_keterangan_2;
            document.getElementById("keterangan_extra_tarif_tampil").innerHTML = '<b><h3>Keterangan:</h3></b>' + html_keterangan + '<br>' + html_keterangan_2;

            clear_rute_gudang();
            // console.log('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima);
            tampilkan_pesan('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima, 'info');
            // outlet_dan_gudang_yang_dilalui(gudangs, loc_penerima, loc_pengirim);

            outlet_dan_gudang_yang_dilalui_manual(gudangs, loc_penerima, loc_pengirim, t_arr[0], r_arr[0]);
        } catch (e) {
            tampilkan_pesan(e.message + ", please check connection and refresh", 'error');
            return;
        } 
    }

    function outlet_dan_gudang_yang_dilalui_manual(data_gudang, data_penerima, data_pengirim, provinsi_pengirim, provinsi_penerima) {
        try {
            $('.rute-manual').remove();
        } catch(error){}
        $('#rute_gudang').html("");
        var gd_penerima = []; //Array penampung jarak penerima dengan semua gudang
        var gd_pengirim = []; //Array penampung jarak pengirim dengan semua Gudang
        var id_gudang_terdekat_penerima;
        var id_gudang_terdekat_pengirim;

        var loc_gudang_1 = [];
        var loc_gudang_2 = [];
        var loc_outlet_1 = [];
        var loc_outlet_2 = [];

        var gudang_pengiriman;
        var gudang_penerimaan;
        
        var html_rute = "";
        var html_outlet_pengiriman = "";
        var html_outlet_penerimaan = "";
        var html_rute_manual = "<div class='my-2 text-primary rute-manual' style='font-weight:lighter'>" +
        "<a style='cursor:pointer' data-toggle='modal' data-target='#modal-rute-manual'><i class='fa fa-cog'></i> &nbsp;Pilih Outlet dan Gudang secara manual</a></div>";

        var lokasi_outlet_penerima;
        var lokasi_outlet_pengirim;
        var provinsi_outlet_penerima;
        var provinsi_outlet_pengirim;
        var lokasi_outlet_pengirim_old = $('#id_outlet_pengiriman').val() || 0;
        var lokasi_outlet_penerima_old = $('#id_outlet_penerimaan').val() || 0;
        var lokasi_gudang_penerima_old = $('#id_gudang_penerimaan').val() || 0;
        var lokasi_gudang_pengirim_old = $('#id_gudang_pengiriman').val() || 0;

        var jarak_total = 0;
        var jarak_pengirim = 0;
        var jarak_penerima = 0;

        var jarak_pengirim_ke_outlet1 = 0;
        var jarak_outlet1_ke_gudang1 = 0;
        var jarak_gudang1_ke_gudang2 = 0;
        var jarak_gudang2_ke_outlet2 = 0;
        var jarak_gudang2_ke_penerima = 0;

        var outlet_pengirim = document.getElementById('inputOutletPengirimManual').value ? document.getElementById('inputOutletPengirimManual').value : 0;
        var gudang_pengirim = document.getElementById('inputGudangPengirimManual').value ? document.getElementById('inputGudangPengirimManual').value : 0;
        var gudang_penerima = document.getElementById('inputGudangPenerimaManual').value ? document.getElementById('inputGudangPenerimaManual').value : 0;
        var outlet_penerima = document.getElementById('inputOutletPenerimaManual').value ? document.getElementById('inputOutletPenerimaManual').value : 0;

        if(outlet_pengirim)
            var url_outlet_pengirim = $("#createOrderForm").data('url_toko') + 'list/' + outlet_pengirim + '/';
        else 
            var url_outlet_pengirim = $("#createOrderForm").data('url_toko') + 'list/' + lokasi_outlet_pengirim_old + '/';

        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: url_outlet_pengirim,
            success: function(response) {
                // // console.log("GUDANG ATAUPUN OUTLET TERDEKAT", response);
                html_outlet_pengiriman = response.data_html;
                lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon

                if(gudang_pengirim)
                    var url_gudang_pengirim = $("#createOrderForm").data('url_gudang_plain') + 'pengirim/list/' + gudang_pengirim + '/';
                else 
                    var url_gudang_pengirim = $("#createOrderForm").data('url_gudang_plain') + 'pengirim/list/' + lokasi_gudang_pengirim_old + '/';

                try {
                    loc_outlet_1 = string_to_arr(response.data.titik_lokasi);
                } catch(error) {}
                provinsi_outlet_pengirim = response.data.provinsi_toko;
                document.getElementById("id_outlet_pengiriman").value = response.data.id;
                // // console.log('RUTE OUTLET 1', html_outlet_pengiriman);
                 
                if (provinsi_outlet_pengirim) {
                    $.ajax({
                        type: "GET",
                        // url: $("#createOrderForm").data('url_gudang_province'),
                        url: url_gudang_pengirim,
                        dataType: "json",
                        data: {
                            csrfmiddlewaretoken: getCookie('csrftoken'),
                            province: provinsi_outlet_pengirim,
                        },
                        success: function(data) {
                            // // console.log('MERNCARI GUDANG', data);
                            loc_gudang_1 = string_to_arr(data.data.titik_lokasi);
                            jarak_outlet1_ke_gudang1 = hitung_jarak(lokasi_outlet_pengirim[0], lokasi_outlet_pengirim[1], loc_gudang_1[0], loc_gudang_1[1])
                            id_gudang_terdekat_pengirim = data.data.id;
                            document.getElementById("id_gudang_pengiriman").value = data.data.id;
                            html_rute += '<div class="row"><h4>Rute Pengiriman:</h4></div>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>';
                            $('#rute_gudang').append(html_rute);
                            // console.log('RUTE OUTLET 1 + GUDANG 1', html_rute);
                             
                            if(outlet_penerima)
                                var url_outlet_penerima = $("#createOrderForm").data('url_toko') + 'penerima/list/' + outlet_penerima + '/';
                            else 
                                var url_outlet_penerima = $("#createOrderForm").data('url_toko') + 'penerima/list/' + lokasi_outlet_penerima_old + '/';

                            $.ajax({
                                type: "GET",
                                // url: $("#createOrderForm").data('url_toko') + 'nearest/' + data_penerima[1] + '/' + data_penerima[0] + '/',
                                url: url_outlet_penerima,
                                success: function(response) {
                                    // // console.log(response);
                                    html_outlet_penerimaan = response.data_html;
                                    lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                                    try {
                                        loc_outlet_2 = string_to_arr(response.data.titik_lokasi);
                                    } catch(error) {}
                                    document.getElementById("id_outlet_penerimaan").value = response.data.id;
                                    provinsi_outlet_penerima = response.data.provinsi_toko;
                                    // console.log('RUTE OUTLET 2', html_outlet_penerimaan);
                                
                                    if(gudang_penerima)
                                        var url_gudang_penerima = $("#createOrderForm").data('url_gudang_plain') + 'penerima/list/' + gudang_penerima + '/';
                                    else 
                                        var url_gudang_penerima = $("#createOrderForm").data('url_gudang_plain') + 'penerima/list/' + lokasi_gudang_penerima_old + '/';

                                    if (provinsi_outlet_penerima) {
                                        $.ajax({
                                            type: "GET",
                                            // url: $("#createOrderForm").data('url_gudang_province'),
                                            url: url_gudang_penerima,
                                            dataType: "json",
                                            data: {
                                                csrfmiddlewaretoken: getCookie('csrftoken'),
                                                province: provinsi_outlet_penerima,
                                            },
                                            success: function(data) {
                                                loc_gudang_2 = string_to_arr(data.data.titik_lokasi);
                                                id_gudang_terdekat_penerima = data.data.id;
                                                document.getElementById("id_gudang_penerimaan").value = data.data.id;
                                                
                                                // console.log('RUTE OUTLET 1 + GUDANG 1 + RUTE OUTLET 2 + GUDANG 2', html_rute);
                                                // console.log("GUDANG TITIK", loc_gudang_1, loc_gudang_2);
                                                // html_rute = html_rute + html_outlet_penerimaan;
                                                // // console.log("RUTE KESELURUHAN", html_rute);
                                                // document.getElementById('rute_gudang').innerHTML = html_rute;
                                                // tampilkan_pesan("Berhasil Mencari Rute", "success");
        
                                                // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP GUDANG
                                                // console.log("DATA PENERIMA", data_penerima, "LOC GUDANG 2", loc_gudang_2, "LOC OUTLET 1", loc_outlet_1, "LOC OUTLET 2", loc_outlet_2);
                                                // console.log("DATA PENGIRIM", data_pengirim, "LOC GUDANG 1", loc_gudang_1, "LOC OUTLET 1", loc_outlet_1, "LOC OUTLET 2", loc_outlet_2);
                                                var url_api_outlet_1_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_1[1] + "," + loc_outlet_1[0] + "&end=" + data_pengirim[0] + "," + data_pengirim[1];
                                                var url_api_outlet_1_gudang_1 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_1[1] + "," + loc_outlet_1[0] + "&end=" + loc_gudang_1[1] + "," + loc_gudang_1[0];
                                                var url_api_gudang_1_gudang_2 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_gudang_1[1] + "," + loc_gudang_1[0] + "&end=" + loc_gudang_2[1] + "," + loc_gudang_2[0];
                                                var url_api_gudang_2_outlet_2 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_gudang_2[1] + "," + loc_gudang_2[0] + "&end=" + loc_outlet_2[1] + "," + loc_outlet_2[0];
                                                var url_api_gudang_2_loc_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_2[1] + "," + loc_outlet_2[0] + "&end=" + data_penerima[0] + "," + data_penerima[1];

                                                $.ajax({
                                                    type: "GET",
                                                    url: url_api_outlet_1_gudang_1,
                                                    success: function(data) {
                                                        jarak_outlet1_ke_gudang1 = data.features[0].properties.summary.distance;
                                                        // console.log("JARAK OUTLET1 GUDANG1 :  ", jarak_outlet1_ke_gudang1);
                                                    },
                                                    error: function(xhr, status, error) {                         
                                                        jarak_outlet1_ke_gudang1 = hitung_jarak(loc_outlet_1[0], loc_outlet_1[1], loc_gudang_1[0], loc_gudang_1[1]);
                                                        // console.log("JARAK OUTLET1 GUDANG 1 :  ", jarak_outlet1_ke_gudang1); 
        
                                                        // Perhitungan Jarak penerima terhadap Outlet
                                                        // jarak_penerima = hitung_jarak(data_penerima[1], data_penerima[0], lokasi_outlet_penerima[0], lokasi_outlet_penerima[1]);
                                                    },
                                                    complete: function() {
                                                        $.ajax({
                                                            type: "GET",
                                                            url: url_api_gudang_1_gudang_2,
                                                            success: function(data) {
                                                                jarak_gudang1_ke_gudang2 = data.features[0].properties.summary.distance;
                                                                // console.log("JARAK GUDANG1 GUDANG2 :  ", jarak_gudang1_ke_gudang2);
                                                            },
                                                            error: function(xhr, status, error) {
                                                                jarak_gudang1_ke_gudang2 = hitung_jarak(loc_gudang_1[0], loc_gudang_1[1], loc_gudang_2[0], loc_gudang_2[1]);
                                                                // console.log("JARAK GUDANG1 GUDANG2 :  ", jarak_gudang1_ke_gudang2);
        
                                                            },
                                                            complete: function() {
                                                                $.ajax({
                                                                    type: "GET",
                                                                    url: url_api_gudang_2_outlet_2,
                                                                    success: function(data) {
                                                                        jarak_gudang2_ke_outlet2 = data.features[0].properties.summary.distance;
                                                                        // console.log("JARAK GUDANG2 OUTLET2 :  ", jarak_gudang2_ke_outlet2);
                                                                    },
                                                                    error: function(xhr, status, error) {
                                                                        jarak_gudang2_ke_outlet2 = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], loc_outlet_2[0], loc_outlet_2[1]);
                                                                        // console.log("JARAK GUDANG2 OUTLET2 :  ", jarak_gudang2_ke_outlet2);
                
                                                                    },
                                                                    complete: function() {
                                                                        $.ajax({
                                                                            type: "GET",
                                                                            url: url_api_gudang_2_loc_penerima,
                                                                            success: function(data) {
                                                                                jarak_gudang2_ke_penerima = data.features[0].properties.summary.distance;
                                                                                // console.log("JARAK GUDANG2 PENERIMA :  ", jarak_gudang2_ke_penerima);
                                                                            },
                                                                            error: function(xhr, status, error) {
                                                                                jarak_gudang2_ke_penerima = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], data_penerima[1], data_penerima[0]);
                                                                                // console.log("JARAK GUDANG2 PENERIMA :  ", jarak_gudang2_ke_penerima);
                                                                            },
                                                                            complete: function() {
                                                                                $.ajax({
                                                                                    type: "GET",
                                                                                    url: url_api_outlet_1_pengirim,
                                                                                    success: function(data) {
                                                                                        jarak_pengirim_ke_outlet1 = data.features[0].properties.summary.distance;
                                                                                        // console.log("JARAK PENGIRIM OUTLET1 :  ", jarak_pengirim_ke_outlet1);
                                                                                    },
                                                                                    error: function(xhr, status, error) {
                                                                                        jarak_pengirim_ke_outlet1 = hitung_jarak(loc_outlet_1[0], loc_outlet_1[1], data_pengirim[1], data_pengirim[0]);
                                                                                        // console.log("JARAK PENGIRIM OUTLET1 :  ", jarak_pengirim_ke_outlet1);
                                                                                    },
                                                                                    complete: function() {
                                                                                        jarak_pengirim_ke_outlet1 = typeof(jarak_pengirim_ke_outlet1) !== "undefined" && !isNaN(jarak_pengirim_ke_outlet1) ? jarak_pengirim_ke_outlet1 : 0;
    
                                                                                        jarak_outlet1_ke_gudang1 = typeof(jarak_outlet1_ke_gudang1) !== "undefined" && !isNaN(jarak_outlet1_ke_gudang1) ? jarak_outlet1_ke_gudang1 : 0;
    
                                                                                        jarak_gudang1_ke_gudang2 = typeof(jarak_gudang1_ke_gudang2) !== "undefined" && !isNaN(jarak_gudang1_ke_gudang2) ? jarak_gudang1_ke_gudang2 : 0;
    
                                                                                        jarak_gudang2_ke_outlet2 = typeof(jarak_gudang2_ke_outlet2) !== "undefined" && !isNaN(jarak_gudang2_ke_outlet2) ? jarak_gudang2_ke_outlet2 : 0;
    
                                                                                        jarak_gudang2_ke_penerima = typeof(jarak_gudang2_ke_penerima) !== "undefined" && !isNaN(jarak_gudang2_ke_penerima) ? jarak_gudang2_ke_penerima : 0;
    
    
                                                                                        jarak_total = (jarak_pengirim_ke_outlet1 +jarak_outlet1_ke_gudang1 + jarak_gudang1_ke_gudang2 + jarak_gudang2_ke_outlet2 + jarak_gudang2_ke_penerima) / 1000;
                                                                                        // }
                                                                                        // console.log("JARAK TOTAL : ", jarak_total);
                                                                                        jarak_total = parseFloat(jarak_total) && !isNaN(jarak_total) ? parseFloat(jarak_total) : 0;
                                
                                                                                        // call function to calculate tarif kilometer;
                                                                                        total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                                                                        total_tarif_kilometer(jarak_total);

                                                                                        html_rute += '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>' + html_outlet_penerimaan;
                                                                                        $('#rute_gudang').html("");
                                                                                        $('#rute_gudang').append(html_rute);
                                                                                        try {
                                                                                            $('.rute-manual').remove();
                                                                                            setTimeout(function(){
                                                                                                document.getElementById("keterangan_extra_tarif_tampil").insertAdjacentHTML('afterend', html_rute_manual);
                                                                                            },100);
                                                                                        } catch(error){}

                                                                                        setTimeout(function(){
                                                                                            $('#modal-rute-manual').modal('hide');
                                                                                        },1000);
                                                                                        setTimeout(function(){
                                                                                            tampilkan_pesan("Berhasil Memilih Rute Outlet dan Gudang", "success");
                                                                                        },1500)
                                                                                    }
                                                                                });
                        
                                                                            }
                                                                        });            
                                                                    }
                                                                })
                                                            }
                                                        });
                                                    }
                                                });
                                            },
                                            error: function(xhr, status, error) {
                                                // console.log("ADA ERROR OUTLET 2 GUDANG 2 1 1", error);
                                                var error_response = xhr.responseJSON;
                                                setTimeout(function(){
                                                    $('#modal-rute-manual').modal('hide');
                                                },1000);
                                                setTimeout(function(){
                                                    tampilkan_pesan(error_response.msg, error_response.type);
                                                },1500)
                                            }
                                        });
                                    } else {
                                        setTimeout(function(){
                                            $('#modal-rute-manual').modal('hide');
                                        },1000);
                                        setTimeout(function(){
                                            tampilkan_pesan('Outlet Penerima Tidak Memiliki data Provinsi!', 'error');
                                        },1500)
                                    }

                                },
                                error: function(xhr, status, error) {
                                    // console.log("ADA ERROR OUTLET 2", error);
                                    var error_response = xhr.responseJSON;
                                    setTimeout(function(){
                                        $('#modal-rute-manual').modal('hide');
                                    },1000);
                                    setTimeout(function(){
                                        tampilkan_pesan(error_response.msg, error_response.type);
                                    },1500)
                                }
                            })

                        },
                        error: function(xhr, status, error) {
                            // console.log("ADA ERROR OUTLET 1 GUDANG 1", error);
                            var error_response = xhr.responseJSON;
                            setTimeout(function(){
                                $('#modal-rute-manual').modal('hide');
                            },1000);
                            setTimeout(function(){
                                tampilkan_pesan(error_response.msg, error_response.type);
                            },1500)
                        }
                    });
                } else {
                    setTimeout(function(){
                        $('#modal-rute-manual').modal('hide');
                    },1000);
                    setTimeout(function(){
                        tampilkan_pesan('Outlet Pengirim Tidak Memiliki data Provinsi!', 'error');
                    },1500)
                }

            },
            error: function(xhr, status, error) {
                var error_response = xhr.responseJSON;
                setTimeout(function(){
                    $('#modal-rute-manual').modal('hide');
                },1000);
                setTimeout(function(){
                    tampilkan_pesan(error_response.msg, error_response.type);
                },1500)
            }
        });
    }

    function outlet_dan_gudang_yang_dilalui_2(data_gudang, data_penerima, data_pengirim, provinsi_pengirim, provinsi_penerima) {
        // try{
        //     $('.overlay-load-data').toggleClass('in')
        // } catch(error){}
        try {
            $('.rute-manual').remove();
        } catch(error){}
        $('#rute_gudang').html("");
        var gd_penerima = []; //Array penampung jarak penerima dengan semua gudang
        var gd_pengirim = []; //Array penampung jarak pengirim dengan semua Gudang
        var id_gudang_terdekat_penerima;
        var id_gudang_terdekat_pengirim;

        var loc_gudang_1 = [];
        var loc_gudang_2 = [];
        var loc_outlet_1 = [];
        var loc_outlet_2 = [];

        var gudang_pengiriman;
        var gudang_penerimaan;
        
        var html_rute = "";
        var html_outlet_pengiriman = "";
        var html_outlet_penerimaan = "";
        var html_rute_manual = "<div class='my-2 text-primary rute-manual' style='font-weight:lighter'>" +
        "<a style='cursor:pointer' data-toggle='modal' data-target='#modal-rute-manual'><i class='fa fa-cog'></i> &nbsp;Pilih Outlet dan Gudang secara manual</a></div>";

        var lokasi_outlet_penerima;
        var lokasi_outlet_pengirim;
        var provinsi_outlet_penerima;
        var provinsi_outlet_pengirim;

        var jarak_total = 0;
        var jarak_pengirim = 0;
        var jarak_penerima = 0;

        var jarak_pengirim_ke_outlet1 = 0;
        var jarak_outlet1_ke_gudang1 = 0;
        var jarak_gudang1_ke_gudang2 = 0;
        var jarak_gudang2_ke_outlet2 = 0;
        var jarak_gudang2_ke_penerima = 0;

        $.ajax({
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createOrderForm").data('url_toko') + data_pengirim[1] + '/' + data_pengirim[0] + '/',
                success: function(response) {
                    // // console.log("GUDANG ATAUPUN OUTLET TERDEKAT", response);
                    html_outlet_pengiriman = response.data_html;
                    lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon
                    try {
                        loc_outlet_1 = string_to_arr(response.data.titik_lokasi);
                    } catch(error) {}
                    provinsi_outlet_pengirim = response.data.provinsi_toko_id;
                    document.getElementById("id_outlet_pengiriman").value = response.data.id;
                    // // console.log('RUTE OUTLET 1', html_outlet_pengiriman);

                },
                error: function(xhr, status, error) {
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                },
                complete: function() {
                    // // console.log('provinsi', provinsi_outlet_pengirim);
                    if (provinsi_outlet_pengirim) {
                        $.ajax({
                            type: "GET",
                            // url: $("#createOrderForm").data('url_gudang_province'),
                            url: $("#createOrderForm").data('url_gudang_plain') + lokasi_outlet_pengirim[0] + '/' + lokasi_outlet_pengirim[1] + '/',
                            dataType: "json",
                            data: {
                                csrfmiddlewaretoken: getCookie('csrftoken'),
                                province: provinsi_outlet_pengirim,
                            },
                            success: function(data) {
                                // // console.log('MERNCARI GUDANG', data);
                                loc_gudang_1 = string_to_arr(data.data.titik_lokasi);
                                jarak_outlet1_ke_gudang1 = hitung_jarak(lokasi_outlet_pengirim[0], lokasi_outlet_pengirim[1], loc_gudang_1[0], loc_gudang_1[1])
                                id_gudang_terdekat_pengirim = data.data.id;
                                document.getElementById("id_gudang_pengiriman").value = data.data.id;
                                html_rute += '<div class="row"><h4>Rute Pengiriman:</h4></div>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>';
                                $('#rute_gudang').append(html_rute);
                                // // console.log('RUTE OUTLET 1 + GUDANG 1', html_rute);

                            },
                            error: function(xhr, status, error) {
                                var error_response = xhr.responseJSON;
                                tampilkan_pesan(error_response.msg, error_response.type);
                            },
                            complete: function() {
                                $.ajax({
                                    type: "GET",
                                    // url: $("#createOrderForm").data('url_toko') + 'nearest/' + data_penerima[1] + '/' + data_penerima[0] + '/',
                                    url: $("#createOrderForm").data('url_toko')+ "nearest/" +data_penerima[1] + '/' + data_penerima[0] + '/',
                                    success: function(response) {
                                        // // console.log(response);
                                        html_outlet_penerimaan = response.data_html;
                                        lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                                        try {
                                            loc_outlet_2 = string_to_arr(response.data.titik_lokasi);
                                        } catch(error) {}
                                        document.getElementById("id_outlet_penerimaan").value = response.data.id;
                                        provinsi_outlet_penerima = response.data.provinsi_toko_id;
                                        // // console.log('RUTE OUTLET 2', html_outlet_penerimaan);
                                    },
                                    error: function(xhr, status, error) {
                                        var error_response = xhr.responseJSON;
                                        tampilkan_pesan(error_response.msg, error_response.type);
                                    },
                                    complete: function() {
                                        if (provinsi_outlet_penerima) {
                                            $.ajax({
                                                type: "GET",
                                                // url: $("#createOrderForm").data('url_gudang_province'),
                                                url: $("#createOrderForm").data('url_gudang_plain') + lokasi_outlet_penerima[0] + '/' + lokasi_outlet_penerima[1] + '/',
                                                dataType: "json",
                                                data: {
                                                    csrfmiddlewaretoken: getCookie('csrftoken'),
                                                    province: provinsi_outlet_penerima,
                                                },
                                                success: function(data) {
                                                    loc_gudang_2 = string_to_arr(data.data.titik_lokasi);
                                                    id_gudang_terdekat_penerima = data.data.id;
                                                    document.getElementById("id_gudang_penerimaan").value = data.data.id;
                                                    html_rute += '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>' + html_outlet_penerimaan;
                                                    $('#rute_gudang').html("");
                                                    $('#rute_gudang').append(html_rute);
                                                    try {
                                                        $('.rute-manual').remove();
                                                        setTimeout(function(){
                                                            document.getElementById("keterangan_extra_tarif_tampil").insertAdjacentHTML('afterend', html_rute_manual);
                                                        },100);
                                                    } catch(error){}
                                                    // // console.log('RUTE OUTLET 1 + GUDANG 1 + RUTE OUTLET 2 + GUDANG 2', html_rute);
                                                },
                                                error: function(xhr, status, error) {
                                                    var error_response = xhr.responseJSON;
                                                    tampilkan_pesan(error_response.msg, error_response.type);
                                                },
                                                complete: function() {
                                                    // console.log("GUDANG TITIK", loc_gudang_1, loc_gudang_2);
                                                    // html_rute = html_rute + html_outlet_penerimaan;
                                                    // // console.log("RUTE KESELURUHAN", html_rute);
                                                    // document.getElementById('rute_gudang').innerHTML = html_rute;
                                                    tampilkan_pesan("Berhasil Mencari Rute", "success");
            
                                                    // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP OUTLET
                                                    // var url_api_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_penerima[0] + "," + data_penerima[1] + "&end=" + lokasi_outlet_penerima[1] + "," + lokasi_outlet_penerima[0];
                                                    // var url_api_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_pengirim[0] + "," + data_pengirim[1] + "&end=" + lokasi_outlet_pengirim[1] + "," + lokasi_outlet_pengirim[0];
            
                                                    // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP GUDANG
                                                    // console.log("DATA PENERIMA", data_penerima, "LOC GUDANG 2", loc_gudang_2, "LOC OUTLET 1", loc_outlet_1, "LOC OUTLET 2", loc_outlet_2);
                                                    // console.log("DATA PENGIRIM", data_pengirim, "LOC GUDANG 1", loc_gudang_1, "LOC OUTLET 1", loc_outlet_1, "LOC OUTLET 2", loc_outlet_2);
                                                    var url_api_outlet_1_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_1[1] + "," + loc_outlet_1[0] + "&end=" + data_pengirim[0] + "," + data_pengirim[1];
                                                    var url_api_outlet_1_gudang_1 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_1[1] + "," + loc_outlet_1[0] + "&end=" + loc_gudang_1[1] + "," + loc_gudang_1[0];
                                                    var url_api_gudang_1_gudang_2 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_gudang_1[1] + "," + loc_gudang_1[0] + "&end=" + loc_gudang_2[1] + "," + loc_gudang_2[0];
                                                    var url_api_gudang_2_outlet_2 = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_gudang_2[1] + "," + loc_gudang_2[0] + "&end=" + loc_outlet_2[1] + "," + loc_outlet_2[0];
                                                    var url_api_gudang_2_loc_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + loc_outlet_2[1] + "," + loc_outlet_2[0] + "&end=" + data_penerima[0] + "," + data_penerima[1];

                                                    // var url_api_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_penerima[0] + "," + data_penerima[1] + "&end=" + loc_gudang_2[1] + "," + loc_gudang_2[0];
                                                    // var url_api_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_pengirim[0] + "," + data_pengirim[1] + "&end=" + loc_gudang_1[1] + "," + loc_gudang_1[0];
            
                                                    $.ajax({
                                                        type: "GET",
                                                        url: url_api_outlet_1_gudang_1,
                                                        success: function(data) {
                                                            jarak_outlet1_ke_gudang1 = data.features[0].properties.summary.distance;
                                                            // console.log("JARAK OUTLET1 GUDANG1 :  ", jarak_outlet1_ke_gudang1);
                                                        },
                                                        error: function(xhr, status, error) {                         
                                                            jarak_outlet1_ke_gudang1 = hitung_jarak(loc_outlet_1[0], loc_outlet_1[1], loc_gudang_1[0], loc_gudang_1[1]);
                                                            // console.log("JARAK OUTLET1 GUDANG 1 :  ", jarak_outlet1_ke_gudang1); 
            
                                                            // Perhitungan Jarak penerima terhadap Outlet
                                                            // jarak_penerima = hitung_jarak(data_penerima[1], data_penerima[0], lokasi_outlet_penerima[0], lokasi_outlet_penerima[1]);
                                                        },
                                                        complete: function() {
                                                            $.ajax({
                                                                type: "GET",
                                                                url: url_api_gudang_1_gudang_2,
                                                                success: function(data) {
                                                                    jarak_gudang1_ke_gudang2 = data.features[0].properties.summary.distance;
                                                                    // console.log("JARAK GUDANG1 GUDANG2 :  ", jarak_gudang1_ke_gudang2);
                                                                },
                                                                error: function(xhr, status, error) {
                                                                    jarak_gudang1_ke_gudang2 = hitung_jarak(loc_gudang_1[0], loc_gudang_1[1], loc_gudang_2[0], loc_gudang_2[1]);
                                                                    // console.log("JARAK GUDANG1 GUDANG2 :  ", jarak_gudang1_ke_gudang2);
            
                                                                },
                                                                complete: function() {
                                                                    $.ajax({
                                                                        type: "GET",
                                                                        url: url_api_gudang_2_outlet_2,
                                                                        success: function(data) {
                                                                            jarak_gudang2_ke_outlet2 = data.features[0].properties.summary.distance;
                                                                            // console.log("JARAK GUDANG2 OUTLET2 :  ", jarak_gudang2_ke_outlet2);
                                                                        },
                                                                        error: function(xhr, status, error) {
                                                                            jarak_gudang2_ke_outlet2 = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], loc_outlet_2[0], loc_outlet_2[1]);
                                                                            // console.log("JARAK GUDANG2 OUTLET2 :  ", jarak_gudang2_ke_outlet2);
                    
                                                                        },
                                                                        complete: function() {
                                                                            $.ajax({
                                                                                type: "GET",
                                                                                url: url_api_gudang_2_loc_penerima,
                                                                                success: function(data) {
                                                                                    jarak_gudang2_ke_penerima = data.features[0].properties.summary.distance;
                                                                                    // console.log("JARAK GUDANG2 PENERIMA :  ", jarak_gudang2_ke_penerima);
                                                                                },
                                                                                error: function(xhr, status, error) {
                                                                                    jarak_gudang2_ke_penerima = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], data_penerima[1], data_penerima[0]);
                                                                                    // console.log("JARAK GUDANG2 PENERIMA :  ", jarak_gudang2_ke_penerima);
                                                                                },
                                                                                complete: function() {
                                                                                    $.ajax({
                                                                                        type: "GET",
                                                                                        url: url_api_outlet_1_pengirim,
                                                                                        success: function(data) {
                                                                                            jarak_pengirim_ke_outlet1 = data.features[0].properties.summary.distance;
                                                                                            // console.log("JARAK PENGIRIM OUTLET1 :  ", jarak_pengirim_ke_outlet1);
                                                                                        },
                                                                                        error: function(xhr, status, error) {
                                                                                            jarak_pengirim_ke_outlet1 = hitung_jarak(loc_outlet_1[0], loc_outlet_1[1], data_pengirim[1], data_pengirim[0]);
                                                                                            // console.log("JARAK PENGIRIM OUTLET1 :  ", jarak_pengirim_ke_outlet1);
                                                                                        },
                                                                                        complete: function() {
                                                                                            jarak_pengirim_ke_outlet1 = typeof(jarak_pengirim_ke_outlet1) !== "undefined" && !isNaN(jarak_pengirim_ke_outlet1) ? jarak_pengirim_ke_outlet1 : 0;
        
                                                                                            jarak_outlet1_ke_gudang1 = typeof(jarak_outlet1_ke_gudang1) !== "undefined" && !isNaN(jarak_outlet1_ke_gudang1) ? jarak_outlet1_ke_gudang1 : 0;
        
                                                                                            jarak_gudang1_ke_gudang2 = typeof(jarak_gudang1_ke_gudang2) !== "undefined" && !isNaN(jarak_gudang1_ke_gudang2) ? jarak_gudang1_ke_gudang2 : 0;
        
                                                                                            jarak_gudang2_ke_outlet2 = typeof(jarak_gudang2_ke_outlet2) !== "undefined" && !isNaN(jarak_gudang2_ke_outlet2) ? jarak_gudang2_ke_outlet2 : 0;
        
                                                                                            jarak_gudang2_ke_penerima = typeof(jarak_gudang2_ke_penerima) !== "undefined" && !isNaN(jarak_gudang2_ke_penerima) ? jarak_gudang2_ke_penerima : 0;
        
        
                                                                                            jarak_total = (jarak_pengirim_ke_outlet1 +jarak_outlet1_ke_gudang1 + jarak_gudang1_ke_gudang2 + jarak_gudang2_ke_outlet2 + jarak_gudang2_ke_penerima) / 1000;
                                                                                            // }
                                                                                            // console.log("JARAK TOTAL : ", jarak_total);
                                                                                            jarak_total = parseFloat(jarak_total) && !isNaN(jarak_total) ? parseFloat(jarak_total) : 0;
                                    
                                                                                            // call function to calculate tarif kilometer;
                                                                                            total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                                                                            total_tarif_kilometer(jarak_total);
        
                                                                                            // try{
                                                                                            //     $('.overlay-load-data').toggleClass('in')
                                                                                            // } catch(error){}
                                                                                        }
                                                                                    });
                            
                                                                                }
                                                                            });            
                                                                        }
                                                                    })
                                                                }
                                                            });
                                                        }
                                                    });
                                                }
                                            });
                                        } else {
                                            tampilkan_pesan('Outlet Penerima Tidak Memiliki data Provinsi!', 'error');
                                        }
            
                                    }
                                })
                            }
                        });
                    } else {
                        tampilkan_pesan('Outlet Pengirim Tidak Memiliki data Provinsi!', 'error');
                    }

                }

            })
    }
    // ========================================= END PENCARIAN RUTE ====================================================

    // ========================================= MODUL SHOW DATA To Drop Down Field =====================================
    function show_kota_list(id_provinsi, pengirim_penerima, id_kota_select, nama_kota) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinsi + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinsi
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_kota_" + pengirim_penerima).html(response.data);
                document.getElementById("id_kota_" + pengirim_penerima).value = id_kota_select;
                document.getElementById("select2-id_kota_" + pengirim_penerima + "-container").innerHTML = nama_kota;
            }
        });
    }

    function show_kecamatan_list(id_kota, pengirim_penerima, id_kecamatan_select, nama_kecamatan) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_kecamatan_" + pengirim_penerima).html(response.data);
                document.getElementById("id_kecamatan_" + pengirim_penerima).value = id_kecamatan_select;
                document.getElementById("select2-id_kecamatan_" + pengirim_penerima + "-container").innerHTML = nama_kecamatan;
            }
        });
    }

    function show_desa_list(id_kecamatan, pengirim_penerima, id_desa_select, nama_desa) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_desa_" + pengirim_penerima).html(response.data);
                document.getElementById("id_desa_" + pengirim_penerima).value = id_desa_select;
                document.getElementById("select2-id_desa_" + pengirim_penerima + "-container").innerHTML = nama_desa;
            }
        });
    }

    function show_kode_pos_list(id_provinces, id_kota, id_kecamatan, id_desa, pengirim_penerima, id_kode_pos_select, kode_pos) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_kode_pos_" + pengirim_penerima).html(response.data);
                document.getElementById("id_kode_pos_" + pengirim_penerima).value = id_kode_pos_select;
                document.getElementById("select2-id_kode_pos_" + pengirim_penerima + "-container").innerHTML = kode_pos;
            }
        });
    }


    function show_provinsi_list() {

        $.ajax({
            type: "POST",
            url: $("#createOrderForm").data('url_provinsi'),
            success: function(response) {
                $("select#id_provinsi_pengirim").html(response.data);
                $("select#id_provinsi_penerima").html(response.data);
            }
        });
    }

    show_provinsi_list();
    // show_list_toko();

    $("#id_provinsi_pengirim").change(function() {
        var id_provinces = $(this).val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinces + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_kota_pengirim").html(response.data);
                getAjaxKota_pengirim();
            }
        });
    });

    $("#id_provinsi_penerima").change(function() {
        var id_provinces = $(this).val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinces + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#id_kota_penerima").html(response.data);
                getAjaxKota_penerima();
            }
        });
    });

    $("#id_kota_pengirim").change(getAjaxKota_pengirim);
    $("#id_kota_penerima").change(getAjaxKota_penerima);

    function getAjaxKota_pengirim() {
        var id_kota = $("#id_kota_pengirim").val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },
            success: function(response) {
                $("select#id_kecamatan_pengirim").html(response.data);
                getAjaxKecamatan_pengirim();
            }
        });
    }

    function getAjaxKota_penerima() {
        var id_kota = $("#id_kota_penerima").val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },
            success: function(response) {
                $("select#id_kecamatan_penerima").html(response.data);
                getAjaxKecamatan_penerima();
            }
        });
    }

    $("#id_kecamatan_pengirim").change(getAjaxKecamatan_pengirim);
    $("#id_kecamatan_penerima").change(getAjaxKecamatan_penerima);

    function getAjaxKecamatan_pengirim() {
        var id_kecamatan = $("#id_kecamatan_pengirim").val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },
            success: function(response) {
                $("select#id_desa_pengirim").html(response.data);
                getAjaxDesa_pengirim();
            }
        });
    }

    function getAjaxKecamatan_penerima() {
        var id_kecamatan = $("#id_kecamatan_penerima").val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },
            success: function(response) {
                $("select#id_desa_penerima").html(response.data);
                getAjaxDesa_penerima();
            }
        });
    }

    $("#id_desa_pengirim").change(getAjaxDesa_pengirim);
    $("#id_desa_penerima").change(getAjaxDesa_penerima);

    function getAjaxDesa_pengirim() {
        var id_provinces = $("#id_provinsi_pengirim").val();
        var id_kota = $("#id_kota_pengirim").val();
        var id_kecamatan = $("#id_kecamatan_pengirim").val();
        var id_desa = $("#id_desa_pengirim").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },
            success: function(response) {
                $("select#id_kode_pos_pengirim").html(response.data);
                alamat_pengirim = getSelectedText('id_desa_pengirim');
                alamat_pengirim += ", " + getSelectedText('id_kecamatan_pengirim');
                alamat_pengirim += ", " + getSelectedText('id_kota_pengirim');
                alamat_pengirim += ", " + getSelectedText('id_provinsi_pengirim');
                // // console.log(alamat_pengirim);
                if (alamat_pengirim && alamat_penerima) {
                    // // console.log(alamat_penerima);
                    // // console.log(alamat_pengirim);
                    get_loc_degree(alamat_pengirim, alamat_penerima);
                }

            }
        });
    }

    function getAjaxDesa_penerima() {
        var id_provinces = $("#id_provinsi_penerima").val();
        var id_kota = $("#id_kota_penerima").val();
        var id_kecamatan = $("#id_kecamatan_penerima").val();
        var id_desa = $("#id_desa_penerima").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createOrderForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },
            success: function(response) {
                $("select#id_kode_pos_penerima").html(response.data);
                alamat_penerima = getSelectedText('id_desa_penerima');
                alamat_penerima += ", " + getSelectedText('id_kecamatan_penerima');
                alamat_penerima += ", " + getSelectedText('id_kota_penerima');
                alamat_penerima += ", " + getSelectedText('id_provinsi_penerima');
                // // console.log(alamat_penerima);
                if (alamat_pengirim && alamat_penerima) {
                    // // console.log(alamat_penerima);
                    // // console.log(alamat_pengirim);
                    get_loc_degree(alamat_pengirim, alamat_penerima);
                }

            },

        });
    }
    // ========================================= END MODUL SHOW DATA To Drop Down Field =================================

    $('.select2-hidden-accessible').on("select2:unselecting", function(e) {
        try{
            $(e.target).trigger('change.select2');
            $(e.target).trigger('change');
        } catch(error){}
    });

    $('.select2-hidden-accessible').on("select2:select", function(e){
        try{
            hitung_total(); 
            // var alamat_penerima = "",
            // alamat_pengirim = "";

            // alamat_pengirim += getSelectedText('id_desa_pengirim');
            // alamat_pengirim += ", " + getSelectedText('id_kecamatan_pengirim');
            // alamat_pengirim += ", " + getSelectedText('id_kota_pengirim');
            // alamat_pengirim += ", " + getSelectedText('id_provinsi_pengirim');

            // alamat_penerima += getSelectedText('id_desa_penerima');
            // alamat_penerima += ", " + getSelectedText('id_kecamatan_penerima');
            // alamat_penerima += ", " + getSelectedText('id_kota_penerima');
            // alamat_penerima += ", " + getSelectedText('id_provinsi_penerima');
            // // console.log(e.target, alamat_penerima, alamat_pengirim);

            // if (alamat_pengirim && alamat_penerima) {
            //     // console.log(`ALAMAT PENGIRIM ${alamat_penerima}`);
            //     // console.log(`ALAMAT PENGIRIM ${alamat_pengirim}`);
            //     get_loc_degree(alamat_pengirim, alamat_penerima);
            //     hitung_total();
            // }
        } catch(error) { 
        // console.log(error) 
        }
    });

    $(document).on('click', '.btn-simpan-manual', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah rute...');
        get_loc_degree_manual(alamat_pengirim, alamat_penerima);
    });

    $('#inputProvinsiPengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Provinsi',
        language: "id"
    });
    $('#inputKotaPengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kota',
        language: "id"
    });
    $('#inputKecamatanPengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kecamatan',
        language: "id"
    });
    $('#inputDesaPengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Desa',
        language: "id"
    });
    $('#inputKodePosPengirim').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kode Pos',
        language: "id"
    });

    $('#inputProvinsiPenerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Provinsi',
        language: "id"
    });
    $('#inputKotaPenerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kota',
        language: "id"
    });
    $('#inputKecamatanPenerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kecamatan',
        language: "id"
    });
    $('#inputDesaPenerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Desa',
        language: "id"
    });
    $('#inputKodePosPenerima').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Kode Pos',
        language: "id"
    });
    $('#inputJenisBarang').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Jenis Barang',
        language: "id"
    });
    $('#inputLayanan').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Layanan',
        language: "id"
    });
    $('#inputPengemasan').select2({
        theme: 'bootstrap4',
        placeholder: 'Pilih Pengemasan',
        language: "id"
    });

    var my_token = 'pk.eyJ1IjoiYmhhcnUiLCJhIjoiY2l0dmhxYWcwMDA1cjJ6cW14eHVpaHp4eCJ9.atVtH1bNhN4WgYUrzh0h_g';
    var mymap = L.map('maps_tracking').setView([-8.652415520702286, 115.21718502044679], 8);
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
        maxZoom: 18,
        id: 'maps_tracking',
        accessToken: my_token
    }).addTo(mymap);

    function show_lokasi_kiriman(id_pengiriman) {
        if (marker_lokasi_terkini) {
            mymap.removeLayer(marker_lokasi_terkini);
        }

        (async () => {
            const rawResponse = await fetch($("#createPengirimanForm").data('url_current_location'), {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id_pengiriman: id_pengiriman,
                })
            });
            const content = await rawResponse.json();
            var location = content.data.titik_lokasi;
            if (location) {
                var lat_long = location.split(",");
                marker_lokasi_terkini = L.marker([lat_long[0], lat_long[1]], {
                    icon: IconLokasi
                }).addTo(mymap);
                marker_lokasi_terkini.bindPopup("<b>Lokasi Paket</b>").openPopup();
            }
            // // console.log(content);
        })();
        // setTimeout(show_lokasi_kiriman(id_pengiriman), 5000);
    }

    var IconGudang = L.icon({
        iconUrl: 'https://cdn0.iconfinder.com/data/icons/containers/512/self1.png',
        iconRetinaUrl: 'https://cdn0.iconfinder.com/data/icons/containers/512/self1.png',
        iconSize: [29, 24],
        iconAnchor: [9, 21],
        popupAnchor: [0, -14]
    });

    var IconOutlet = L.icon({
        iconUrl: 'https://cdn0.iconfinder.com/data/icons/shopping-and-ecommerce-15/512/sale_lineal_color_cnvrt-01-512.png',
        iconRetinaUrl: 'https://cdn0.iconfinder.com/data/icons/shopping-and-ecommerce-15/512/sale_lineal_color_cnvrt-01-512.png',
        iconSize: [29, 24],
        iconAnchor: [9, 21],
        popupAnchor: [0, -14]
    });

    var IconLokasi = L.icon({
        iconUrl: 'https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png',
        iconRetinaUrl: 'https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png',
        iconSize: [29, 24],
        iconAnchor: [9, 21],
        popupAnchor: [0, -14]
    });

    // $.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=-8.1152&lon=115.0944', function(data){
    //     // console.log(data);
    // });

    var theMarker = {};
    var markers_rute_1;
    var markers_rute_2;
    var theMarker_rute_1 = [];
    var theMarker_rute_2 = [];
    var marker_lokasi_terkini;
    var arcgisOnline = L.esri.Geocoding.arcgisOnlineProvider();

    function check_show_rincian() {
        var status = document.getElementById("inputStatusPengirim").value;

        var input_harga = document.getElementById("inputTotalTarif");
        input_harga.setAttribute("type", "hidden");
        if (status == 'goverment') {
            var input_harga = document.getElementById("inputTotalTarif");
            input_harga.setAttribute("type", "text");
            document.getElementById("rincian_tarif").style.display = "none";
            document.getElementById("label_total").innerHTML = "Input Harga Pengiriman";
        } else {
            var input_harga = document.getElementById("inputTotalTarif");
            input_harga.setAttribute("type", "hidden");
            document.getElementById("rincian_tarif").style.display = "block";
            document.getElementById("label_total").innerHTML = "Rincian Tarif";
            viewRupiah('inputTarifBerat', 'tarifBerat');
            viewRupiah('inputTarifKilometer', 'tarifKilometer');
            viewRupiah('inputTarifGudang', 'tarifGudang');
            viewRupiah('inputTarifLayanan', 'tarifLayanan');
            viewRupiah('inputTotalTarif', 'tarifTotal');
            viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
            viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
        }
    }

    function makeCode(text) {
        if (!text) {
            tampilkan_pesan('ID/Resi Tidak ada!', 'error');
            return;
        }
        document.getElementById("qrcode").innerHTML = '';
        var qrcode = new QRCode(document.getElementById("qrcode"), {
            width: 100,
            height: 100
        });

        qrcode.makeCode(text);
    }

    function create_jalur(pengiriman_penerimaan, latlong_from, latlong_to) {

        if (latlong_from && latlong_to) {
            var data_from = latlong_from.split(",");
            var data_to = latlong_to.split(",");

            $.ajax({
                type: "GET", //rest Type
                dataType: 'json',
                url: "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_from[1] + "," + data_from[0] + "&end=" + data_to[1] + "," + data_to[0] + "",
                async: false,
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    // console.log(data);

                    var marker_loc = data.metadata.query.coordinates;
                    // console.log(marker_loc);
                    if (pengiriman_penerimaan == 'Pengiriman') {
                        markers_rute_1 = L.geoJSON(data).addTo(mymap);
                    } else {
                        markers_rute_2 = L.geoJSON(data).addTo(mymap);
                    }


                    for (var i = 0; i < marker_loc.length; i++) {
                        if (pengiriman_penerimaan == 'Pengiriman') {

                            if (i == 0) {
                                theMarker_rute_1[i] = L.marker([marker_loc[i][1], marker_loc[i][0]], {
                                    icon: IconOutlet
                                }).addTo(mymap);
                                theMarker_rute_1[i].bindPopup("<b>Outlet Pengiriman</b>").openPopup();
                            } else {
                                theMarker_rute_1[i] = L.marker([marker_loc[i][1], marker_loc[i][0]], {
                                    icon: IconGudang
                                }).addTo(mymap);
                                theMarker_rute_1[i].bindPopup("<b>Gudang Pengiriman</b>").openPopup();
                            };
                        } else {

                            if (i == 0) {
                                theMarker_rute_2[i] = L.marker([marker_loc[i][1], marker_loc[i][0]], {
                                    icon: IconOutlet
                                }).addTo(mymap);
                                theMarker_rute_2[i].bindPopup("<b>Outlet Penerimaan</b>").openPopup();
                            } else {
                                theMarker_rute_2[i] = L.marker([marker_loc[i][1], marker_loc[i][0]], {
                                    icon: IconGudang
                                }).addTo(mymap);
                                theMarker_rute_2[i].bindPopup("<b>Gudang Penerimaan</b>").openPopup();
                            };
                        };

                    }
                }
            });
        }
    }

    $(document).on('click', 'tr.data-log', function(){
        try{
            var data_is = data_log[parseInt($(this).data('log'))];
            $('.status-log').val(data_is.status);
            $('.penempatan-log').val(data_is.penempatan);
            $('.no-telp-log').val(data_is.no_telp);
            $('.kurir-nama-log').val(data_is.nama_kurir);
        } catch(error){
            // console.log('error mendapatkan detail scan data')
        }
    })

    // DETAIL PENGIRIMAN
    var data_log = [];
    $('body').on('click', '.detailPengiriman', function(event) {
        data_log = [];
        event.preventDefault();
        $("#createPengirimanForm")[0].reset();
        // check_show_rincian();
        var pengemasanSelect = $('#inputPengemasan');
        var layananSelect = $('#inputLayanan');
        var id_pengiriman = $(this).data("id");
        if (markers_rute_1) {
            mymap.removeLayer(markers_rute_1);
        };
        if (markers_rute_2) {
            mymap.removeLayer(markers_rute_2);
        };
        if (theMarker_rute_1) {
            for (var i = 0; i < theMarker_rute_1.length; i++) {
                mymap.removeLayer(theMarker_rute_1[i]);
            }

        };
        if (theMarker_rute_2) {
            for (var i = 0; i < theMarker_rute_2.length; i++) {
                mymap.removeLayer(theMarker_rute_2[i]);
            }
        };
        $.ajax({
            url: $("#createPengirimanForm").data('url') + id_pengiriman + '/detail/',
            type: 'get',
            success: function(response) {
                document.getElementById('custom-tabs-two-pengirim-tab').click();
                // console.log("RESPON SERVER", response);
                document.getElementById("inputNamaPengirim").value = response.data.nama_pengirim;
                document.getElementById("inputNoTlpPengirim").value = response.data.no_telp_pengirim;
                // document.getElementById("inputEmailPengirim").value = response.data.email_pengirim;
                document.getElementById("inputAlamatPengirim").value = response.data.alamat_pengirim;
                document.getElementById("id_outlet_pengiriman").value = response.data.id_outlet_pengiriman;
                document.getElementById("tampil_outlet_pengiriman").value = response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat;

                document.getElementById("inputProvinsiPengirim").innerHTML = '<option selected>' + response.data.provinsi_pengirim + '</option>';
                document.getElementById("inputKotaPengirim").innerHTML = '<option selected>' + response.data.kota_pengirim + '</option>';
                document.getElementById("inputKecamatanPengirim").innerHTML = '<option selected>' + response.data.kecamatan_pengirim + '</option>';
                document.getElementById("inputDesaPengirim").innerHTML = '<option selected>' + response.data.desa_pengirim + '</option>';
                document.getElementById("inputKodePosPengirim").innerHTML = '<option selected>' + response.data.kode_pos_pengirim + '</option>';

                document.getElementById("inputNamaPenerima").value = response.data.nama_penerima;
                document.getElementById("inputNoTlpPenerima").value = response.data.no_telp_penerima;
                // document.getElementById("inputEmailPenerima").value = response.data.email_penerima;
                document.getElementById("inputAlamatPenerima").value = response.data.alamat_penerima;

                document.getElementById("inputProvinsiPenerima").innerHTML = '<option selected>' + response.data.provinsi_penerima + '</option>';
                document.getElementById("inputKotaPenerima").innerHTML = '<option selected>' + response.data.kota_penerima + '</option>';
                document.getElementById("inputKecamatanPenerima").innerHTML = '<option selected>' + response.data.kecamatan_penerima + '</option>';
                document.getElementById("inputDesaPenerima").innerHTML = '<option selected>' + response.data.desa_penerima + '</option>';
                document.getElementById("inputKodePosPenerima").innerHTML = '<option selected>' + response.data.kode_pos_penerima + '</option>';

                document.getElementById("inputJenisBarang").value = response.data.jenis_barang;
                document.getElementById("select2-inputJenisBarang-container").innerHTML = response.data.jenis_barang;
                
                document.getElementById("inputDetailBarang").value = response.data.detail_barang;
                document.getElementById("inputPengemasan").value = response.data.id_pengemasan;

                var option = new Option(response.data.pengemasan, response.data.id_pengemasan, true, true);
                pengemasanSelect.append(option).trigger('change');

                var option_layanan = new Option(response.data.layanan, response.data.id_layanan, true, true);
                layananSelect.append(option_layanan).trigger('change');

                document.getElementById("select2-inputPengemasan-container").innerHTML = response.data.pengemasan;

                document.getElementById("inputLayanan").value = response.data.id_layanan;
                document.getElementById("select2-inputLayanan-container").innerHTML = response.data.layanan;
                document.getElementById("inputBerat").value = response.data.berat;
                document.getElementById("inputJumlah").value = response.data.jumlah;
                document.getElementById("inputSatuan_pengiriman").innerHTML = '<option selected>' + response.data.data_satuan + '</option>';

                document.getElementById("inputTarifBerat").value = response.data.tarif_berat;
                document.getElementById("inputTarifKilometer").value = response.data.tarif_kilometer;
                document.getElementById("inputTarifGudang").value = response.data.tarif_gudang;
                document.getElementById("inputTarifLayanan").value = response.data.tarif_layanan;
                document.getElementById("inputTotalTarif").value = response.data.total_tarif;
                document.getElementById("inputTarifPengemasan").value = response.data.tarif_pengemasan;
                document.getElementById("inputExtraTarifPenerima").value = response.data.extra_tarif_penerima;
                document.getElementById("keterangan_pengiriman").innerHTML = response.data.keterangan_extra_tarif;

                // viewRupiah('inputTarifBerat', 'tarifBerat');
                // viewRupiah('inputTarifKilometer', 'tarifKilometer');
                // viewRupiah('inputTarifGudang', 'tarifGudang');
                // viewRupiah('inputTarifLayanan', 'tarifLayanan');
                // viewRupiah('inputTotalTarif', 'tarifTotal');
                // viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');

                viewRupiah('inputTarifBerat', 'tarifBerat');
                viewRupiah('inputTarifKilometer', 'tarifKilometer');
                viewRupiah('inputTarifGudang', 'tarifGudang');
                viewRupiah('inputTarifLayanan', 'tarifLayanan');
                viewRupiah('inputTotalTarif', 'tarifTotal');
                viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
                viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');

                var html_rute = '<div class=""><h4>Rute Pengiriman:</h4><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div>';

                document.getElementById("rute_gudang_pengiriman").innerHTML = html_rute;
                // document.getElementById("status_pengiriman").innerHTML = '<div class="form-group row"><label for="statusPengiriman" class="col-sm-2 col-form-label">Status</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.status.data + '"></div></div><div class="form-group row"><label for="idKurirPengiriman" class="col-sm-2 col-form-label">ID Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.id + '"></div></div><div class="form-group row"><label for="namaKurirPengiriman" class="col-sm-2 col-form-label">Nama Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.nama + '"></div></div><div class="form-group row"><label for="noKurirPengiriman" class="col-sm-2 col-form-label">No. Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.kontak + '"></div></div>';
                // // console.log(response);
                document.getElementById("status_pengiriman_pengiriman").innerHTML = '<div class="form-group row"><label for="statusPengiriman" class="col-sm-4 col-form-label">Status</label><div class="col-sm-8"><input class="form-control status-log" type="text" disabled value="' + response.status.data + '"></div></div><div class="form-group row"><label for="namaKurirPengiriman" class="col-sm-4 col-form-label">Discan Oleh</label><div class="col-sm-8"><input class="form-control kurir-nama-log" type="text" disabled value="' + response.kurir.nama + '"></div></div> <div class="form-group row"><label for="penempatanKurir" class="col-sm-4 col-form-label">Penempatan</label><div class="col-sm-8"><input class="form-control penempatan-log" type="text" disabled value="' + response.kurir.penempatan + '"></div></div> <div class="form-group row"><label for="noKurirPengiriman" class="col-sm-4 col-form-label">Telp.</label><div class="col-sm-8"><input class="form-control no-telp-log" type="text" disabled value="' + response.kurir.kontak + '"></div></div>';

                var html_log = '';
                for (var i = 0; i < response.log.length; i++) {

                    var date_time = response.log[i].created_at;
                    date_time = formatDate(new Date(date_time));
                    // // console.log(formatDate(new Date(date_time)));
                    var dateTime = date_time.split(" ");
                    var date = dateTime[0];
                    var time = dateTime[1];

                    var penempatan = response.log[i].kurir_penempatan_outlet ? response.log[i].kurir_penempatan_outlet : response.log[i].kurir_penempatan_gudang ? response.log[i].kurir_penempatan_gudang : '';
                    var status = response.log[i].status_pengiriman ? response.log[i].status_pengiriman : '';
                    var no_telp = response.log[i].kurir_telp ? response.log[i].kurir_telp : ''
                    var kurir_nama = response.log[i].kurir_nama ? response.log[i].kurir_nama : '';

                    data_log[i] = {status:status,penempatan:penempatan,no_telp:no_telp,nama_kurir:kurir_nama};
                    // console.log(data_log)

                    html_log = html_log + '<tr class="data-log" data-log='+i+'><td>' + (i + 1) + '</td> <td>' + date + '</td> <td>' + time + '</td> <td>' + response.log[i].status_pengiriman + '</td></tr>';
                }

                var log_activity = '<h4>LOG:</h4><br><table class="table table-bordered table-striped"><thead><tr><th>No</th><th>Tanggal</th><th>Jam</th><th>Status</th></tr></thead><tbody style="font-size:15px; height: 100px; overflow-y: auto; overflow-x: hidden;">' + html_log + '</tbody></table>';
                document.getElementById("log_pengiriman").innerHTML = log_activity;

                makeCode(response.data.id_pengiriman);
                document.getElementById("updateButton").style.display = "none";
                document.getElementById("createButton").style.display = "none";
                document.getElementById("maps_tracking").style.display = "block";
                document.getElementById("maps_tracking").style.height = "350px";
                document.getElementById("title_modal").innerHTML = "Detail Data Pengiriman";
                $("#createPengirimanForm input").prop("disabled", true);
                $("#createPengirimanForm textarea").prop("disabled", true);
                $("#createPengirimanForm select").prop("disabled", true);

                // $("#loadMe").modal("hide");
                create_jalur('Pengiriman', response.rute.outlet_1.titik_lokasi, response.rute.gudang_1.titik_lokasi);
                create_jalur('Penerimaan', response.rute.outlet_2.titik_lokasi, response.rute.gudang_2.titik_lokasi);
                show_lokasi_kiriman(response.data.id);

                setTimeout(function() {
                    mymap.invalidateSize()
                    $('#modal_pengiriman').modal('show');
                }, 100);
            },
            error: function(xhr, status, error) {
                // $("#loadMe").modal("hide");
                var error_response = xhr.responseJSON;

                tampilkan_pesan(error_response.msg, error_response.type);
            }
        })

    });
});