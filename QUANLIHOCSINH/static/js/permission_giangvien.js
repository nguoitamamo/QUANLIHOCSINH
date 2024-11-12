// document.getElementById('btn-continue-email').addEventListener('click', function () {
//
//     const email = document.getElementById('email-confirm').value;
//     if (email === '') {
//         alert('Vui lòng nhập email');
//        window.location.href = '/';
//     }
// });
//
// document.getElementById('send_pass_confirm_email').addEventListener('click', function (event) {
//     const email = document.getElementById('email-confirm').value;
//     if (email === '') {
//         alert("Vui lòng nhập email!");
//     } else {
//
//
//     }
// });




    document.getElementById('option_giangvien').addEventListener('change', function (event) {
        const permission_giangvien = document.getElementById('permisson_giangvien');

        if (event.target.value === 'Giảng viên') {
            permission_giangvien.style.display = 'flex';
        } else {
            permission_giangvien.style.display = 'none';
        }
    });
