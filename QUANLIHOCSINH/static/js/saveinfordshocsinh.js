function UpdateSdt(stt, obj) {


    fetch('/user/uploaddanhsachhocsinh/updatesdt', {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            STT: stt,
            sdt: obj.value
        })
    })


}


function RemoveHocSinh(stt) {
    if (!confirm("Bạn có chắc chắn muốn xóa học sinh này không?")) {
        return;
    }
    fetch(`/user/uploaddanhsachhocsinh/removehocsinh/${stt}`, {
        method: 'delete',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`hs${stt}`);
                if (row) {
                    row.remove();
                }
            } else {
                alert("Xóa thất bại. Vui lòng thử lại!");
            }
        })

}

function SaveInforDshocsinh(){

    alert("dã click")
    fetch(`/user/uploaddanhsachhocsinh/savedshocsinh`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("đã lưu")
            } else {
                alert("Xóa thất bại. Vui lòng thử lại!");
            }
        })

}
