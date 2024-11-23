


    document.getElementById('option_giangvien').addEventListener('change', function (event) {
        const permission_giangvien = document.getElementById('permisson_giangvien');

        if (event.target.value === 'Giảng viên') {
            permission_giangvien.style.display = 'flex';
        } else {
            permission_giangvien.style.display = 'none';
        }
    });




    // // Hàm xử lý khi thêm từ các nút cộng khác
        // function addPhone(element) {
        //     const newDiv = document.createElement('div');
        //     newDiv.className = 'w3-container';
        //
        //     newDiv.innerHTML = `
        //         <p style="margin-left: 4%;">
        //             <i class="fa-solid fa-mobile-screen-button"></i>
        //             <input type="text" name="sdt" placeholder="  Số điện thoại.." style="margin-bottom: 20px;">
        //             <i class="fa-solid fa-plus" style="cursor: pointer;" onclick="addPhone(this)"></i>
        //         </p>
        //     `;
        //     element.closest('.w3-container').after(newDiv);
        // }