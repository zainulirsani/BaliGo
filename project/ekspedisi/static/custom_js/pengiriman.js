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

    $('#inputNoTlpPengirim').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $('#inputNoTlpPenerima').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $(function() {
        $("input[name='berat']").on('input', function(e) {
            // $(this).val($(this).val().replace(/[^0-9]/g, ''));
            // $(this).val($(this).val().replace(/^\d*\.?\d*$/, ''));
            // return e.charCode === 0 || ((e.charCode >= 48 && e.charCode <= 57) || (e.charCode == 46 && document.getElementById("test").value.indexOf('.') < 0));

        });
    });

    $(function() {
        $("input[name='jumlah']").on('input', function(e) {
            $(this).val($(this).val().replace(/[^0-9]/g, ''));
        });
    });

    $(function() {
        $("input[name='total_tarif']").on('input', function(e) {
            $(this).val($(this).val().replace(/[^0-9]/g, ''));
        });
    });

    $('#panjang_barang').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $('#lebar_barang').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $('#tinggi_barang').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $("#panjang_barang").keyup(function() {
        hitungBerat();
    });

    $("#lebar_barang").keyup(function() {
        hitungBerat();
    });

    $("#tinggi_barang").keyup(function() {
        hitungBerat();
    });

    function hitungBerat() {
        var panjang = document.getElementById("panjang_barang").value;
        var lebar = document.getElementById("lebar_barang").value;
        var tinggi = document.getElementById("tinggi_barang").value;

        panjang = panjang == "" ? 0 : panjang;
        lebar = lebar == "" ? 0 : lebar;
        tinggi = tinggi == "" ? 0 : tinggi;

        var volume = parseInt(panjang) * parseInt(lebar) * parseInt(tinggi);
        // console.log(volume)
        // var volume2berat = Math.round((parseInt(panjang) * parseInt(lebar) * parseInt(tinggi)) / 6000);
        try {
            var volumeCekOns = parseFloat("0" +parseFloat(volume / 6000).toFixed(1).slice(-2));
            // console.log("VOLUME BERAT", volumeCekOns)
            if(volumeCekOns >= 0.1)
                var volume2berat = Math.floor(parseFloat(volume / 6000)) + 1;
            else 
                var volume2berat = (parseInt(parseFloat(volume / 6000).toFixed(0)))
        } catch(error){
            // console.log(error);
            var volume2berat = Math.round(parseFloat(volume / 6000));
        }
        if (volume2berat > 0) {
            hitung_berat_input(volume2berat);
        }
        document.getElementById("volume").value = volume;
        document.getElementById("volume2berat").value = volume2berat;
        document.getElementById("inputBerat").value = volume2berat;
    }

    $("#inputBerat").keyup(function() {
        document.getElementById("panjang_barang").value = "";
        document.getElementById("lebar_barang").value = "";
        document.getElementById("tinggi_barang").value = "";
        document.getElementById("volume").value = "";
        document.getElementById("volume2berat").value = "";
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

    function formatRupiah(angka, prefix) {
        try {
            if (angka.includes('.00')) {
                angka = angka.split('.00')[0];
            }
        } catch (error) {
            // console.log(error);
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
        // // console.log(output);
        document.getElementById(output_id).innerHTML = output;
    }

    $('#inputPengemasan').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_pengemasan'),
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
        placeholder: 'Tidak Memerlukan Pengemasan Lagi',
        language: "id"
    });


    // ===================================== Bagian Input Pengirim =====================

    $('#cari_pengirim').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_pelanggan') + 'select2',
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
                            text: item.text,
                            html: item.html
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },

        },
        escapeMarkup: function(markup) { return markup; },
        templateResult: function(d) { return d.html; },
        templateSelection: function(d) { return d.text; },

        theme: 'bootstrap4',
        placeholder: 'Pilih Pelanggan',
        language: "id"
    });


    $("#cari_pengirim").change(function() {
        var id_pelanggan = $(this).val();
        var response;
        // console.log('ID: ' + id_pelanggan);
        if (id_pelanggan == null) {
            document.getElementById("inputNamaPengirim").value = '';
            document.getElementById("inputNoTlpPengirim").value = '';
            document.getElementById("inputAlamatPengirim").value = '';
            document.getElementById("inputStatusPengirim").value = 'personal';
            setTimeout(function() {
                check_show_rincian();
            }, 500);
        } else {
            $.ajax({
                type: "GET",
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id: id_pelanggan
                },
                dataType: 'json',
                contentType: "application/json",
                url: $("#createPengirimanForm").data('url_pelanggan') + 'detail/',
                success: function(response) {
                    response = response;
                    try {
                        setTimeout(function() {
                            document.getElementById("inputNamaPengirim").value = response.data.first_name;
                            document.getElementById("inputNoTlpPengirim").value = response.data.no_telp;
                            document.getElementById("inputAlamatPengirim").value = response.data.alamat;
                            document.getElementById("inputStatusPengirim").value = response.data.register_sebagai;
                            check_if_goverment();

                            try {
                                // $('#inputProvinsiPengirim').val(null).trigger('change');
                                // $('#inputKotaPengirim').val(null).trigger('change');
                                // $('#inputKecamatanPengirim').val(null).trigger('change');
                                // $('#inputDesaPengirim').val(null).trigger('change');
                                // $('#inputKodePosPengirim').val(null).trigger('change');
                                
                                // $_provinsi = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.provinsi : 0;
                                // if($_provinsi){
                                //     setTimeout(function(){
                                //         $('#inputProvinsiPengirim').val($_provinsi).trigger('change');
                                //     },200)
                                //     setTimeout(function(){
                                //         $('#inputKotaPengirim').val('').trigger('change');
                                //         $('#inputKecamatanPengirim').val('').trigger('change');
                                //         $('#inputDesaPengirim').val('').trigger('change');
                                //         $('#inputKodePosPengirim').val('').trigger('change');
                                //     },400);
                                // }

                                // try {
                                //     $_kota = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kota : 0;
                                //     if($_kota){
                                //         setTimeout(function(){
                                //             $('#inputKotaPengirim').val($_kota).trigger('change');
                                //         },450);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputKecamatanPengirim').val('').trigger('change');
                                //         $('#inputDesaPengirim').val('').trigger('change');
                                //         $('#inputKodePosPengirim').val('').trigger('change');
                                //     },650)
                                // } catch(error){}

                                // try {
                                //     $_kecamatan = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kecamatan : 0;
                                //     if($_kecamatan){
                                //         setTimeout(function(){
                                //             $('#inputKecamatanPengirim').val($_kecamatan).trigger('change');
                                //         },700);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputDesaPengirim').val('').trigger('change');
                                //         $('#inputKodePosPengirim').val('').trigger('change');
                                //     },900)
                                // } catch(error){}

                                // try {
                                //     $_desa = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.desa : 0;
                                //     if($_desa){
                                //         setTimeout(function(){
                                //             $('#inputDesaPengirim').val($_desa).trigger('change');
                                //         },950);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputKodePosPengirim').val('').trigger('change');
                                //     },1150)
                                // } catch(error){}

                                // try {
                                //     $_kodepos = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kode_pos : 0;
                                //     if($_kodepos){
                                //         setTimeout(function(){
                                //             $('#inputKodePosPengirim').val($_kodepos).trigger('change');
                                //         },1200);
                                //     }
                                // } catch(error){}
                                $('#inputProvinsiPengirim').val(response.data.detail_pelanggan.provinsi_id).trigger('change');
                                setTimeout(function(){
                                document.getElementById("select2-inputProvinsiPengirim-container").innerHTML = response.data.detail_pelanggan.provinsi__nama_provinsi;
                                show_kota_list(response.data.detail_pelanggan.provinsi_id, 'Pengirim', response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kota__nama_kota);
                                show_kecamatan_list(response.data.detail_pelanggan.kota_id, 'Pengirim', response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.kecamatan__nama_kecamatan);
                                show_desa_list(response.data.detail_pelanggan.kecamatan_id, 'Pengirim', response.data.detail_pelanggan.desa_id, response.data.detail_pelanggan.desa__nama_desa);
                                show_kode_pos_list(response.data.detail_pelanggan.provinsi_id, response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.desa_id, 'Pengirim', response.data.detail_pelanggan.kode_pos_id, response.data.detail_pelanggan.kode_pos__kode_pos);
                                },200)

                            } catch(error){}

                        }, 500);
                    } catch {
                        setTimeout(function() {
                            // console.log('selected Pelanggan Failed to add in form!');
                            document.getElementById("inputNamaPengirim").value = '';
                            document.getElementById("inputNoTlpPengirim").value = '';
                            document.getElementById("inputAlamatPengirim").value = '';
                            document.getElementById("inputStatusPengirim").value = 'personal';
                        }, 500);
                    }
                    setTimeout(function() {
                        check_show_rincian();
                    }, 500);
                }
            });
        }

    });

    // Bagian Text Area Nama Pengirim

    $("#inputNamaPengirim").keyup(function() {
        var status = document.getElementById("inputStatusPengirim").value;
        // jadi ketika drop down cari pengirim 
        if (status == 'goverment') {
            document.getElementById("inputNamaPengirim").value = '';
            document.getElementById("inputNoTlpPengirim").value = '';
            document.getElementById("inputAlamatPengirim").value = '';
            $('#cari_pengirim').val(null).trigger('change');
            document.getElementById("inputStatusPengirim").value = 'personal';
        }
    });

    // ================================ END Bagian Input Pengirim ==========================

    // ================================ Bagian Jenis barang/kiriman ======================================
    $('#inputJenisBarang').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_jenis_kiriman'),
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
                // console.log(data);
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
    // ===================================== Bagian Input Penerima =====================

    $('#cari_penerima').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_pelanggan') + 'select2',
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
                            text: item.text,
                            html: item.html,
                        }
                    }),
                    pagination: {
                        more: data.total_count >= (page * 10)
                    }
                };
            },
        },
        escapeMarkup: function(markup) { return markup; },
        templateResult: function(d) { return d.html; },
        templateSelection: function(d) { return d.text; },
        theme: 'bootstrap4',
        placeholder: 'Pilih Pelanggan',
        language: "id"
    });


    $("#cari_penerima").change(function() {
        var id_pelanggan = $(this).val();
        var response;
        if (id_pelanggan == null) {
            document.getElementById("inputNamaPenerima").value = '';
            document.getElementById("inputNoTlpPenerima").value = '';
            document.getElementById("inputAlamatPenerima").value = '';
        } else {
            $.ajax({
                type: "GET",
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id: id_pelanggan
                },
                dataType: 'json',
                contentType: "application/json",
                url: $("#createPengirimanForm").data('url_pelanggan') + 'detail/',
                success: function(response) {
                    response = response;
                    try {
                        setTimeout(function() {
                            document.getElementById("inputNamaPenerima").value = response.data.first_name;
                            document.getElementById("inputNoTlpPenerima").value = response.data.no_telp;
                            document.getElementById("inputAlamatPenerima").value = response.data.alamat;

                            try {
                                // $('#inputProvinsiPenerima').val(null).trigger('change');
                                // $('#inputKotaPenerima').val(null).trigger('change');
                                // $('#inputKecamatanPenerima').val(null).trigger('change');
                                // $('#inputDesaPenerima').val(null).trigger('change');
                                // $('#inputKodePosPenerima').val(null).trigger('change');
                                
                                // $_provinsi = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.provinsi : 0;
                                // if($_provinsi){
                                //     setTimeout(function(){
                                //         $('#inputProvinsiPenerima').val($_provinsi).trigger('change');
                                //     },200)
                                //     setTimeout(function(){
                                //         $('#inputKotaPenerima').val('').trigger('change');
                                //         $('#inputKecamatanPenerima').val('').trigger('change');
                                //         $('#inputDesaPenerima').val('').trigger('change');
                                //         $('#inputKodePosPenerima').val('').trigger('change');
                                //     },400);
                                // }

                                // try {
                                //     $_kota = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kota : 0;
                                //     if($_kota){
                                //         setTimeout(function(){
                                //             $('#inputKotaPenerima').val($_kota).trigger('change');
                                //         },450);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputKecamatanPenerima').val('').trigger('change');
                                //         $('#inputDesaPenerima').val('').trigger('change');
                                //         $('#inputKodePosPenerima').val('').trigger('change');
                                //     },650)
                                // } catch(error){}

                                // try {
                                //     $_kecamatan = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kecamatan : 0;
                                //     if($_kecamatan){
                                //         setTimeout(function(){
                                //             $('#inputKecamatanPenerima').val($_kecamatan).trigger('change');
                                //         },700);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputDesaPenerima').val('').trigger('change');
                                //         $('#inputKodePosPenerima').val('').trigger('change');
                                //     },900)
                                // } catch(error){}

                                // try {
                                //     $_desa = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.desa : 0;
                                //     if($_desa){
                                //         setTimeout(function(){
                                //             $('#inputDesaPenerima').val($_desa).trigger('change');
                                //         },950);
                                //     }
                                //     setTimeout(function(){
                                //         $('#inputKodePosPenerima').val('').trigger('change');
                                //     },1150)
                                // } catch(error){}

                                // try {
                                //     $_kodepos = response.data.hasOwnProperty('detail_pelanggan') ? response.data.detail_pelanggan.kode_pos : 0;
                                //     if($_kodepos){
                                //         setTimeout(function(){
                                //             $('#inputKodePosPenerima').val($_kodepos).trigger('change');
                                //         },1200);
                                //     }
                                // } catch(error){}
                                $('#inputProvinsiPenerima').val(response.data.detail_pelanggan.provinsi_id).trigger('change');
                                setTimeout(function(){
                                document.getElementById("select2-inputProvinsiPenerima-container").innerHTML = response.data.detail_pelanggan.provinsi__nama_provinsi;
                                show_kota_list(response.data.detail_pelanggan.provinsi_id, 'Penerima', response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kota__nama_kota);
                                show_kecamatan_list(response.data.detail_pelanggan.kota_id, 'Penerima', response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.kecamatan__nama_kecamatan);
                                show_desa_list(response.data.detail_pelanggan.kecamatan_id, 'Penerima', response.data.detail_pelanggan.desa_id, response.data.detail_pelanggan.desa__nama_desa);
                                show_kode_pos_list(response.data.detail_pelanggan.provinsi_id, response.data.detail_pelanggan.kota_id, response.data.detail_pelanggan.kecamatan_id, response.data.detail_pelanggan.desa_id, 'Penerima', response.data.detail_pelanggan.kode_pos_id, response.data.detail_pelanggan.kode_pos__kode_pos);
                                },200);
                            } catch(error){}
                            
                        }, 500);

                    } catch {
                        setTimeout(function() {
                            // console.log('selected Pelanggan Failed to add in form!');
                            document.getElementById("inputNamaPenerima").value = '';
                            document.getElementById("inputNoTlpPenerima").value = '';
                            document.getElementById("inputAlamatPenerima").value = '';
                        }, 500);

                    }
                }
            });
        }

    });



    // ================================ END Bagian Input penerima ==========================


    // ================================ Bagian Satuan ======================================
    $('#inputSatuan').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_satuan'),
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

    $('#inputLayanan').select2({
        allowClear: true,
        ajax: {
            url: $("#createPengirimanForm").data('url_layanan_select2'),
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




    var url_edit = '';

    function tampilkan_pesan(pesan, type) {
        Toast.fire({
            icon: type,
            title: pesan
        });
    }

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });

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

    var my_token = 'pk.eyJ1IjoiYmhhcnUiLCJhIjoiY2l0dmhxYWcwMDA1cjJ6cW14eHVpaHp4eCJ9.atVtH1bNhN4WgYUrzh0h_g';

    //Basic map
    // DOCUMENTATION https://esri.github.io/esri-leaflet/examples/search-map-service.html

    var mymap = L.map('maps_tracking').setView([-8.652415520702286, 115.21718502044679], 8);
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
        maxZoom: 18,
        id: 'maps_tracking',
        accessToken: my_token
    }).addTo(mymap);

    // $.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=-8.1152&lon=115.0944', function(data){
    //     // console.log(data);
    // });

    var theMarker = {};

    var arcgisOnline = L.esri.Geocoding.arcgisOnlineProvider();

    L.esri.Geocoding.geosearch({
        providers: [
            arcgisOnline,
            L.esri.Geocoding.mapServiceProvider({
                label: 'States and Counties',
                url: 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer',
                layers: [2, 3],
                searchFields: ['NAME', 'STATE_NAME']
            })
        ]
    }).addTo(mymap);

    var markers_rute_1;
    var markers_rute_2;
    var theMarker_rute_1 = [];
    var theMarker_rute_2 = [];
    var marker_lokasi_terkini;

    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    var table = $('#pengiriman').DataTable({
        "columns": [{
                "width": "6%"
            }, {
                "width": "14%"
            }, {
                "width": "14%"
            }, {
                "width": "16%"
            }, {
                "width": "16%"
            },
            null, {
                "width": "18%"
            },
        ],
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
            "url": $("#createPengirimanForm").data('url'),
            "type": "get",
            "data" : params
        }
    });

    var table_arsip = $('#pengiriman_arsip').DataTable({
        "columns": [{
                "width": "6%"
            }, {
                "width": "14%"
            }, {
                "width": "14%"
            }, {
                "width": "16%"
            }, {
                "width": "16%"
            },
            null, {
                "width": "18%"
            },
        ],
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
            "url": $("#createPengirimanForm").data('url_arsip'),
            "type": "get"
        }
    });

    // Function ketika memilih user goverment/company
    var berat__ = '';
    var kilometer__ = '';
    var gudang__ = '';
    var layanan__ = '';
    var penerima__ = '';
    var lain__ = '';
    var pengemasan__ = '';
    var total__ = '';

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
            viewRupiah('inputTarifLain', 'tarifLain');

        }
    }

    function check_if_goverment() {
        var status = document.getElementById("inputStatusPengirim").value;
        var input_harga = document.getElementById("inputTotalTarif");
        input_harga.setAttribute("type", "hidden");
        if (status == 'goverment') {
            document.getElementById("inputTarifBerat").value = '0';
            document.getElementById("inputTarifKilometer").value = '0';
            document.getElementById("inputTarifGudang").value = '0';
            document.getElementById("inputTarifLayanan").value = '0';
            document.getElementById("inputTarifLain").value = '0';
            document.getElementById("inputTotalTarif").value = '0';
            document.getElementById("inputExtraTarifPenerima").value = '0';
            document.getElementById("inputTarifPengemasan").value = '0';

            var input_harga = document.getElementById("inputTotalTarif");
            input_harga.setAttribute("type", "text");

            document.getElementById("rincian_tarif").style.display = "none";
        } else {
            document.getElementById("inputTarifBerat").value = berat__;
            document.getElementById("inputTarifKilometer").value = kilometer__;
            document.getElementById("inputTarifGudang").value = gudang__;
            document.getElementById("inputTarifLayanan").value = layanan__;
            document.getElementById("inputTarifLain").value = lain__;
            document.getElementById("inputTotalTarif").value = total__;
            document.getElementById("inputTarifPengemasan").value = pengemasan__;
            document.getElementById("inputExtraTarifPenerima").value = penerima__;

            viewRupiah('inputTarifBerat', 'tarifBerat');
            viewRupiah('inputTarifKilometer', 'tarifKilometer');
            viewRupiah('inputTarifGudang', 'tarifGudang');
            viewRupiah('inputTarifLayanan', 'tarifLayanan');
            viewRupiah('inputTotalTarif', 'tarifTotal');
            viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
            viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
            viewRupiah('inputTarifLain', 'tarifLain');

            var input_harga = document.getElementById("inputTotalTarif");
            input_harga.setAttribute("type", "hidden");

            document.getElementById("rincian_tarif").style.display = "block";

        }

    }

    //CREATE DATA (SHOW FORM)
    $("#createPengiriman").click(function(e) {
        e.preventDefault();
        $("#createPengirimanForm")[0].reset();
        check_show_rincian();
        var penempatan = $("#createPengirimanForm").data('outlet_id');
        if (penempatan == 'None') {
            tampilkan_pesan("Anda Harus Memiliki Penempatan Outlet!, Pastikan anda sebagai Admin Outlet!", "error");
        } else {
            show_provinsi_list();
            $("#createPengirimanForm")[0].reset();
            $('#inputLayanan').val(null).trigger('change');
            $('#inputPengemasan').val(null).trigger('change');
            document.getElementById('custom-tabs-one-pengirim-tab').click();

            document.getElementById("inputExtraTarifPenerima").value = '';
            document.getElementById("inputTarifKilometer").value = '';
            document.getElementById("inputTotalTarif").value = '';
            document.getElementById("inputTarifBerat").value = '';
            document.getElementById("inputTarifGudang").value = '';
            document.getElementById("inputTarifPengemasan").value = '';
            document.getElementById("inputTarifLain").value = '';

            document.getElementById("tarifBerat").innerHTML = 'Rp. 0';
            document.getElementById("tarifKilometer").innerHTML = 'Rp. 0';
            document.getElementById("tarifGudang").innerHTML = 'Rp. 0';
            document.getElementById("tarifLayanan").innerHTML = 'Rp. 0';
            document.getElementById("tarifTotal").innerHTML = 'Rp. 0';
            document.getElementById("tarifExtraPenerima").innerHTML = 'Rp. 0';
            document.getElementById("tarifLain").innerHTML = 'Rp. 0';

            document.getElementById("inputKotaPengirim").innerHTML = '';
            document.getElementById("inputKecamatanPengirim").innerHTML = '';
            document.getElementById("inputDesaPengirim").innerHTML = '';
            document.getElementById("inputKodePosPengirim").innerHTML = '';
            document.getElementById("tarifPengemasan").innerHTML = 'Rp. 0';

            document.getElementById("inputKotaPenerima").innerHTML = '';
            document.getElementById("inputKecamatanPenerima").innerHTML = '';
            document.getElementById("inputDesaPenerima").innerHTML = '';
            document.getElementById("inputKodePosPenerima").innerHTML = '';
            document.getElementById("inputJumlah").value = '';
            document.getElementById("inputSatuan").innerHTML = '';

            document.getElementById("rute_gudang").innerHTML = '';
            document.getElementById("inputKeteranganExtraTarif").value = '';
            document.getElementById("keterangan").innerHTML = '';

            document.getElementById("status_pengiriman").innerHTML = '';
            document.getElementById("log").innerHTML = '';
            document.getElementById("qrcode").innerHTML = '';

            document.getElementById("updateButton").style.display = "none";
            document.getElementById("createButton").style.display = "block";
            document.getElementById("title_modal").innerHTML = "Tambah Data Pengiriman";
            $("#createPengirimanForm :input").prop("disabled", false);
            document.getElementById("maps_tracking").style.display = "none";
            document.getElementById("maps_tracking").style.height = "0px";
            $('#modal_pengiriman').modal('show');
            try {
                $('#rincian_tarif th a.btn').show();
            } catch(error){}
        };
    });

    var existErrors = false;
    $('a.header[data-toggle="pill"]').on('show.bs.tab', function (e) {
        $element = e;
        $this = this;
        if(!$("#createPengirimanForm").valid()){
            $element.preventDefault();
            // existErrors = true;
            return;
        }
    });


    // CREATE DATA ACTION
    $("#createButton").click(function(e) {
        e.preventDefault();
        // // console.log('BERAT', $('#inputBerat').val());
        if (!$("#createPengirimanForm").valid()) return;
        else if(existErrors){
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            });
    
            Toast.fire({
                icon: 'warning',
                title: 'Pastikan semua data yang dibutuhkan sudah terisi!'
            });
            return
        }
        else if($('#inputBerat').val() == '0' || $('#inputBerat').val() == 0 || $('#inputBerat').val() == null){
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

        var total = $('#inputTotalTarif').val().toString();
        var tagihan = $('#inputTotalTarif').val();
        // console.log(total);

        setTimeout(function(){
            $('#modal_pengiriman').modal('hide');
            $('#id_total_tagihan').val(tagihan);
            $('#total-bayar-text').text(formatRupiah(total, 'Rp. '))
            $('#modal-pos').modal({
                backdrop: 'static',
                keyboard: true,
                show: true
            });
        },500)

        return;
    });

    $('#modal-pos').on('show.bs.modal', function(){
        try{
            $('.nominal_bayar').val('');
        } catch(error){}    
    })

    $('.btn-simpan-pos').click(function(e) {
        e.preventDefault();
        var balance = $('#id_total_kembali').val();
        if(balance < 0){
            try {
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000
                });
    
                Toast.fire({
                    icon: 'warning',
                    title: 'Nominal bayar tidak mencukupi total transaksi'
                });
    
            } catch(error){
                alert('Nominal bayar tidak mencukupi total transaksi')
            }
            return;
        }
        var form_pos = $('#form-pos')[0];
        form_pos = new FormData(form_pos);
        form_pos.delete('id_pengiriman');
        for (var pair of form_pos.entries()) {
            // console.log(pair[0]+ ', ' + pair[1]); 
        }
        $('#modal-pos').modal('hide');

        var serializeData = $("#createPengirimanForm")[0];
        serializeData = new FormData(serializeData);

        $.ajax({
            url: $("#createPengirimanForm").data('url'),
            data: serializeData,
            type: 'post',
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                var response = response;
                // console.log(response);
        
                form_pos.set('id_pengiriman',response.data_pengiriman.id_pengiriman);
                form_pos.set('total_tagihan',response.data_pengiriman.total_tagihan);
                $.ajax({
                    url: '/admin/pengiriman/update/pos',
                    type: 'POST',
                    data: form_pos,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        // console.log(response)
                        try {
                            // try {
                            //     table.ajax.reload();
                            // } catch(error){ // console.log(error) }
                            tampilkan_pesan(response.msg, response.type);
                            setTimeout(function(){
                                location.reload()
                            },400)
                        } catch(error) {
                        // console.log(error)
                        }
                    },
                    error: function(xhr, status, error) {
                        $("#createPengirimanForm")[0].reset();
                        var error_response = xhr.responseJSON;
                        if (error_response) {
                            tampilkan_pesan(error_response.msg, error_response.type);
                        }
                    }
                })
            },
            error: function(xhr, status, error) {
                // $('#modal_pengiriman').modal('hide');
                setTimeout(function() {
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                }, 1000)
                // $("#createPengirimanForm")[0].reset();
            },
        })
    })

    //BAGIAN ARSIP
    $('body').on('click', '.arsipPengiriman', function() {
        var id_pengiriman = $(this).data("id");
        var nama_pengirim = $(this).data("nama");
        Swal.fire({
            title: 'Anda yakin?',
            text: "Yakin Arsipkan Pengiriman ini? " + nama_pengirim + "!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ya, Arsipkan!',
            cancelButtonText: 'Tidak, Batalkan!',
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: id_pengiriman + '/arsip/',
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        id: id_pengiriman
                    },
                    type: 'post',
                    dataType: 'json',
                    success: function(response) {
                        tampilkan_pesan(response.msg, response.type);
                        table.ajax.reload();
                        table_arsip.ajax.reload();
                    },
                    error: function(xhr, status, error) {
                        var error_response = xhr.responseJSON;
                        tampilkan_pesan(error_response.msg, error_response.type);
                    }
                });

            }
        })
    });

    //BAGIAN DELETE
    $('body').on('click', '.deletePengiriman', function() {
        var id_pengiriman = $(this).data("id");
        var nama_pengirim = $(this).data("nama");
        Swal.fire({
            title: 'Anda yakin?',
            text: "Yakin Hapus Pengiriman ini? " + nama_pengirim + "!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ya, Hapus!',
            cancelButtonText: 'Tidak, Batalkan!',
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: id_pengiriman + '/delete/',
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        id: id_pengiriman
                    },
                    type: 'post',
                    dataType: 'json',
                    success: function(response) {
                        tampilkan_pesan(response.msg, response.type);
                        table.ajax.reload();
                        table_arsip.ajax.reload();
                    },
                    error: function(xhr, status, error) {
                        var error_response = xhr.responseJSON;
                        tampilkan_pesan(error_response.msg, error_response.type);
                    }
                });

            }
        })
    });

    //BAGIAN UNARSIP
    $('body').on('click', '.unarsipPengiriman', function() {
        var id_pengiriman = $(this).data("id");
        var nama_pengirim = $(this).data("nama");
        Swal.fire({
            title: 'Anda yakin?',
            text: "Yakin Mengembalikan Pengiriman ini?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ya, Kembalikan!',
            cancelButtonText: 'Tidak, Batalkan!',
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: id_pengiriman + '/unarsip/',
                    data: {
                        csrfmiddlewaretoken: getCookie('csrftoken'),
                        id: id_pengiriman
                    },
                    type: 'post',
                    dataType: 'json',
                    success: function(response) {
                        tampilkan_pesan(response.msg, response.type);
                        table.ajax.reload();
                        table_arsip.ajax.reload();
                    },
                    error: function(xhr, status, error) {
                        var error_response = xhr.responseJSON;
                        tampilkan_pesan(error_response.msg, error_response.type);
                    }
                });

            }
        })
    });

    // DETAIL PENGIRIMAN
    var data_log = [];
    $('body').on('click', '.detailPengiriman', function(event) {
        data_log = [];
        event.preventDefault();
        $("#createPengirimanForm")[0].reset();
        check_show_rincian();
        var pengemasanSelect = $('#inputPengemasan');
        var layananSelect = $('#inputLayanan');
        // $("#loadMe").modal({
        //         backdrop: "static", //remove ability to close modal with click
        //         keyboard: false, //remove option to close with keyboard
        //         show: true //Display loader!
        //     });
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
                document.getElementById('custom-tabs-one-pengirim-tab').click();
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
                document.getElementById("inputSatuan").innerHTML = '<option selected>' + response.data.data_satuan + '</option>';

                setTimeout(function(){
                    // console.log(response.data);
                    document.getElementById("inputTarifBerat").value = response.data.tarif_berat;
                    document.getElementById("inputTarifKilometer").value = response.data.tarif_kilometer;
                    document.getElementById("inputTarifGudang").value = response.data.tarif_gudang;
                    document.getElementById("inputTarifPengemasan").value = response.data.tarif_pengemasan;
                    document.getElementById("inputTarifLayanan").value = response.data.tarif_layanan;
                    document.getElementById("inputTotalTarif").value = response.data.total_tarif;
                    document.getElementById("inputExtraTarifPenerima").value = response.data.extra_tarif_penerima;
                    document.getElementById("inputTarifLain").value = response.data.tarif_lain;

                    document.getElementById("keterangan").innerHTML = response.data.keterangan_extra_tarif;

                    viewRupiah('inputTarifBerat', 'tarifBerat');
                    viewRupiah('inputTarifKilometer', 'tarifKilometer');
                    viewRupiah('inputTarifGudang', 'tarifGudang');
                    viewRupiah('inputTarifLayanan', 'tarifLayanan');
                    viewRupiah('inputTotalTarif', 'tarifTotal');
                    viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
                    viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
                    viewRupiah('inputTarifLain', 'tarifLain');

                },1000)

                /* DISABLE SEMENTARA
                document.getElementById("inputTarifBerat").value = response.data.tarif_berat;
                document.getElementById("inputTarifKilometer").value = response.data.tarif_kilometer;
                document.getElementById("inputTarifGudang").value = response.data.tarif_gudang;
                document.getElementById("inputTarifLayanan").value = response.data.tarif_layanan;
                document.getElementById("inputTotalTarif").value = response.data.total_tarif;
                document.getElementById("inputExtraTarifPenerima").value = response.data.extra_tarif_penerima;
                document.getElementById("keterangan").innerHTML = response.data.keterangan_extra_tarif;

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
                */
               
                var html_rute = '<div class="row"><h4>Rute Pengiriman:</h4><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div>';

                document.getElementById("rute_gudang").innerHTML = html_rute;

                // document.getElementById("status_pengiriman").innerHTML = '<div class="form-group row"><label for="statusPengiriman" class="col-sm-2 col-form-label">Status</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.status.data + '"></div></div><div class="form-group row"><label for="idKurirPengiriman" class="col-sm-2 col-form-label">ID Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.id + '"></div></div><div class="form-group row"><label for="namaKurirPengiriman" class="col-sm-2 col-form-label">Nama Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.nama + '"></div></div><div class="form-group row"><label for="noKurirPengiriman" class="col-sm-2 col-form-label">No. Kurir</label><div class="col-sm-10"><input class="form-control" type="text" disabled value="' + response.kurir.kontak + '"></div></div>';
                // console.log(response);
                document.getElementById("status_pengiriman").innerHTML = '<div class="form-group row"><label for="statusPengiriman" class="col-sm-4 col-form-label">Status</label><div class="col-sm-8"><input class="form-control status-log" type="text" disabled value="' + response.status.data + '"></div></div><div class="form-group row"><label for="namaKurirPengiriman" class="col-sm-4 col-form-label">Discan Oleh</label><div class="col-sm-8"><input class="form-control kurir-nama-log" type="text" disabled value="' + response.kurir.nama + '"></div></div> <div class="form-group row"><label for="penempatanKurir" class="col-sm-4 col-form-label">Penempatan</label><div class="col-sm-8"><input class="form-control penempatan-log" type="text" disabled value="' + response.kurir.penempatan + '"></div></div> <div class="form-group row"><label for="noKurirPengiriman" class="col-sm-4 col-form-label">Telp.</label><div class="col-sm-8"><input class="form-control no-telp-log" type="text" disabled value="' + response.kurir.kontak + '"></div></div>';

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

                var log_activity = '<h4>LOG:</h4><br><table class="table table-bordered table-striped"><thead><tr><th>No</th><th>Tanggal</th><th>Jam</th><th>Status</th></tr></thead><tbody style="height: 100px; overflow-y: auto; overflow-x: hidden;">' + html_log + '</tbody></table>';
                document.getElementById("log").innerHTML = log_activity;

                makeCode(response.data.id_pengiriman);

                document.getElementById("updateButton").style.display = "none";
                document.getElementById("createButton").style.display = "none";
                document.getElementById("createButton").style.display = "none";
                document.getElementById("maps_tracking").style.display = "block";
                document.getElementById("maps_tracking").style.height = "350px";
                document.getElementById("title_modal").innerHTML = "Detail Data Pengiriman";
                $("#createPengirimanForm input").prop("disabled", true);
                $("#createPengirimanForm textarea").prop("disabled", true);
                $("#createPengirimanForm select").prop("disabled", true);

                // $("#loadMe").modal("hide");
                $('#modal_pengiriman').modal('show');
                create_jalur('Pengiriman', response.rute.outlet_1.titik_lokasi, response.rute.gudang_1.titik_lokasi);
                create_jalur('Penerimaan', response.rute.outlet_2.titik_lokasi, response.rute.gudang_2.titik_lokasi);
                show_lokasi_kiriman(response.data.id);

                setTimeout(function() {
                    mymap.invalidateSize()
                }, 400);
                try {
                    $('#rincian_tarif th a.btn').hide();
                } catch(error){}
            },
            error: function(xhr, status, error) {
                // $("#loadMe").modal("hide");
                var error_response = xhr.responseJSON;

                tampilkan_pesan(error_response.msg, error_response.type);
            }
        })

    });

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


    //EDIT DATA SHOW
    $('body').on('click', '.editPengiriman', function(event) {
        event.preventDefault();
        $("#createPengirimanForm")[0].reset();
        var id_pengiriman = $(this).data("id");
        var pengemasanSelect = $('#inputPengemasan');
        var layananSelect = $('#inputLayanan');
        var jenisBarangSelect = $('#inputJenisBarang');
        var satuanSelect = $('#inputSatuan');

        show_provinsi_list();
        url_edit = id_pengiriman + "/update/";
        $.ajax({
            url: id_pengiriman + '/detail/',
            type: 'get',
            success: function(response) {
                document.getElementById('custom-tabs-one-pengirim-tab').click();
                // console.log('EDIT DATA', response)
                show_kota_list(response.data.id_provinsi_pengirim, 'Pengirim', response.data.id_kota_pengirim, response.data.kota_pengirim);
                show_kota_list(response.data.id_provinsi_penerima, 'Penerima', response.data.id_kota_penerima, response.data.kota_penerima);
                show_kecamatan_list(response.data.id_kota_pengirim, 'Pengirim', response.data.id_kecamatan_pengirim, response.data.kecamatan_pengirim);
                show_kecamatan_list(response.data.id_kota_penerima, 'Penerima', response.data.id_kecamatan_penerima, response.data.kecamatan_penerima);
                show_desa_list(response.data.id_kecamatan_pengirim, 'Pengirim', response.data.id_desa_pengirim, response.data.desa_pengirim);
                show_desa_list(response.data.id_kecamatan_penerima, 'Penerima', response.data.id_desa_penerima, response.data.desa_penerima);
                show_kode_pos_list(response.data.id_provinsi_pengirim, response.data.id_kota_pengirim, response.data.id_kecamatan_pengirim, response.data.id_desa_pengirim, 'Pengirim', response.data.id_kode_pos_pengirim, response.data.kode_pos_pengirim);
                show_kode_pos_list(response.data.id_provinsi_penerima, response.data.id_kota_penerima, response.data.id_kecamatan_penerima, response.data.id_desa_penerima, 'Penerima', response.data.id_kode_pos_penerima, response.data.kode_pos_penerima);

                document.getElementById("id_outlet_pengiriman").value = response.data.id_outlet_pengiriman;
                document.getElementById("tampil_outlet_pengiriman").value = response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat;

                // document.getElementById("inputProvinsiPengirim").innerHTML = '<option selected>' + response.data.provinsi_pengirim + '</option>';
                $("#inputProvinsiPengirim").val(response.data.id_provinsi_pengirim);
                document.getElementById("inputKotaPengirim").innerHTML = '<option selected>' + response.data.kota_pengirim + '</option>';
                document.getElementById("inputKecamatanPengirim").innerHTML = '<option selected>' + response.data.kecamatan_pengirim + '</option>';
                document.getElementById("inputDesaPengirim").innerHTML = '<option selected>' + response.data.desa_pengirim + '</option>';
                document.getElementById("inputKodePosPengirim").innerHTML = '<option selected>' + response.data.kode_pos_pengirim + '</option>';
                document.getElementById("select2-inputKodePosPengirim-container").innerHTML = response.data.kode_pos_pengirim;

                // document.getElementById("inputProvinsiPenerima").innerHTML = '<option selected>' + response.data.provinsi_penerima + '</option>';
                $("#inputProvinsiPenerima").val(response.data.id_provinsi_penerima);
                document.getElementById("inputKotaPenerima").innerHTML = '<option selected>' + response.data.kota_penerima + '</option>';
                document.getElementById("inputKecamatanPenerima").innerHTML = '<option selected>' + response.data.kecamatan_penerima + '</option>';
                document.getElementById("inputDesaPenerima").innerHTML = '<option selected>' + response.data.desa_penerima + '</option>';
                document.getElementById("inputKodePosPenerima").innerHTML = '<option selected>' + response.data.kode_pos_penerima + '</option>';
                document.getElementById("select2-inputKodePosPenerima-container").innerHTML = response.data.kode_pos_penerima;


                document.getElementById("inputNamaPengirim").value = response.data.nama_pengirim;
                document.getElementById("inputNoTlpPengirim").value = response.data.no_telp_pengirim;
                // document.getElementById("inputEmailPengirim").value = response.data.email_pengirim;
                document.getElementById("inputAlamatPengirim").value = response.data.alamat_pengirim;

                document.getElementById("inputProvinsiPengirim").value = response.data.id_provinsi_pengirim;
                document.getElementById("select2-inputProvinsiPengirim-container").innerHTML = response.data.provinsi_pengirim;

                document.getElementById("inputJumlah").value = response.data.jumlah;
                // document.getElementById("inputSatuan").value = response.data.id_satuan;
                // document.getElementById("select2-inputSatuan-container").innerHTML = response.data.data_satuan;
                var option_satuan = new Option(response.data.data_satuan, response.data.id_satuan, true, true);
                satuanSelect.append(option_satuan).trigger('change');

                document.getElementById("inputNamaPenerima").value = response.data.nama_penerima;
                document.getElementById("inputNoTlpPenerima").value = response.data.no_telp_penerima;
                // document.getElementById("inputEmailPenerima").value = response.data.email_penerima;
                document.getElementById("inputAlamatPenerima").value = response.data.alamat_penerima;

                document.getElementById("inputProvinsiPenerima").value = response.data.id_provinsi_penerima;
                document.getElementById("select2-inputProvinsiPenerima-container").innerHTML = response.data.provinsi_penerima;

                // document.getElementById("inputOutletPengiriman").value = response.data.id_outlet_pengiriman;
                document.getElementById("inputOutletPenerimaan").value = response.data.id_outlet_penerimaan;
                document.getElementById("inputGudang1").value = response.rute.gudang_1.id;
                document.getElementById("inputGudangPengiriman").value = response.rute.gudang_1.id;
                document.getElementById("inputGudang2").value = response.rute.gudang_2.id;
                document.getElementById("inputGudangPenerimaan").value = response.rute.gudang_2.id;
                document.getElementById("id_pengiriman").value = response.data.id_pengiriman;


                document.getElementById("pencatat").value = response.data.id_pencatat;
                // document.getElementById("inputJenisBarang").value = response.data.jenis_barang_id;
                // $('#inputJenisBarang').val(response.data.jenis_barang_id).trigger('change');
                // document.getElementById("select2-inputJenisBarang-container").innerHTML = response.data.jenis_barang;
                // $('#inputJenisBarang').select2('data', {id: response.data.jenis_barang_id, text: response.data.jenis_barang});
                var option_jenisBarang = new Option(response.data.jenis_barang, response.data.jenis_barang_id, true, true);
                jenisBarangSelect.append(option_jenisBarang).trigger('change');

                // $("#inputJenisBarang").select2('destroy');
                // $("#inputJenisBarang").val(response.data.jenis_barang);
                // $("#inputJenisBarang").select2();
                
                document.getElementById("inputDetailBarang").value = response.data.detail_barang;
                // document.getElementById("inputPengemasan").value = response.data.id_pengemasan;
                // document.getElementById("select2-inputPengemasan-container").innerHTML = response.data.pengemasan;
                var option = new Option(response.data.pengemasan, response.data.id_pengemasan, true, true);
                pengemasanSelect.append(option).trigger('change');

                // document.getElementById("inputLayanan").value = response.data.id_layanan;
                // document.getElementById("select2-inputLayanan-container").innerHTML = response.data.layanan;

                var option_layanan = new Option(response.data.layanan, response.data.id_layanan, true, true);
                layananSelect.append(option_layanan).trigger('change');

                setTimeout(function(){
                    document.getElementById("inputBerat").value = response.data.berat;
                    document.getElementById("inputTarifBerat").value = response.data.tarif_berat;
                    document.getElementById("inputTarifKilometer").value = response.data.tarif_kilometer;
                    document.getElementById("inputTarifGudang").value = response.data.tarif_gudang;
                    document.getElementById("inputTarifPengemasan").value = response.data.tarif_pengemasan;
                    document.getElementById("inputTarifLayanan").value = response.data.tarif_layanan;
                    document.getElementById("inputTotalTarif").value = response.data.total_tarif;
                    document.getElementById("inputExtraTarifPenerima").value = response.data.extra_tarif_penerima;
                    document.getElementById("inputTarifLain").value = response.data.tarif_lain;
                    document.getElementById("keterangan").innerHTML = response.data.keterangan_extra_tarif;

                    viewRupiah('inputTarifBerat', 'tarifBerat');
                    viewRupiah('inputTarifKilometer', 'tarifKilometer');
                    viewRupiah('inputTarifGudang', 'tarifGudang');
                    viewRupiah('inputTarifLayanan', 'tarifLayanan');
                    viewRupiah('inputTotalTarif', 'tarifTotal');
                    viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
                    viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
                    viewRupiah('inputTarifLain', 'tarifLain');

                },1000)

                var html_rute = '<div class="row"><h4>Rute Pengiriman:</h4><div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #1</span> ' + response.rute.outlet_1.nama + ' | Alamat: ' + response.rute.outlet_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_1.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #1</span> ' + response.rute.gudang_1.nama + ' | Alamat: ' + response.rute.gudang_1.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.gudang_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-warning">Gudang #2</span> ' + response.rute.gudang_2.nama + ' | Alamat: ' + response.rute.gudang_2.alamat + '</small></p></div>';

                html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + response.rute.outlet_2.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Outlet #2</span> ' + response.rute.outlet_2.nama + ' | Alamat: ' + response.rute.outlet_2.alamat + '</small></p></div>';

                document.getElementById("rute_gudang").innerHTML = html_rute;

                document.getElementById("status_pengiriman").innerHTML = '';

                var html_log = '';
                for (var i = 0; i < response.log.length; i++) {

                    var date_time = response.log[i].created_at;
                    var dateTime = date_time.split("T");
                    var date = dateTime[0];
                    var time = dateTime[1].split(".");

                    html_log = html_log + '<tr><td>' + (i + 1) + '</td> <td>' + date + '</td> <td>' + time[0] + '</td> <td>' + response.log[i].status_pengiriman + '</td></tr>';
                }

                var log_activity = '<h4>LOG:</h4><br><table class="table table-bordered table-striped"><thead><tr><th>No</th><th>Tanggal</th><th>Jam</th><th>Status</th></tr></thead><tbody style="height: 100px; overflow-y: auto; overflow-x: hidden;">' + html_log + '</tbody></table>';
                document.getElementById("log").innerHTML = log_activity;

                makeCode(response.data.id_pengiriman);

                document.getElementById("updateButton").style.display = "block";
                document.getElementById("createButton").style.display = "none";
                document.getElementById("maps_tracking").style.display = "none";
                document.getElementById("maps_tracking").style.height = "0px";
                document.getElementById("title_modal").innerHTML = "Edit Data Pengiriman";
                $("#createPengirimanForm :input").prop("disabled", false);
                // $("#loadMe").modal("hide");
                $('#modal_pengiriman').modal('show');
                try {
                    $('#rincian_tarif th a.btn').show();
                } catch(error){}
            },
            error: function(xhr, status, error) {
                // $("#loadMe").modal("hide");
                var error_response = xhr.responseJSON;
                if (error_response) {
                    tampilkan_pesan(error_response.msg, error_response.type);
                }
            }
        })

    });


    // Update action
    $("#updateButton").click(function(e) {
        e.preventDefault();
        var serializeData = $("#createPengirimanForm").serialize();
        // url_edit = id_pengiriman + "/update/";

        $.ajax({
            url: url_edit,
            data: serializeData,
            type: 'POST',
            cache: false,
            success: function(response) {
                table.ajax.reload();
                $('#modal_pengiriman').modal('hide');
                tampilkan_pesan(response.msg, response.type);
                $("#createPengirimanForm")[0].reset();
            },
            error: function(xhr, status, error) {
                // console.log(xhr);
                var error_response = xhr.responseJSON;
                if (error_response) {
                    tampilkan_pesan(error_response.msg, error_response.type);
                }
            },
        })


    });

    // DOWNLOAD BILLING
    $('body').on('click', '.downloadLabel', function(event) {
        event.preventDefault();
        var id_pengiriman = $(this).data("id");

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        var url_image = $("#createPengirimanForm").data('url_image');
        var url_qrcode = $("#createPengirimanForm").data('url_qrcode');
        var url_custom_billing = $("#createPengirimanForm").data('url_custom_billing');
        today = mm + '/' + dd + '/' + yyyy;

        function wait(ms) {
            var start = new Date().getTime();
            var end = start;
            while (end < start + ms) {
                end = new Date().getTime();
            }
        }

        var printWindow;

        $.ajax({
            url: id_pengiriman + '/detail/',
            type: 'get',
            success: function(response) {

                printWindow = window.open('', '', 'height=450,width=600');
                printWindow.document.write('<html><head><title>DATA Pengiriman - ' + response.data.id_pengiriman + '</title>');
                printWindow.document.write('<style id="style_billing">.invoice-box {max-width: 490px;margin: auto;padding: 20px;border: 1px solid #eee;box-shadow: 0 0 5px rgba(0, 0, 0, .15);font-size: 9px;line-height: 10px;font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;color: #555;}.invoice-box table {width: 100%;line-height: inherit;text-align: left;}.invoice-box table td {padding: 2px;vertical-align: top;}.invoice-box table tr td:nth-child(2) {text-align: right;}.invoice-box table tr.top table td {padding-bottom: 5px;}.invoice-box table tr.top table td.title {font-size: 20px;line-height: 20px;color: #333;}.invoice-box table tr.information table td {padding-bottom: 10px;}.invoice-box table tr.heading td {background: #eee;border-bottom: 1px solid #ddd;font-weight: bold;}.invoice-box table tr.details td {padding-bottom: 20px;}.invoice-box table tr.item td{border-bottom: 1px solid #eee;}.invoice-box table tr.item.last td {border-bottom: none;}.invoice-box table tr.total td:nth-child(2) {border-top: 1px solid #eee;font-weight: bold;}@media only screen and (max-width: 600px) {.invoice-box table tr.top table td {width: 100%;display: block;text-align: center;}.invoice-box table tr.information table td {width: 100%;display: block;text-align: right;}}.rtl {direction: rtl;font-family: Tahoma, "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;}.rtl table {text-align: right;}.rtl table tr td:nth-child(2) {text-align: left;}</style>');
                printWindow.document.write('</head><body >');
                printWindow.document.write('<div class="invoice-box">');
                printWindow.document.write('<table style="height: 69px; width: 435px;" width="276">');
                printWindow.document.write('<tbody>');
                printWindow.document.write('<tr style="border-style: solid;">');
                printWindow.document.write('<td style="width: 254.017px;">Resi: ' + response.data.id_pengiriman + '<p style="font-size: 8px;">Created: ' + today + '<br />Tgl Input: ' + response.data.created_at + '</p></td>');
                printWindow.document.write('<td style="width: 164.983px;"><img src="' + url_image + '" alt="" width="181" height="42" /></td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('</tbody>');
                printWindow.document.write('</table>');
                printWindow.document.write('<table style="height: 55px; width: 435px;" width="435">');
                printWindow.document.write('<tbody>');
                printWindow.document.write('<tr class="heading" style="height: 11px;">');
                printWindow.document.write('<td style="font-size: 9px; height: 11px; width: 74.1833px;"><strong>Data Pengirim</strong></td>');
                printWindow.document.write('<td style="font-size: 9px; width: 9.03333px; height: 11px;">&nbsp;</td>');
                printWindow.document.write('<td style="font-size: 9px; height: 11px; width: 238.567px;">&nbsp;</td>');
                printWindow.document.write('<td id="qr_print" style="font-size: 9px; width: 85.2167px; height: 55px;" rowspan="5"></td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr style="height: 11px;">');
                printWindow.document.write('<td style="font-size: 9px; height: 11px; width: 74.1833px;">Nama</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 9.03333px; height: 11px;">:</td>');
                printWindow.document.write('<td style="font-size: 9px; height: 11px; width: 238.567px;">' + response.data.nama_pengirim + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr style="height: 11px;">');
                printWindow.document.write('<td style="font-size: 9px; width: 74.1833px; height: 11px;">No.Tlp</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 9.03333px; height: 11px;">:</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 238.567px; height: 11px;">' + response.data.no_telp_pengirim + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr style="height: 11px;">');
                printWindow.document.write('<td style="font-size: 9px; width: 74.1833px; height: 11px;">Alamat</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 9.03333px; height: 11px;">:</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 238.567px; height: 11px;">' + response.data.alamat_pengirim + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr style="height: 11px;">');
                printWindow.document.write('<td style="font-size: 9px; width: 74.1833px; height: 11px;"><strong>Pengiriman</strong></td>');
                printWindow.document.write('<td style="font-size: 9px; width: 9.03333px; height: 11px;">:</td>');
                printWindow.document.write('<td style="font-size: 9px; width: 238.567px; height: 11px;">' + response.data.layanan + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('</tbody>');
                printWindow.document.write('</table>');
                printWindow.document.write('<table style="width: 436px; height: 90px;">');
                printWindow.document.write('<tbody>');
                printWindow.document.write('<tr class="heading" style="height: 18px; background-color: #2ecc71;">');
                printWindow.document.write('<td style="width: 146.35px; height: 18px;"><strong>DETAIL TUJUAN</strong></td>');
                printWindow.document.write('<td style="width: 10.0333px; height: 18px;"><strong>&nbsp;</strong></td>');
                printWindow.document.write('<td style="width: 257.617px; height: 18px; text-align: right;"><strong>DATA</strong></td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr class="item" style="height: 18px;">');
                printWindow.document.write('<td style="width: 146.35px; height: 18px;">Nama</td>');
                printWindow.document.write('<td style="width: 10.0333px; height: 18px;">:</td>');
                printWindow.document.write('<td style="width: 257.617px; height: 18px;">' + response.data.nama_penerima + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr class="item" style="height: 18px;">');
                printWindow.document.write('<td style="width: 146.35px; height: 18px;">Alamat</td>');
                printWindow.document.write('<td style="width: 10.0333px; height: 18px;">:</td>');
                printWindow.document.write('<td style="width: 257.617px; height: 18px;">' + response.data.alamat_penerima + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr class="item" style="height: 18px;">');
                printWindow.document.write('<td style="width: 146.35px; height: 18px;">No. Tlp</td>');
                printWindow.document.write('<td style="width: 10.0333px; height: 18px;">:</td>');
                printWindow.document.write('<td style="width: 257.617px; height: 18px;">' + response.data.no_telp_penerima + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('<tr class="item" style="height: 18px;">');
                printWindow.document.write('<td style="width: 146.35px; height: 18px;">Email</td>');
                printWindow.document.write('<td style="width: 10.0333px; height: 18px;">:</td>');
                printWindow.document.write('<td style="width: 257.617px; height: 18px;">' + response.data.email_penerima + '</td>');
                printWindow.document.write('</tr>');
                printWindow.document.write('</tbody>');
                printWindow.document.write('</table>');
                printWindow.document.write('</div>');

                printWindow.document.write('<script type="text/javascript" src="' + url_qrcode + '"></script><script type="text/javascript" src="' + url_custom_billing + '"></script><script>makeCodeQR("' + response.data.id_pengiriman + '")</script></body></html>');
                printWindow.document.close();

            },
            done: function() {
                printWindow.print();
            },

        })
    });


    $('#modal_pengiriman').on('hide.bs.modal', function() {
        setTimeout(function() {
            var validator = $("#createPengirimanForm").validate();
            validator.resetForm();

        })
    });

    var alamat_pengirim;
    var alamat_penerima;
    var lokasi_pengirim;
    var lokasi_penerima;

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

    function hitung_total() {
        var t_layanan = document.getElementById("inputTarifLayanan").value;
        var t_berat = document.getElementById("inputTarifBerat").value;
        var t_kilometer = document.getElementById("inputTarifKilometer").value;
        var t_gudang = document.getElementById("inputTarifGudang").value;
        var t_pengemasan = document.getElementById("inputTarifPengemasan").value;
        var t_extra_cash = document.getElementById("inputExtraTarifPenerima").value;
        var t_lain = document.getElementById("inputTarifLain").value;

        berat__ = t_berat;
        kilometer__ = t_kilometer;
        gudang__ = t_gudang;
        layanan__ = t_layanan;
        penerima__ = t_extra_cash;
        pengemasan__ = t_pengemasan;
        lain__ = t_lain;

        var n_layanan = str2int(t_layanan);
        var n_berat = str2int(t_berat);
        var n_kilometer = str2int(t_kilometer);
        var n_gudang = str2int(t_gudang);
        var n_pengemasan = str2int(t_pengemasan);
        var n_extra_cash = str2int(t_extra_cash);
        var n_lain = str2int(t_lain);

        var total_tarif = n_layanan + n_berat + n_kilometer + n_gudang + n_pengemasan + n_extra_cash + n_lain;
        total__ = total_tarif;
        // console.log(n_layanan);

        check_if_goverment();

        document.getElementById("inputTotalTarif").value = total_tarif;
        // document.getElementById("tarifTotal").innerHTML = 'Rp. ' + total_tarif;
        viewRupiah('inputTotalTarif', 'tarifTotal');

    }

    function show_list_toko() {
        $.ajax({
            type: "POST",
            url: $("#createPengirimanForm").data('url_toko'),
            success: function(response) {
                // $("select#inputOutletPengiriman").html(response.data);
                $("select#inputOutletPenerimaan").html(response.data);
            }
        });
    }

    function show_kota_list(id_provinsi, pengirim_penerima, id_kota_select, nama_kota) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinsi + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinsi
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputKota" + pengirim_penerima).html(response.data);
                document.getElementById("inputKota" + pengirim_penerima).value = id_kota_select;
                document.getElementById("select2-inputKota" + pengirim_penerima + "-container").innerHTML = nama_kota;
            }
        });
    }

    function show_kecamatan_list(id_kota, pengirim_penerima, id_kecamatan_select, nama_kecamatan) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputKecamatan" + pengirim_penerima).html(response.data);
                document.getElementById("inputKecamatan" + pengirim_penerima).value = id_kecamatan_select;
                document.getElementById("select2-inputKecamatan" + pengirim_penerima + "-container").innerHTML = nama_kecamatan;
            }
        });
    }

    function show_desa_list(id_kecamatan, pengirim_penerima, id_desa_select, nama_desa) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputDesa" + pengirim_penerima).html(response.data);
                document.getElementById("inputDesa" + pengirim_penerima).value = id_desa_select;
                document.getElementById("select2-inputDesa" + pengirim_penerima + "-container").innerHTML = nama_desa;
            }
        });
    }

    function show_kode_pos_list(id_provinces, id_kota, id_kecamatan, id_desa, pengirim_penerima, id_kode_pos_select, kode_pos) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputKodePos" + pengirim_penerima).html(response.data);
                document.getElementById("inputKodePos" + pengirim_penerima).value = id_kode_pos_select;
                document.getElementById("select2-inputKodePos" + pengirim_penerima + "-container").innerHTML = kode_pos;
            }
        });
    }


    function show_provinsi_list() {
        $.ajax({
            type: "POST",
            url: $("#createPengirimanForm").data('url_provinsi'),
            success: function(response) {
                $("select#inputProvinsiPengirim").html(response.data);
                $("select#inputProvinsiPenerima").html(response.data);
            }
        });
    }

    show_provinsi_list();
    // show_list_toko();

    $("#inputProvinsiPengirim").change(function() {
        var id_provinces = $(this).val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinces + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputKotaPengirim").html(response.data);
                getAjaxKota_pengirim();
            }
        });
    });

    $("#inputProvinsiPenerima").change(function() {
        var id_provinces = $(this).val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinces + '/kota/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces
            },

            success: function(response) {
                // // console.log(response.data);
                $("select#inputKotaPenerima").html(response.data);
                getAjaxKota_penerima();
            }
        });
    });

    $("#inputKotaPengirim").change(getAjaxKota_pengirim);
    $("#inputKotaPenerima").change(getAjaxKota_penerima);

    function getAjaxKota_pengirim() {
        var id_kota = $("#inputKotaPengirim").val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },
            success: function(response) {
                $("select#inputKecamatanPengirim").html(response.data);
                getAjaxKecamatan_pengirim();
            }
        });
    }

    function getAjaxKota_penerima() {
        var id_kota = $("#inputKotaPenerima").val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kota + '/kecamatan/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kota_id: id_kota
            },
            success: function(response) {
                $("select#inputKecamatanPenerima").html(response.data);
                getAjaxKecamatan_penerima();
            }
        });
    }

    $("#inputKecamatanPengirim").change(getAjaxKecamatan_pengirim);
    $("#inputKecamatanPenerima").change(getAjaxKecamatan_penerima);

    function getAjaxKecamatan_pengirim() {
        var id_kecamatan = $("#inputKecamatanPengirim").val();
        alamat_pengirim = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },
            success: function(response) {
                $("select#inputDesaPengirim").html(response.data);
                getAjaxDesa_pengirim();
            }
        });
    }

    function getAjaxKecamatan_penerima() {
        var id_kecamatan = $("#inputKecamatanPenerima").val();
        alamat_penerima = "";
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_kecamatan + '/desa/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                kecamatan_id: id_kecamatan
            },
            success: function(response) {
                $("select#inputDesaPenerima").html(response.data);
                getAjaxDesa_penerima();
            }
        });
    }

    $("#inputDesaPengirim").change(getAjaxDesa_pengirim);
    $("#inputDesaPenerima").change(getAjaxDesa_penerima);

    function getAjaxDesa_pengirim() {
        var id_provinces = $("#inputProvinsiPengirim").val();
        var id_kota = $("#inputKotaPengirim").val();
        var id_kecamatan = $("#inputKecamatanPengirim").val();
        var id_desa = $("#inputDesaPengirim").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },
            success: function(response) {
                $("select#inputKodePosPengirim").html(response.data);
                alamat_pengirim = getSelectedText('inputDesaPengirim');
                alamat_pengirim += ", " + getSelectedText('inputKecamatanPengirim');
                alamat_pengirim += ", " + getSelectedText('inputKotaPengirim');
                alamat_pengirim += ", " + getSelectedText('inputProvinsiPengirim');
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
        var id_provinces = $("#inputProvinsiPenerima").val();
        var id_kota = $("#inputKotaPenerima").val();
        var id_kecamatan = $("#inputKecamatanPenerima").val();
        var id_desa = $("#inputDesaPenerima").val();
        $.ajax({
            type: "POST",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_provinsi') + id_provinces + '/' + id_kota + '/' + id_kecamatan + '/' + id_desa + '/kode/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                provinsi_id: id_provinces,
                kota_id: id_kota,
                kecamatan_id: id_kecamatan,
                desa_id: id_desa
            },
            success: function(response) {
                $("select#inputKodePosPenerima").html(response.data);
                alamat_penerima = getSelectedText('inputDesaPenerima');
                alamat_penerima += ", " + getSelectedText('inputKecamatanPenerima');
                alamat_penerima += ", " + getSelectedText('inputKotaPenerima');
                alamat_penerima += ", " + getSelectedText('inputProvinsiPenerima');
                // // console.log(alamat_penerima);
                if (alamat_pengirim && alamat_penerima) {
                    // // console.log(alamat_penerima);
                    // // console.log(alamat_pengirim);
                    get_loc_degree(alamat_pengirim, alamat_penerima);
                }

            }
        });
    }




    // ============================= HITUNG TARIF LAYANAN ====================================
    $("#inputLayanan").change(function() {
        var id_layanan = $(this).val();
        if (!id_layanan) {
            id_layanan = 0;
        }
        $.ajax({
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_layanan') + id_layanan + '/harga/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                id_layanan: id_layanan
            },

            success: function(response) {
                // // console.log(response.data);
                document.getElementById("inputTarifLayanan").value = response.harga;
                // document.getElementById("tarifLayanan").innerHTML = 'Rp. ' + response.harga;
                viewRupiah('inputTarifLayanan', 'tarifLayanan');
            }
        }).done(function() {
            hitung_total();
        });

    });

    // ============================= HITUNG TARIF PENGEMASAN ====================================
    $("#inputPengemasan").change(function() {
        var id_pengemasan = $(this).val();
        // console.log("id_pengemasan", id_pengemasan);
        if (!id_pengemasan) {
            id_pengemasan = 0;
        }
        if (id_pengemasan && id_pengemasan != 0) {
            // console.log('ajax call')
            $.ajax({
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createPengirimanForm").data('url_detail_pengemasan') + 'detail/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id: id_pengemasan
                },
                success: function(response) {
                    // // console.log("PENGEMASAN", response);
                    document.getElementById("inputTarifPengemasan").value = response.data.tarif;
                    // document.getElementById("tarifPengemasan").innerHTML = 'Rp. ' + response.data.tarif;
                    viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
                }
            }).done(function() {
                hitung_total();
            });
        }
        else {
            document.getElementById("inputTarifPengemasan").value = 0;
            viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
            hitung_total();
        }
    });

    // ============================= HITUNG TARIF Berat ====================================
    inputBerat.oninput = function() {
        var berat = $(this).val();
        setTimeout(function(){
            // console.log('BERAT KONVERSI');
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
                    $("#inputBerat").prop('disabled', true);
                    $("#inputBerat").val(berat);
                } catch(error){}
            },800)

            setTimeout(function(){
                $("#inputBerat").prop('disabled', false);
                hitung_berat_input(berat);
            },1000)
        },100)

    };

    function hitung_berat_input(berat_input) {
        var berat = berat_input;
        if (!berat) {
            berat = 0;
        }
        $.ajax({
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_berat') + berat + '/harga/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                berat: berat
            },

            success: function(response) {
                // // console.log(response.data);
                document.getElementById("inputTarifBerat").value = response.harga;
                document.getElementById("tarifBerat").innerHTML = 'Rp. ' + response.harga;
                viewRupiah('inputTarifBerat', 'tarifBerat');
            }
        }).done(function() {
            hitung_total();
        });

    };

    // ============================= HITUNG TARIF KILOMETER & Gudang ====================================
    var lat_pengirim;
    var lon_pengirim;
    var api_key = $("#createPengirimanForm").data('api_open_route_service'); //API OPENROUTESERVICE
    // https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf62486f09c07e222343b09d62cf8daadf701d&start=115.18286043300274,%20-8.648084101228674&end=115.19248114543201,%20-8.655464920602416
    function jarak_in_two_point(lat1, lon1, lat2, lon2) {
        var url_api = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + lon1 + "," + lat1 + "&end=" + lon2 + "," + lat2;

        $.ajax({
                type: "GET",
                url: url_api,
                success: function(data) {
                    // console.log("jarak_in_two_point_HASIL_", data)
                    data_pengirim = data.features[0].geometry.coordinates;
                    // console.log("Sukses Ambil data pengirim");
                }
            })
            .done(function() {

            });
    }

    function clear_rute_gudang() {
        document.getElementById('rute_gudang').innerHTML = "";
    }


    async function get_loc_degree(alamat_pengirim, alamat_penerima) {
        try{
            var url_api_geo = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=";
            var extra_cash_pengirim = 'Tidak Kena';
            var extra_cash_penerima = 'Tidak Kena';

            var t_arr = alamat_pengirim.split(',');
            var r_arr = alamat_penerima.split(',');

            var loc_pengirim;
            var loc_penerima;

            //fetch all gudang
            const response_gudang = await fetch($("#createPengirimanForm").data('url_gudang'));
            const data_gudang = await response_gudang.json();
            var gudangs = data_gudang.data;
            // console.log("ALAMAT PENGIRIM", alamat_pengirim);
            // console.log("ALAMAT PENERIMA", alamat_penerima);


            //Pencarian Titik Lokasi Untuk Pengirim
            // const T_response_1 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[0].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
            const T_response_1 = await fetch(url_api_geo + alamat_pengirim + "&boundary.country=IDN&size=1");
            const data_pengirim = await T_response_1.json();
            // console.log("ALAMAT PENGIRIM API", data_pengirim);
            if (data_pengirim.features.length <= 0) {
                const T_response_2 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[2].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
                const data_pengirim = await T_response_2.json();
                if (data_pengirim.features.length <= 0) {
                    const T_response_3 = await fetch(url_api_geo + t_arr[2].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
                    const data_pengirim = await T_response_3.json();
                    if (data_pengirim.features.length <= 0) {
                        const T_response_4 = await fetch(url_api_geo + t_arr[3].trim() + "&boundary.country=IDN&size=1");
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
            // const R_response_1 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[0].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1");
            const R_response_1 = await fetch(url_api_geo + alamat_penerima + "&boundary.country=IDN&size=1");
            const data_penerima = await R_response_1.json();
            // console.log("ALAMAT PENERIMA API", data_penerima);
            if (data_penerima.features.length <= 0) {
                const R_response_2 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[2].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1");
                const data_penerima = await R_response_2.json();
                if (data_penerima.features.length <= 0) {
                    const R_response_3 = await fetch(url_api_geo + r_arr[2].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1N");
                    const data_penerima = await R_response_3.json();
                    if (data_penerima.features.length <= 0) {
                        const R_response_4 = await fetch(url_api_geo + r_arr[3].trim() + "&boundary.country=IDN&size=1");
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
            if (extra_cash_penerima != 'Tidak Kena') {
                const response_extra_cash_penerima = await fetch($("#createPengirimanForm").data('url_extra_cash') + '?wilayah=' + extra_cash_penerima);
                const data_ec_penerima = await response_extra_cash_penerima.json();
                document.getElementById("inputExtraTarifPenerima").value = data_ec_penerima.harga;
                viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
                html_keterangan += 'Alamat Penerima Paket Kena Extra Cash (' + data_ec_penerima.wilayah + ')';
            } else {
                html_keterangan += 'Alamat Penerima Tidak Kena Extra Cash';
                document.getElementById("inputExtraTarifPenerima").value = '';
            }
            document.getElementById("inputKeteranganExtraTarif").value = html_keterangan;
            document.getElementById("keterangan").innerHTML = html_keterangan;

            // console.log("LOKASI PENGIRIM", loc_pengirim);
            // console.log("LOKASI PENERIMA", loc_penerima);
            // Tidak Perlu karena paket dikirimkan dari outlet

            // if(extra_cash_pengirim != 'Tidak Kena'){
            //     const response_extra_cash_pengirim = await fetch($("#createPengirimanForm").data('url_extra_cash')+'?wilayah='+extra_cash_pengirim);
            //     const data_ec_pengirim = await response_extra_cash_pengirim.json();
            //     document.getElementById("inputExtraTarifPenerima").value = data_ec_pengirim.harga;
            //     viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
            // }
            // clear_rute_gudang();
            // console.log('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima);
            tampilkan_pesan('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima, 'info');

            outlet_dan_gudang_yang_dilalui_2(gudangs, loc_penerima, loc_pengirim, t_arr[0], r_arr[0]);
        } catch (e) {
            tampilkan_pesan(e.message + ", please check connection and refresh", 'error');
            return;
        } 
    }


    async function get_loc_degree2(alamat_pengirim, alamat_penerima) {
        var data_penerima;
        var data_pengirim;
        var data_gudang;

        var url_geocode_1 = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=" + alamat_pengirim + "&size=1&country=IDN";
        var url_geocode_2 = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=" + alamat_penerima + "&size=1&country=IDN";
        // console.log(alamat_penerima);
        $.ajax({
                type: "GET",
                url: $("#createPengirimanForm").data('url_gudang'),
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
                                // outlet_dan_gudang_yang_dilalui(data_gudang, data_penerima, data_pengirim);
                                var t_arr = alamat_pengirim.split(',');
                                var r_arr = alamat_penerima.split(',');
                                outlet_dan_gudang_yang_dilalui_2(data_gudang, data_penerima, data_pengirim, t_arr[0], r_arr[0]);

                            });
                    });
            });
    }

    async function get_loc_degree_manual(alamat_pengirim, alamat_penerima) {
        try{
            var url_api_geo = "https://api.openrouteservice.org/geocode/search?api_key=" + api_key + "&text=";
            var extra_cash_pengirim = 'Tidak Kena';
            var extra_cash_penerima = 'Tidak Kena';

            var t_arr = alamat_pengirim.split(',');
            var r_arr = alamat_penerima.split(',');

            var loc_pengirim;
            var loc_penerima;

            //fetch all gudang
            const response_gudang = await fetch($("#createPengirimanForm").data('url_gudang'));
            const data_gudang = await response_gudang.json();
            var gudangs = data_gudang.data;
            // console.log("ALAMAT PENGIRIM", alamat_pengirim);
            // console.log("ALAMAT PENERIMA", alamat_penerima);


            //Pencarian Titik Lokasi Untuk Pengirim
            // const T_response_1 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[0].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
            const T_response_1 = await fetch(url_api_geo + alamat_pengirim + "&boundary.country=IDN&size=1");
            const data_pengirim = await T_response_1.json();
            // console.log("ALAMAT PENGIRIM API", data_pengirim);
            if (data_pengirim.features.length <= 0) {
                const T_response_2 = await fetch(url_api_geo + t_arr[1].trim() + ',' + t_arr[2].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
                const data_pengirim = await T_response_2.json();
                if (data_pengirim.features.length <= 0) {
                    const T_response_3 = await fetch(url_api_geo + t_arr[2].trim() + ',' + t_arr[3].trim() + "&boundary.country=IDN&size=1");
                    const data_pengirim = await T_response_3.json();
                    if (data_pengirim.features.length <= 0) {
                        const T_response_4 = await fetch(url_api_geo + t_arr[3].trim() + "&boundary.country=IDN&size=1");
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
            // const R_response_1 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[0].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1");
            const R_response_1 = await fetch(url_api_geo + alamat_penerima + "&boundary.country=IDN&size=1");
            const data_penerima = await R_response_1.json();
            // console.log("ALAMAT PENERIMA API", data_penerima);
            if (data_penerima.features.length <= 0) {
                const R_response_2 = await fetch(url_api_geo + r_arr[1].trim() + ',' + r_arr[2].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1");
                const data_penerima = await R_response_2.json();
                if (data_penerima.features.length <= 0) {
                    const R_response_3 = await fetch(url_api_geo + r_arr[2].trim() + ',' + r_arr[3].trim() + "&boundary.country=IDN&size=1N");
                    const data_penerima = await R_response_3.json();
                    if (data_penerima.features.length <= 0) {
                        const R_response_4 = await fetch(url_api_geo + r_arr[3].trim() + "&boundary.country=IDN&size=1");
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
            if (extra_cash_penerima != 'Tidak Kena') {
                const response_extra_cash_penerima = await fetch($("#createPengirimanForm").data('url_extra_cash') + '?wilayah=' + extra_cash_penerima);
                const data_ec_penerima = await response_extra_cash_penerima.json();
                document.getElementById("inputExtraTarifPenerima").value = data_ec_penerima.harga;
                viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
                html_keterangan += 'Alamat Penerima Paket Kena Extra Cash (' + data_ec_penerima.wilayah + ')';
            } else {
                html_keterangan += 'Alamat Penerima Tidak Kena Extra Cash';
                document.getElementById("inputExtraTarifPenerima").value = '';
            }
            document.getElementById("inputKeteranganExtraTarif").value = html_keterangan;
            document.getElementById("keterangan").innerHTML = html_keterangan;

            // console.log("LOKASI PENGIRIM", loc_pengirim);
            // console.log("LOKASI PENERIMA", loc_penerima);
            // Tidak Perlu karena paket dikirimkan dari outlet

            // if(extra_cash_pengirim != 'Tidak Kena'){
            //     const response_extra_cash_pengirim = await fetch($("#createPengirimanForm").data('url_extra_cash')+'?wilayah='+extra_cash_pengirim);
            //     const data_ec_pengirim = await response_extra_cash_pengirim.json();
            //     document.getElementById("inputExtraTarifPenerima").value = data_ec_pengirim.harga;
            //     viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
            // }
            // clear_rute_gudang();
            // console.log('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima);
            tampilkan_pesan('Rute ditemukan, EC_pengiriman = ' + extra_cash_pengirim + ' EC_penerimaan = ' + extra_cash_penerima, 'info');

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
        var lokasi_outlet_penerima_old = $('#inputOutletPenerimaan').val() || 0;
        var lokasi_gudang_penerima_old = $('#inputGudangPenerimaan').val() || 0;
        var lokasi_gudang_pengirim_old = $('#inputGudangPengiriman').val() || 0;

        var provinsi_outlet_penerima;
        var provinsi_outlet_pengirim;
        var url_gudang_pengirim;
        var url_outlet_penerima;
        var url_gudang_penerima;

        var jarak_total = 0;
        var jarak_pengirim = 0;
        var jarak_penerima = 0;

        var jarak_outlet1_ke_gudang1 = 0;
        var jarak_gudang1_ke_gudang2 = 0;
        var jarak_gudang2_ke_outlet2 = 0;
        var jarak_gudang2_ke_penerima = 0;

        var outlet_pengirim = document.getElementById('id_outlet_pengiriman').value ? document.getElementById('id_outlet_pengiriman').value : 0;
        var gudang_pengirim = document.getElementById('inputGudangPengirimManual').value ? document.getElementById('inputGudangPengirimManual').value : 0;
        var gudang_penerima = document.getElementById('inputGudangPenerimaManual').value ? document.getElementById('inputGudangPenerimaManual').value : 0;
        var outlet_penerima = document.getElementById('inputOutletPenerimaManual').value ? document.getElementById('inputOutletPenerimaManual').value : 0;

        $.ajax({
            type: "POST",
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            url: $("#createPengirimanForm").data('url_toko') + 'list/' + outlet_pengirim + '/',
            success: function(response) {
                // console.log("GUDANG ATAUPUN OUTLET TERDEKAT", response);
                html_outlet_pengiriman = response.data_html;
                lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon

                if(gudang_pengirim)
                    var url_gudang_pengirim = $("#createPengirimanForm").data('url_gudang_plain') + 'pengirim/list/' + gudang_pengirim + '/';
                else 
                    var url_gudang_pengirim = $("#createPengirimanForm").data('url_gudang_plain') + 'pengirim/list/' + lokasi_gudang_pengirim_old + '/';

                try {
                    loc_outlet_1 = string_to_arr(response.data.titik_lokasi);
                } catch(error) {}
                provinsi_outlet_pengirim = response.data.provinsi_toko;
                // document.getElementById("inputOutletPengiriman").value = response.data.id;
                // console.log('RUTE OUTLET 1', html_outlet_pengiriman);

                // Mulai cek gudang pengirim
                if (provinsi_outlet_pengirim) {
                    $.ajax({
                        type: "GET",
                        url: url_gudang_pengirim,
                        dataType: "json",
                        data: {
                            csrfmiddlewaretoken: getCookie('csrftoken'),
                            province: provinsi_outlet_pengirim,
                        },
                        success: function(data) {
                            // // console.log('MERNCARI GUDANG', data);
                            loc_gudang_1 = string_to_arr(data.data.titik_lokasi);
                            id_gudang_terdekat_pengirim = data.data.id;
                            document.getElementById("inputGudang1").value = data.data.id;
                            document.getElementById("inputGudangPengiriman").value = data.data.id;
                            html_rute += '<div class="row"><h4>Rute Pengiriman:</h4></div>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>';
                            $('#rute_gudang').append(html_rute);
                            // console.log('RUTE OUTLET 1 + GUDANG 1', html_rute);

                            if(outlet_penerima)
                                var url_outlet_penerima = $("#createPengirimanForm").data('url_toko') + 'penerima/list/' + outlet_penerima + '/';
                            else 
                                var url_outlet_penerima = $("#createPengirimanForm").data('url_toko') + 'penerima/list/' + lokasi_outlet_penerima_old + '/';

                            // Mulai cek outlet penerima
                            $.ajax({
                                type: "GET",
                                url: url_outlet_penerima,
                                success: function(response) {
                                    // // console.log("OUTLET_PENERIMA",response);
                                    html_outlet_penerimaan = response.data_html;
                                    lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                                    try {
                                        loc_outlet_2 = string_to_arr(response.data.titik_lokasi);
                                    } catch(error) {}
                                    document.getElementById("inputOutletPenerimaan").value = response.data.id;
                                    provinsi_outlet_penerima = response.data.provinsi_toko;
                                    // console.log('RUTE OUTLET 2', html_outlet_penerimaan);

                                    if(gudang_penerima)
                                        var url_gudang_penerima = $("#createPengirimanForm").data('url_gudang_plain') + 'penerima/list/' + gudang_penerima + '/';
                                    else 
                                        var url_gudang_penerima = $("#createPengirimanForm").data('url_gudang_plain') + 'penerima/list/' + lokasi_gudang_penerima_old + '/';

                                    // Mulai cek gudang penerima
                                    if (provinsi_outlet_penerima) {
                                        $.ajax({
                                            type: "GET",
                                            url: url_gudang_penerima,
                                            dataType: "json",
                                            data: {
                                                csrfmiddlewaretoken: getCookie('csrftoken'),
                                                province: provinsi_outlet_penerima,
                                            },
                                            success: function(data) {
                                                loc_gudang_2 = string_to_arr(data.data.titik_lokasi);
                                                id_gudang_terdekat_penerima = data.data.id;
                                                document.getElementById("inputGudang2").value = data.data.id;
                                                document.getElementById("inputGudangPenerimaan").value = data.data.id;
                                                html_rute += '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>' + html_outlet_penerimaan;
                                                $('#rute_gudang').html("");
                                                $('#rute_gudang').append(html_rute);
                                                try {
                                                    $('.rute-manual').remove();
                                                    setTimeout(function(){
                                                        document.getElementById("keterangan").insertAdjacentHTML('afterend', html_rute_manual);
                                                    },100);
                                                } catch(error){}

                                                // console.log('RUTE OUTLET 1 + GUDANG 1 + RUTE OUTLET 2 + GUDANG 2', html_rute);
                                                // console.log("GUDANG TITIK", loc_gudang_1, loc_gudang_2);            
                                                // html_rute = html_rute + html_outlet_penerimaan;
                                                // // console.log("RUTE KESELURUHAN", html_rute);
                                                // document.getElementById('rute_gudang').innerHTML = html_rute;
                                                // tampilkan_pesan("Berhasil Mencari Rute", "success");
        
                                                // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP GUDANG
                                                // console.log("DATA PENERIMA", data_penerima, "LOC GUDANG 2", loc_gudang_2, "LOC OUTLET 2", loc_outlet_2);
                                                // console.log("DATA PENGIRIM", data_pengirim, "LOC GUDANG 1", loc_gudang_1, 'LOC OUTLET 1', loc_outlet_1);
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
                                                                                jarak_outlet1_ke_gudang1 = typeof(jarak_outlet1_ke_gudang1) !== "undefined" && !isNaN(jarak_outlet1_ke_gudang1) ? jarak_outlet1_ke_gudang1 : 0;
    
                                                                                jarak_gudang1_ke_gudang2 = typeof(jarak_gudang1_ke_gudang2) !== "undefined" && !isNaN(jarak_gudang1_ke_gudang2) ? jarak_gudang1_ke_gudang2 : 0;
    
                                                                                jarak_gudang2_ke_outlet2 = typeof(jarak_gudang2_ke_outlet2) !== "undefined" && !isNaN(jarak_gudang2_ke_outlet2) ? jarak_gudang2_ke_outlet2 : 0;
    
                                                                                jarak_gudang2_ke_penerima = typeof(jarak_gudang2_ke_penerima) !== "undefined" && !isNaN(jarak_gudang2_ke_penerima) ? jarak_gudang2_ke_penerima : 0;
    
                                                                                jarak_total = (jarak_outlet1_ke_gudang1 + jarak_gudang1_ke_gudang2 + jarak_gudang2_ke_outlet2 + jarak_gudang2_ke_penerima) / 1000;
                                                                                // }
                                                                                
                                                                                // console.log("JARAK TOTAL : ", jarak_total);
                                                                                jarak_total = parseFloat(jarak_total) && !isNaN(jarak_total) ? parseFloat(jarak_total) : 0;
                        
                                                                                // call function to calculate tarif kilometer;
                                                                                total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                                                                total_tarif_kilometer(jarak_total);

                                                                                setTimeout(function(){
                                                                                    $('#modal-rute-manual').modal('hide');
                                                                                },1000);
                                                                                setTimeout(function(){
                                                                                    tampilkan_pesan("Berhasil Memilih Rute Outlet dan Gudang", "success");
                                                                                },1500)
                        
                                                                            }
                                                                        });            
                                                                    }
                                                                })
                                                            }
                                                        });
                                                    }
                                                });
                                                
                                                // jarak_outlet1_ke_gudang1 = hitung_jarak(loc_outlet_1[0], loc_outlet_1[1], loc_gudang_1[0], loc_gudang_1[1]);
                                                //         // console.log("JARAK OUTLET1 GUDANG 1 :  ", jarak_outlet1_ke_gudang1);
                                                // jarak_gudang1_ke_gudang2 = hitung_jarak(loc_gudang_1[0], loc_gudang_1[1], loc_gudang_2[0], loc_gudang_2[1]);
                                                //         // console.log("JARAK GUDANG1 GUDANG2 :  ", jarak_gudang1_ke_gudang2);
                                                // jarak_gudang2_ke_outlet2 = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], loc_outlet_2[0], loc_outlet_2[1]);
                                                //         // console.log("JARAK GUDANG2 OUTLET2 :  ", jarak_gudang2_ke_outlet2);
                                                // jarak_gudang2_ke_penerima = hitung_jarak(loc_gudang_2[0], loc_gudang_2[1], data_penerima[1], data_penerima[0]);
                                                //         // console.log("JARAK GUDANG2 PENERIMA :  ", jarak_gudang2_ke_penerima);

                                                // jarak_outlet1_ke_gudang1 = typeof(jarak_outlet1_ke_gudang1) !== "undefined" && !isNaN(jarak_outlet1_ke_gudang1) ? jarak_outlet1_ke_gudang1 : 0;
                                                // jarak_gudang1_ke_gudang2 = typeof(jarak_gudang1_ke_gudang2) !== "undefined" && !isNaN(jarak_gudang1_ke_gudang2) ? jarak_gudang1_ke_gudang2 : 0;
                                                // jarak_gudang2_ke_outlet2 = typeof(jarak_gudang2_ke_outlet2) !== "undefined" && !isNaN(jarak_gudang2_ke_outlet2) ? jarak_gudang2_ke_outlet2 : 0;
                                                // jarak_gudang2_ke_penerima = typeof(jarak_gudang2_ke_penerima) !== "undefined" && !isNaN(jarak_gudang2_ke_penerima) ? jarak_gudang2_ke_penerima : 0;
                                                // jarak_total = (jarak_outlet1_ke_gudang1 + jarak_gudang1_ke_gudang2 + jarak_gudang2_ke_outlet2 + jarak_gudang2_ke_penerima) / 1000;
                                                
                                                // // console.log("JARAK TOTAL : ", jarak_total);
                                                // jarak_total = parseFloat(jarak_total) && !isNaN(jarak_total) ? parseFloat(jarak_total) : 0;

                                                // // call function to calculate tarif kilometer;
                                                // total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                                // total_tarif_kilometer(jarak_total);

                                                // setTimeout(function(){
                                                //     $('#modal-rute-manual').modal('hide');
                                                // },1000);
                                                // setTimeout(function(){
                                                //     tampilkan_pesan("Berhasil Memilih Rute Outlet dan Gudang", "success");
                                                // },1500)
                                            },
                                            error: function(xhr, status, error) {
                                                var error_response = xhr.responseJSON;
                                                // console.log("ADA ERROR OUTLET 2 GUDANG 2 1 1", error);
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
                // console.log("ADA ERROR OUTLET 1", error);
                var error_response = xhr.responseJSON;
                setTimeout(function(){
                    $('#modal-rute-manual').modal('hide');
                },1000);
                setTimeout(function(){
                    tampilkan_pesan(error_response.msg, error_response.type);
                },1500)
            }
        })
    }

    function outlet_dan_gudang_yang_dilalui_2(data_gudang, data_penerima, data_pengirim, provinsi_pengirim, provinsi_penerima) {
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

        var jarak_outlet1_ke_gudang1 = 0;
        var jarak_gudang1_ke_gudang2 = 0;
        var jarak_gudang2_ke_outlet2 = 0;
        var jarak_gudang2_ke_penerima = 0;

        var outlet_pengirim = document.getElementById('id_outlet_pengiriman').value ? document.getElementById('id_outlet_pengiriman').value : 0;
        $.ajax({
                type: "POST",
                dataType: 'json',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                },
                // url: $("#createPengirimanForm").data('url_toko') + data_pengirim[1] + '/' + data_pengirim[0] + '/',
                url: $("#createPengirimanForm").data('url_toko') + 'list/' + outlet_pengirim + '/',
                success: function(response) {
                    // console.log("GUDANG ATAUPUN OUTLET TERDEKAT", response);
                    html_outlet_pengiriman = response.data_html;
                    lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon
                    try {
                        loc_outlet_1 = string_to_arr(response.data.titik_lokasi);
                    } catch(error) {}
                    provinsi_outlet_pengirim = response.data.provinsi_toko;
                    // document.getElementById("inputOutletPengiriman").value = response.data.id;
                    // console.log('RUTE OUTLET 1', html_outlet_pengiriman);

                },
                error: function(xhr, status, error) {
                    // console.log("ADA ERROR OUTLET 1", error);
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                },
                complete: function() {
                    // // console.log('provinsi', provinsi_outlet_pengirim);
                    if (provinsi_outlet_pengirim) {
                        $.ajax({
                            type: "GET",
                            url: $("#createPengirimanForm").data('url_gudang_plain') + lokasi_outlet_pengirim[0] + '/' + lokasi_outlet_pengirim[1] + '/',
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
                                document.getElementById("inputGudang1").value = data.data.id;
                                document.getElementById("inputGudangPengiriman").value = data.data.id;
                                html_rute += '<div class="row"><h4>Rute Pengiriman:</h4></div>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>';
                                $('#rute_gudang').append(html_rute);
                                // console.log('RUTE OUTLET 1 + GUDANG 1', html_rute);

                            },
                            error: function(xhr, status, error) {
                                // console.log("ADA ERROR OUTLET 1 GUDANG 1", error);
                                var error_response = xhr.responseJSON;
                                tampilkan_pesan(error_response.msg, error_response.type);
                            },
                            complete: function() {
                                $.ajax({
                                    type: "GET",
                                    // url: $("#createPengirimanForm").data('url_toko') + 'nearest/' + data_penerima[1] + '/' + data_penerima[0] + '/',
                                    url: $("#createPengirimanForm").data('url_toko') + "nearest/" + data_penerima[1] + '/' + data_penerima[0] + '/',
                                    success: function(response) {
                                        // // console.log(response);
                                        html_outlet_penerimaan = response.data_html;
                                        lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                                        try {
                                            loc_outlet_2 = string_to_arr(response.data.titik_lokasi);
                                        } catch(error) {}
                                        document.getElementById("inputOutletPenerimaan").value = response.data.id;
                                        provinsi_outlet_penerima = response.data.provinsi_toko_id;
                                        // console.log('RUTE OUTLET 2', html_outlet_penerimaan);
                                    },
                                    error: function(xhr, status, error) {
                                        // console.log("ADA ERROR OUTLET 2", error);
                                        var error_response = xhr.responseJSON;
                                        tampilkan_pesan(error_response.msg, error_response.type);
                                    },
                                    complete: function() {
                                        if (provinsi_outlet_penerima) {
                                            $.ajax({
                                                type: "GET",
                                                url: $("#createPengirimanForm").data('url_gudang_plain') + lokasi_outlet_penerima[0] + '/' + lokasi_outlet_penerima[1] + '/',
                                                dataType: "json",
                                                data: {
                                                    csrfmiddlewaretoken: getCookie('csrftoken'),
                                                    province: provinsi_outlet_penerima,
                                                },
                                                success: function(data) {
                                                    loc_gudang_2 = string_to_arr(data.data.titik_lokasi);
                                                    id_gudang_terdekat_penerima = data.data.id;
                                                    document.getElementById("inputGudang2").value = data.data.id;
                                                    document.getElementById("inputGudangPenerimaan").value = data.data.id;
                                                    html_rute += '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data.data.titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data.data.nama_gudang + ' | Alamat: ' + data.data.alamat + '</small></p></div>' + html_outlet_penerimaan;
                                                    $('#rute_gudang').html("");
                                                    $('#rute_gudang').append(html_rute);
                                                    try {
                                                        $('.rute-manual').remove();
                                                        setTimeout(function(){
                                                            document.getElementById("keterangan").insertAdjacentHTML('afterend', html_rute_manual);
                                                        },100);
                                                    } catch(error){}

                                                    // console.log('RUTE OUTLET 1 + GUDANG 1 + RUTE OUTLET 2 + GUDANG 2', html_rute);
                                                },
                                                error: function(xhr, status, error) {
                                                    // console.log("ADA ERROR OUTLET 2 GUDANG 2 1 1", error);
            
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
                                                    // console.log("DATA PENERIMA", data_penerima, "LOC GUDANG 2", loc_gudang_2, "LOC OUTLET 2", loc_outlet_2);
                                                    // console.log("DATA PENGIRIM", data_pengirim, "LOC GUDANG 1", loc_gudang_1, 'LOC OUTLET 1', loc_outlet_1);
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
                                                                                    jarak_outlet1_ke_gudang1 = typeof(jarak_outlet1_ke_gudang1) !== "undefined" && !isNaN(jarak_outlet1_ke_gudang1) ? jarak_outlet1_ke_gudang1 : 0;
        
                                                                                    jarak_gudang1_ke_gudang2 = typeof(jarak_gudang1_ke_gudang2) !== "undefined" && !isNaN(jarak_gudang1_ke_gudang2) ? jarak_gudang1_ke_gudang2 : 0;
        
                                                                                    jarak_gudang2_ke_outlet2 = typeof(jarak_gudang2_ke_outlet2) !== "undefined" && !isNaN(jarak_gudang2_ke_outlet2) ? jarak_gudang2_ke_outlet2 : 0;
        
                                                                                    jarak_gudang2_ke_penerima = typeof(jarak_gudang2_ke_penerima) !== "undefined" && !isNaN(jarak_gudang2_ke_penerima) ? jarak_gudang2_ke_penerima : 0;
        
                                                                                    jarak_total = (jarak_outlet1_ke_gudang1 + jarak_gudang1_ke_gudang2 + jarak_gudang2_ke_outlet2 + jarak_gudang2_ke_penerima) / 1000;
                                                                                    // }
                                                                                    
                                                                                    // console.log("JARAK TOTAL : ", jarak_total);
                                                                                    jarak_total = parseFloat(jarak_total) && !isNaN(jarak_total) ? parseFloat(jarak_total) : 0;
                            
                                                                                    // call function to calculate tarif kilometer;
                                                                                    total_tarif_gudang(id_gudang_terdekat_pengirim, id_gudang_terdekat_penerima);
                                                                                    total_tarif_kilometer(jarak_total);
                            
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

    // Mencari Gudang terdekat dengan pengirim & penerima
    function outlet_dan_gudang_yang_dilalui(data_gudang, data_penerima, data_pengirim, provinsi_pengirim, provinsi_penerima) {
        var gd_penerima = []; //Array penampung jarak penerima dengan semua gudang
        var gd_pengirim = []; //Array penampung jarak pengirim dengan semua Gudang
        var id_gudang_terdekat_penerima;
        var id_gudang_terdekat_pengirim;

        // PEncarian data Gudang By Lokasi Terdekat dengan pengirim/penerima
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

        loc_gudang_1 = string_to_arr(data_gudang[idx_terdekat_pengirim].titik_lokasi);
        loc_gudang_2 = string_to_arr(data_gudang[idx_terdekat_penerima].titik_lokasi);


        document.getElementById("inputGudang1").value = id_gudang_terdekat_pengirim;
        document.getElementById("inputGudangPengiriman").value = id_gudang_terdekat_pengirim;
        document.getElementById("inputGudang2").value = id_gudang_terdekat_penerima;
        document.getElementById("inputGudangPenerimaan").value = id_gudang_terdekat_penerima;

        var html_rute = "";
        var html_outlet_pengiriman = "";
        var html_outlet_penerimaan = "";

        var lokasi_outlet_penerima;
        var lokasi_outlet_pengirim;

        var jarak_total = 0;
        var jarak_pengirim = 0;
        var jarak_penerima = 0;


        $.ajax({
                type: "POST",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createPengirimanForm").data('url_toko') + 'list/' + $("#createPengirimanForm").data('outlet_id') + '/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    id: $("#createPengirimanForm").data('outlet_id'),
                },
                success: function(response) {
                    // console.log(response);
                    html_outlet_pengiriman = response.data_html;
                    lokasi_outlet_pengirim = string_to_arr(response.data.titik_lokasi); //lat, lon
                    // document.getElementById("inputOutletPengiriman").value = response.data.id;

                },
                error: function(xhr, status, error) {
                    var error_response = xhr.responseJSON;
                    tampilkan_pesan(error_response.msg, error_response.type);
                }

            })
            .done(function() {

                if (idx_terdekat_pengirim != null) {
                    html_rute = '<div class="row"><h4>Rute Pengiriman:</h4></div>' + html_outlet_pengiriman + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data_gudang[idx_terdekat_pengirim].titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #1</span> ' + data_gudang[idx_terdekat_pengirim].nama_gudang + ' | Alamat: ' + data_gudang[idx_terdekat_pengirim].alamat + '</small></p></div>';
                }
                if (idx_terdekat_penerima != null) {
                    html_rute = html_rute + '<div class="timeline-item"><span class="time"><i class="fas fa-map-marker-alt"></i> (' + data_gudang[idx_terdekat_penerima].titik_lokasi + ')</span><p class="timeline-header no-border"><small><span class="badge badge-success">Gudang #2</span> ' + data_gudang[idx_terdekat_penerima].nama_gudang + ' | Alamat: ' + data_gudang[idx_terdekat_penerima].alamat + '</small></p></div>';
                }
                $.ajax({
                        type: "GET",
                        url: $("#createPengirimanForm").data('url_toko') + 'nearest/' + data_penerima[1] + '/' + data_penerima[0] + '/',
                        success: function(response) {
                            // console.log(response);
                            html_outlet_penerimaan = response.data_html;
                            lokasi_outlet_penerima = string_to_arr(response.data.titik_lokasi); //lat, lon
                            document.getElementById("inputOutletPenerimaan").value = response.data.id;

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

                        // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP OUTLET
                        // var url_api_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_penerima[0] + "," + data_penerima[1] + "&end=" + lokasi_outlet_penerima[1] + "," + lokasi_outlet_penerima[0];
                        // var url_api_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_pengirim[0] + "," + data_pengirim[1] + "&end=" + lokasi_outlet_pengirim[1] + "," + lokasi_outlet_pengirim[0];

                        // URL API PERHITUNGAN JARAK PENGIRIM/PENERIMA TERHADAP GUDANG

                        var url_api_penerima = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_penerima[0] + "," + data_penerima[1] + "&end=" + loc_gudang_2[1] + "," + loc_gudang_2[0];
                        var url_api_pengirim = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + data_pengirim[0] + "," + data_pengirim[1] + "&end=" + loc_gudang_1[1] + "," + loc_gudang_1[0];

                        $.ajax({
                            type: "GET",
                            url: url_api_penerima,
                            success: function(data) {
                                jarak_penerima = data.features[0].properties.summary.distance;
                                // console.log(jarak_penerima);
                            },
                            error: function(xhr, status, error) {
                                // if API not found route (length of route) calculate range manualy
                                // Perhitunagn Jarak penerima terhadap Gudang
                                jarak_penerima = hitung_jarak(data_penerima[1], data_penerima[0], loc_gudang_2[0], loc_gudang_2[1]);

                                // Perhitungan Jarak penerima terhadap Outlet
                                // jarak_penerima = hitung_jarak(data_penerima[1], data_penerima[0], lokasi_outlet_penerima[0], lokasi_outlet_penerima[1]);
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
                                        // Perhitunagn Jarak penerima terhadap Gudang
                                        jarak_pengirim = hitung_jarak(data_pengirim[1], data_pengirim[0], loc_gudang_2[0], loc_gudang_2[1]);

                                        // Perhitunagn Jarak penerima terhadap outlet
                                        // jarak_pengirim = hitung_jarak(data_pengirim[1], data_pengirim[0], lokasi_outlet_pengirim[0], lokasi_outlet_pengirim[1]);

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

    function total_tarif_kilometer(kilometer) {
        // console.log(`JARAK ADALAH ${kilometer} KM`);
        $.ajax({
                type: "GET",
                dataType: 'json',
                contentType: "application/json",
                url: $("#createPengirimanForm").data('url_kilometer') + kilometer + '/harga/',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    kilometer: kilometer
                },

                success: function(response) {
                    // // console.log(response.data);
                    document.getElementById("inputTarifKilometer").value = response.harga;
                    // document.getElementById("tarifKilometer").innerHTML = 'Rp. ' + response.harga;
                    viewRupiah('inputTarifKilometer', 'tarifKilometer');
                }
            })
            .done(function() {
                hitung_total();
            });
    }

    function total_tarif_gudang(id_gudang_1, id_gudang_2) {
        $.ajax({
            type: "GET",
            dataType: 'json',
            contentType: "application/json",
            url: $("#createPengirimanForm").data('url_tarif_gudang') + id_gudang_1 + '/' + id_gudang_2 + '/',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                id_gudang_1: id_gudang_1,
                id_gudang_2: id_gudang_2
            },
            success: function(response) {
                if (response.data == '0') {
                    document.getElementById("inputTarifGudang").value = '0';
                    // document.getElementById("tarifGudang").innerHTML = 'Rp. 0';
                    viewRupiah('inputTarifGudang', 'tarifGudang');
                } else {
                    document.getElementById("inputTarifGudang").value = response.data.tarif;
                    // document.getElementById("tarifGudang").innerHTML = 'Rp. ' + response.data.tarif;
                    viewRupiah('inputTarifGudang', 'tarifGudang');
                }

            },
            error: function(xhr, status, error) {
                // console.log(xhr);
            }
        }).done(function() {
            hitung_total();
        });
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

            // alamat_pengirim += getSelectedText('inputDesaPengirim');
            // alamat_pengirim += ", " + getSelectedText('inputKecamatanPengirim');
            // alamat_pengirim += ", " + getSelectedText('inputKotaPengirim');
            // alamat_pengirim += ", " + getSelectedText('inputProvinsiPengirim');

            // alamat_penerima += getSelectedText('inputDesaPenerima');
            // alamat_penerima += ", " + getSelectedText('inputKecamatanPenerima');
            // alamat_penerima += ", " + getSelectedText('inputKotaPenerima');
            // alamat_penerima += ", " + getSelectedText('inputProvinsiPenerima');
            // // console.log(e.target, alamat_penerima, alamat_pengirim);

            // if (alamat_pengirim && alamat_penerima) {
            //     // console.log(`ALAMAT PENGIRIM ${alamat_penerima}`);
            //     // console.log(`ALAMAT PENERIMA ${alamat_penerima}`);
            //     get_loc_degree(alamat_pengirim, alamat_penerima);
            //     hitung_total();
            // }
        } catch(error) {
         // console.log(error) 
         }
    })

    $(document).on('click', '.btn-simpan-manual', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah rute...');
        get_loc_degree_manual(alamat_pengirim, alamat_penerima);
    });

    $('#inputUbahTarifBerat').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifExtraPenerima').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifKilometer').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifLayanan').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifPengemasan').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifGudang').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
    $('#inputUbahTarifLain').on('input', function() {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });

    $(document).on('click', '.btn-simpan-tarif-lain', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Menyimpan Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifLain').val() ? $('#inputUbahTarifLain').val() : $('#inputUbahTarifLain').val(0);
                $('#inputTarifLain').val( parseFloat($('#inputUbahTarifLain').val()).toFixed(0) );
            }catch(error){ $('#inputTarifLain').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifLain').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah extra tarif lain - lain', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-extra-tarif', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifExtraPenerima').val() ? $('#inputUbahTarifExtraPenerima').val() : $('#inputUbahTarifExtraPenerima').val(0);
                $('#inputExtraTarifPenerima').val( parseFloat($('#inputUbahTarifExtraPenerima').val()).toFixed(0) );
            }catch(error){ $('#inputExtraTarifPenerima').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifExtraPenerima').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah extra tarif penerima', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-tarif-berat', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifBerat').val() ? $('#inputUbahTarifBerat').val() : $('#inputUbahTarifBerat').val(0);
                $('#inputTarifBerat').val( parseFloat($('#inputUbahTarifBerat').val()).toFixed(0) );
            }catch(error){ $('#inputTarifBerat').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifBerat').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah tarif berat', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-tarif-kilometer', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifKilometer').val() ? $('#inputUbahTarifKilometer').val() : $('#inputUbahTarifKilometer').val(0);
                $('#inputTarifKilometer').val( parseFloat($('#inputUbahTarifKilometer').val()).toFixed(0) );
            }catch(error){ $('#inputTarifKilometer').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifKilometer').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah tarif kilometer', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-tarif-gudang', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifGudang').val() ? $('#inputUbahTarifGudang').val() : $('#inputUbahTarifGudang').val(0);
                $('#inputTarifGudang').val( parseFloat($('#inputUbahTarifGudang').val()).toFixed(0) );
            }catch(error){ $('#inputTarifGudang').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifGudang').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah tarif gudang', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-tarif-layanan', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifLayanan').val() ? $('#inputUbahTarifLayanan').val() : $('#inputUbahTarifLayanan').val(0)
                $('#inputTarifLayanan').val( parseFloat($('#inputUbahTarifLayanan').val()).toFixed(0) );
            }catch(error){ $('#inputTarifLayanan').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifLayanan').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah tarif layanan', 'success');
        },800)
    });

    $(document).on('click', '.btn-simpan-tarif-pengemasan', function(e){
        $(this).prop('disabled', true);
        $(this).html('<i class="fa fa-spin fa-spinner"></i>&nbsp; Mengubah Tarif...');
        var obj = $(this);
        setTimeout(function(){
            try{
                $('#inputUbahTarifPengemasan').val() ? $('#inputUbahTarifPengemasan').val() : $('#inputUbahTarifPengemasan').val(0)
                $('#inputTarifPengemasan').val( parseFloat($('#inputUbahTarifPengemasan').val()).toFixed(0) );
            }catch(error){ $('#inputTarifPengemasan').val(0) }
        },500)
        setTimeout(function(){
            obj.html('Simpan');
            obj.prop('disabled', false);
            $('#modalUbahTarifPengemasan').modal('hide'); 
            hitung_total();
        },600)
        setTimeout(function(){
            tampilkan_pesan('Berhasil mengubah tarif pengemasan', 'success');
        },800)
    });

    $('#modalUbahTarifBerat').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifBerat').val( !isNaN(parseFloat($('#inputTarifBerat').val()).toFixed(0)) ? parseFloat($('#inputTarifBerat').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifBerat').val(0) }
    });
    $('#modalUbahTarifKilometer').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifKilometer').val( !isNaN(parseFloat($('#inputTarifKilometer').val()).toFixed(0)) ? parseFloat($('#inputTarifKilometer').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifKilometer').val(0) }
    });
    $('#modalUbahTarifGudang').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifGudang').val( !isNaN(parseFloat($('#inputTarifGudang').val()).toFixed(0)) ? parseFloat($('#inputTarifGudang').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifGudang').val(0) }
    });
    $('#modalUbahTarifLayanan').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifLayanan').val( !isNaN(parseFloat($('#inputTarifLayanan').val()).toFixed(0)) ? parseFloat($('#inputTarifLayanan').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifLayanan').val(0) }
    });
    $('#modalUbahTarifPengemasan').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifPengemasan').val( !isNaN(parseFloat($('#inputTarifPengemasan').val()).toFixed(0)) ? parseFloat($('#inputTarifPengemasan').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifPengemasan').val(0) }
    });
    $('#modalUbahTarifLain').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifLain').val( !isNaN(parseFloat($('#inputTarifLain').val()).toFixed(0)) ? parseFloat($('#inputTarifLain').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifLain').val(0) }
    });
    $('#modalUbahTarifExtraPenerima').on('shown.bs.modal', function(){
        try{
            $('#inputUbahTarifExtraPenerima').val( !isNaN(parseFloat($('#inputExtraTarifPenerima').val()).toFixed(0)) ? parseFloat($('#inputExtraTarifPenerima').val()).toFixed(0) : 0 );
        }catch(error){ $('#inputUbahTarifExtraPenerima').val(0) }
    });


    // viewRupiah('inputTarifBerat', 'tarifBerat');
    // viewRupiah('inputTarifKilometer', 'tarifKilometer');
    // viewRupiah('inputTarifGudang', 'tarifGudang');
    // viewRupiah('inputTarifLayanan', 'tarifLayanan');
    // viewRupiah('inputTotalTarif', 'tarifTotal');
    // viewRupiah('inputTarifPengemasan', 'tarifPengemasan');
    // viewRupiah('inputExtraTarifPenerima', 'tarifExtraPenerima');
});