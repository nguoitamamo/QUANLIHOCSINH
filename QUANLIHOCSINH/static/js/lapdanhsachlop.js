

function LoadLopOfKhoi(makhoi) {


    alert(makhoi)
    fetch(`/user/danhsachlop/${makhoi}`, {
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


    alert(tenkhoi);
}