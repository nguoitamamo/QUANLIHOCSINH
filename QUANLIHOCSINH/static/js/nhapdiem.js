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

    fetch(`/user/nhapdiem/loadmon/${tenlop}`, {
        method: 'post',
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
