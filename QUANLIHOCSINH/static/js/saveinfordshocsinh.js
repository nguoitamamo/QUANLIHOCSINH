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

function SaveInforDshocsinh() {

    fetch('/user/uploaddanhsachhocsinh/savedshocsinh', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload()
            }
        })

}


function RemoveHS(MaHocSinh, TenLop) {



    fetch(`/user/dieuchinhdanhsachlop/removehocsinh/${TenLop}/${MaHocSinh}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`${MaHocSinh}`);
                if (row) {
                    row.remove();
                }
                alert("thành công")
                window.location.reload();
            } else {
                alert("Xóa không thành công!")
            }
        })
}

function CheckAddHocSinh(id, obj) {

    if (obj.checked) {
        fetch(`/user/dieuchinhdanhsachlop/addhocsinh/${id}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        })
    } else {
        fetch(`/user/dieuchinhdanhsachlop/removehocsinh/${id}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        })
    }


}


function AddHocSinhToLop(tenlop) {



    fetch(`/user/dieuchinhdanhsachlop/addhocsinh/ds/${tenlop}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }

    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}

window.onload = function() {
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
}



function SelectKhoi(obj) {


    alert(obj.value);

    fetch(`/user/dieuchinhdanhsachlop/khoi/${obj.value}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }

    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}