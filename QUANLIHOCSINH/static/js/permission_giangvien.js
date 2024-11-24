


    document.getElementById('option_giangvien').addEventListener('change', function (event) {
        const permission_giangvien = document.getElementById('permisson_giangvien');

        if (event.target.value === 'Giảng viên') {
            permission_giangvien.style.display = 'flex';
        } else {
            permission_giangvien.style.display = 'none';
        }
    });


