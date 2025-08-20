function makeCodeQR(text) {
    if (!text) {
        tampilkan_pesan('ID/Resi Tidak ada!', 'error');
        return;
    }
    document.getElementById("qr_print").innerHTML = '';
    var qrcode = new QRCode(document.getElementById("qr_print"), {
        width: 100,
        height: 100
    });

    qrcode.makeCode(text);
}

function makeCodeQROrderPickup(text) {
    console.log('invoked');
    if (!text) {
        tampilkan_pesan('ID/Resi Tidak ada!', 'error');
        return;
    }
    try {
    document.getElementById("qr_print_order").innerHTML = '';
    var qrcode = new QRCode(document.getElementById("qr_print_order"), {
        width: 100,
        height: 100
    });

    qrcode.makeCode(text);
    } catch(error){
        tampilkan_pesan(error, 'error');
    }
}

function showQR() {
return new Instascan.Scanner({ video: document.getElementById('preview'), scanPeriod: 5, mirror: false });
    scanner.addListener('scan',function(content){
        alert(content);
        //window.location.href=content;
    });
    Instascan.Camera.getCameras().then(function (cameras){
        if(cameras.length>0){
            scanner.start(cameras[0]);
            $('[name="options"]').on('change',function(){
                if($(this).val()==1){
                    if(cameras[0]!=""){
                        scanner.start(cameras[0]);
                    }else{
                        alert('No Front camera found!');
                    }
                }else if($(this).val()==2){
                    if(cameras[1]!=""){
                        scanner.start(cameras[1]);
                    }else{
                        alert('No Back camera found!');
                    }
                }
            });
        }else{
            console.error('No cameras found.');
            alert('No cameras found.');
        }
    }).catch(function(e){
        console.error(e);
        alert(e);
    });
}