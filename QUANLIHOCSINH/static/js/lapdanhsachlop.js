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


}


function SearchHocSinh(input) {

    alert(input)


}


function TimKiemHocSinhNew() {

    const textinput = document.querySelector('.btn_timkiem').value



    fetch(`/user/danhsachlop/timkiemhocsinh/${textinput}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }

    })

}