function Column15phut(state) {


    fetch(`/user/nhapdiem/column15phut/${state}`, {
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


function Column1tiet(state) {


    fetch(`/user/nhapdiem/column1tiet/${state}`, {
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

