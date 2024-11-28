function Column15phut(state) {


    fetch(`/user/nhapdiem/column15phut/${state}`, {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("Xóa thất bại. Vui lòng thử lại!");
            }
        })


}


function Column1tiet(state) {


    fetch(`/user/nhapdiem/column1tiet/${state}`, {
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("Xóa thất bại. Vui lòng thử lại!");
            }
        })

}


function updateLabel(selectElement, inputId) {




    const tenlop = selectElement.value;

    const inputField = document.getElementById(inputId);

    inputField.value = tenlop;

    if( inputId === "lopLabel") {
        fetch(`/user/nhapdiem/loadmon/${tenlop}`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    const monhocs = data.dsmonhoc;

                    const monHocSelect = document.querySelector("select[name='dsmonhoc']");

                    monhocs.forEach(mon => {

                        const option = document.createElement("option");
                        option.text = `${mon.TenMonHoc}`;
                        monHocSelect.add(option);
                    });

                } else {
                    alert("Xóa thất bại. Vui lòng thử lại!");
                }
            })
    }
}


function FindLop(obj) {

    alert(obj.value)

    const lop = obj.value

    const monhoc = document.getElementById("monhocLabel").value;
    const hocki = document.getElementById("hocki").value;
    const namhoc = document.getElementById("namehoc").value;



    alert( lop , monhoc , hocki , namhoc)


    // const lop = document.getElementById("lop").value;
    //
    // alert(lop)


    //   fetch(`/user/nhapdiem/column1tiet/${state}`, {
    //     method: 'put',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     }
    // }).then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             window.location.reload();
    //         } else {
    //             alert("Xóa thất bại. Vui lòng thử lại!");
    //         }
    //     })


}