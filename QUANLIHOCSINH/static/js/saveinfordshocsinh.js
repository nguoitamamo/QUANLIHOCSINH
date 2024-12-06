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
                window.location.reload();
            } else {
                alert("Xóa không thành công!")
            }
        })
}

function CheckAddHocSinh(hocsinhid, obj) {

    if (obj.checked) {
        console.log(hocsinhid);
        fetch(`/user/dieuchinhdanhsachlop/addhocsinh/${hocsinhid}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        })
    } else {
        fetch(`/user/dieuchinhdanhsachlop/removehocsinh/${hocsinhid}`, {
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
            } else {

                const errorContainer = document.querySelector('.alert-danger');
                const errorText = document.getElementById('error');
                errorText.innerText = data.error;
                errorContainer.style.display = "block";
            }
        })

}

window.onload = function () {
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


function DevisionClassBegin0() {

    fetch('/user/dieuchinhdanhsachlop/sapxeptudau', {
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


function CreateLop(solop) {


    alert(solop)
}


// function CheckAddAllHocSinh(obj) {
//
//     // if( obj.checked) {
//         const dschecbox = document.querySelectorAll('.form-check-input-creatlop');
//
//         dschecbox.forEach(checkbox => {
//             checkbox.checked = obj.checked;
//
//             const checkboxId = checkbox.getAttribute('id')
//
//             if (checkboxId) {
//                 CheckAddHocSinh(checkboxId, checkbox)
//             }
//         });
//     // }
//
//
// }


function CreateLopWithDsHocSinh() {

    const tenlop = document.getElementById('tenlop').value.trim();
    fetch(`/user/dieuchinhdanhsachlop/taolop/ds/${tenlop}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })

}


function FindOfCondition() {
    const selectcondition = document.getElementById('selectcondition').value;
    const textcondition = document.getElementById('textcondition').value.trim();


    const value = parseFloat(textcondition);


    const rows = document.querySelectorAll('.container-dshoc-notlop tbody tr');

    rows.forEach(row => {
        const diemCell = row.querySelector('.diem');
        if (!diemCell) return;

        const diem = parseFloat(diemCell.textContent);

        let match = false;
        switch (selectcondition) {
            case '1':
                match = diem > value;
                break;
            case '2':
                match = diem < value;
                break;
            case '3':
                match = diem >= value;
                break;
            case '4':
                match = diem <= value;
                break;
        }

        if (match) {
            row.classList.add('highlight-row');
        }else {
            row.classList.remove('highlight-row');
        }
    });
}



function FindHocSinhAllLop() {

    const textinput = document.getElementById('inputsearch').value.trim();


     fetch(`/user/dieuchinhdanhsachlop/timkiem/dshocsinh/${textinput}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })


}