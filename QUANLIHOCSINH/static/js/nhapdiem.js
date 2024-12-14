let lop = document.getElementById('dslop');
const searchInputLop = document.getElementById('lopLabel');
const errorContainer = document.querySelector('.alert-danger');
const errorText = document.getElementById('error');


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
                errorText.innerText = data.error; // Hiển thị nội dung lỗi
                errorContainer.style.display = "block";
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
                errorText.innerText = data.error; // Hiển thị nội dung lỗi
                errorContainer.style.display = "block";
            }
        })

}


function GetDataTable() {


    const socot15phut = parseInt(document.getElementById("socot15phut").textContent.trim());
    const socot1tiet = parseInt(document.getElementById("socot1tiet").textContent.trim());


    diemhocsinh = []

    $('#scoreTable tr').each(function () {

        var maHocSinh = ''

        maHocSinh = $(this).attr("id");

        var hoten = $(this).find("td").eq(1).text();

        if (maHocSinh === "") {
            return; // Skip this row if maHocSinh is empty
        }

        console.log(hoten)
        var diem15phut = [];
        for (var i = 2; i < 2 + socot15phut; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem15phut.push(diem.trim());
            } else {
                diem15phut.push('');
            }
        }


        var diem1tiet = [];
        for (var i = 2 + socot15phut; i < 2 + socot15phut + socot1tiet; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem1tiet.push(diem.trim());
            } else {
                diem1tiet.push('');
            }
        }

        var diemthi = $(this).find("td").last().find("input").val();
        if (!diemthi) {
            diemthi = "";
        }

        if (maHocSinh && maHocSinh.trim() !== "" && (diem15phut.length > 0 || diem1tiet.length > 0 || diemthi !== "")) {
            diemhocsinh.push({
                maHocSinh: maHocSinh,
                hoten: hoten,
                diem15phut: diem15phut,
                diem1tiet: diem1tiet,
                diemthi: diemthi
            });
        }


    });
    return diemhocsinh
}


// function Suggestion(keyword, searchInput, suggestionsList, field) {
//
//     let malop = 'lop'
//
//     if (field === 'monhoc') {
//         const lop = document.getElementById('dslop');
//         malop = lop.value;
//
//         console.log("Monhoc" + malop);
//     }
//
//     fetch(`/user/nhapdiem/lop/search/${keyword}/${field}/${malop}`)
//         .then(response => response.json())
//         .then(data => {
//
//             suggestionsList.innerHTML = '';
//
//             data.forEach(suggestionEdOfKeyword => {
//                 suggestionEdOfKeyword.forEach(item => {
//
//                     const li = document.createElement('li');
//                     li.textContent = item;
//
//                     li.addEventListener('click', () => {
//                         searchInput.value = item;
//                         suggestionsList.innerHTML = '';
//
//
//                         for (let i = 0; i < lop.options.length; i++) {
//                             if (lop.options[i].text === searchInputLop.value) {
//                                 lop.selectedIndex = i;
//
//                                 break;
//                             }
//                         }
//                         LoadMonOfLop();
//
//                     });
//
//                     suggestionsList.appendChild(li);
//                 });
//             });
//         })
// }


searchInputLop.addEventListener('input', () => {

    for (let i = 0; i < lop.options.length; i++) {
        if (lop.options[i].text === searchInputLop.value) {
            lop.selectedIndex = i;
            break;
        }
    }
    LoadMonOfLop();

});


function updateLabel(selectElement, inputId) {


    const selectedOption = selectElement.options[selectElement.selectedIndex];

    const tenlop = selectedOption.text;

    const inputField = document.getElementById(inputId);

    inputField.value = tenlop;


}

lop.addEventListener('change', function () {
    LoadMonOfLop();
});


function saveTableData(state) {


    errorContainer.style.display = "none";


    diemhocsinh = GetDataTable()

    console.log(diemhocsinh)

    monhoc = document.getElementById("monhocLabel").value;
    hocki = document.getElementById("hocky").value;
    namhoc = document.getElementById("namhoc").value;


    const selectedOption = lop.options[lop.selectedIndex];

    malop = selectedOption.value;

    fetch(`/user/nhapdiem/diemdshocsinh/${malop}/${monhoc}/${hocki}/${namhoc}/${state}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            diemdshocsinh: diemhocsinh
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                errorText.innerText = data.state;


            } else {
                errorText.innerText = data.state;

            }
            errorContainer.style.display = "block";
        })


}

function LoadAllMon() {

    fetch('/user/nhapdiem/loadallmon', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const monhocs = data.dsmonhoc;

                const monHocSelect = document.querySelector("select[name='dsmonhoc']");

                monHocSelect.innerHTML = '';

                monhocs.forEach(mon => {

                    const option = document.createElement("option");
                    option.text = `${mon}`;
                    monHocSelect.add(option);
                });

            } else {
                alert(data.error);
            }
        })

}


function LoadMonOfLop() {


    const lop = document.getElementById('dslop');
    malop = lop.value;

    fetch(`/user/nhapdiem/loadmon/${malop}`, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                const monhocs = data.dsmonhoc;

                const monHocDataList = document.getElementById('monhocLabels');

                monHocDataList.innerHTML = ''
                monhocs.forEach(mon => {
                    const option = document.createElement("option");
                    option.value = `${mon.TenMonHoc}`;
                    monHocDataList.appendChild(option);
                });


                const monHocSelect = document.querySelector("select[name='dsmonhoc']");

                monHocSelect.innerHTML = '';

                monhocs.forEach(mon => {

                    const option = document.createElement("option");
                    option.text = `${mon.TenMonHoc}`;
                    monHocSelect.add(option);
                });

            } else {
                alert(data.error);
            }
        })

}