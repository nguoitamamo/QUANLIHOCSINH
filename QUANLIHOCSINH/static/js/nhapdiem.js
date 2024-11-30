const lop = document.getElementById('dslop');
const searchInputLop = document.getElementById('lopLabel');
const suggestionsListLop = document.getElementById('suggestionLop');
const searchInputMon = document.getElementById('monhocLabel');
const suggestionsListMon = document.getElementById('suggestionMonHoc');


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


function GetDataTable() {
    var socot15phut = parseInt(document.getElementById("socot15phut").textContent.trim());
    var socot1tiet = parseInt(document.getElementById("socot1tiet").textContent.trim());

    diemhocsinh = []

    $('#scoreTable tr').each(function () {

        var maHocSinh = $(this).attr("id");


        var diem15phut = [];
        for (var i = 2; i < 2 + socot15phut; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem15phut.push(diem.trim());
            }
        }


        var diem1tiet = [];
        for (var i = 2 + socot15phut; i < 2 + socot15phut + socot1tiet; i++) {
            var diem = $(this).find("td").eq(i).find("input").val();
            if (diem && diem.trim() !== "") {
                diem1tiet.push(diem.trim());
            }
        }

        var diemthi = $(this).find("td").last().find("input").val();
        if (!diemthi) {
            diemthi = "";
        }

        if (diem15phut.length > 0 || diem1tiet.length > 0 || diemthi !== "") {
            diemhocsinh.push({
                maHocSinh: maHocSinh,
                diem15phut: diem15phut,
                diem1tiet: diem1tiet,
                diemthi: diemthi
            });
        }

    });
    return diemhocsinh
}


function Suggestion(keyword, searchInput, suggestionsList, field) {

    let malop = 'lop'

    if (field === 'monhoc') {
        const lop = document.getElementById('dslop');
        malop = lop.value;

        console.log("Monhoc" + malop);
    }

    fetch(`/user/nhapdiem/lop/search/${keyword}/${field}/${malop}`)
        .then(response => response.json())
        .then(data => {

            suggestionsList.innerHTML = '';

            data.forEach(suggestionEdOfKeyword => {
                suggestionEdOfKeyword.forEach(item => {

                    const li = document.createElement('li');
                    li.textContent = item;

                    li.addEventListener('click', () => {
                        searchInput.value = item;
                        suggestionsList.innerHTML = '';


                        for (let i = 0; i < lop.options.length; i++) {
                            if (lop.options[i].text === searchInputLop.value) {
                                lop.selectedIndex = i;

                                break;
                            }
                        }
                         LoadMonOfLop();

                    });

                    suggestionsList.appendChild(li);
                });
            });
        })
}


searchInputLop.addEventListener('input', () => {
    const keyword = searchInputLop.value.trim();
    if (keyword.length === 0) {
        suggestionsListLop.innerHTML = '';
        return;
    }

    Suggestion(keyword, searchInputLop, suggestionsListLop, 'lop')

});

searchInputMon.addEventListener('input', () => {
    const keyword = searchInputMon.value.trim();
    if (keyword.length === 0) {
        suggestionsListMon.innerHTML = '';
        return;
    }

    Suggestion(keyword, searchInputMon, suggestionsListMon, 'monhoc')

});

function updateLabel(selectElement, inputId) {


    const selectedOption = selectElement.options[selectElement.selectedIndex];

    const tenlop = selectedOption.text;

    const inputField = document.getElementById(inputId);

    inputField.value = tenlop;


}


// searchInputLop.addEventListener('change', function () {
//
//
//
// });

//
lop.addEventListener('change', function () {


    LoadMonOfLop();
});


function saveTableData(state) {
    diemhocsinh = GetDataTable()

    console.log(diemhocsinh)

    monhoc = document.getElementById("monhocLabel").value;
    hocki = document.getElementById("hocky").value;
    namhoc = document.getElementById("namhoc").value;

    fetch(`/user/nhapdiem/diemdshocsinh/${lop.value}/${monhoc}/${hocki}/${namhoc}/${state}`, {
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
                alert("thafnh coong")
            }
        })


}

function LoadMonOfLop() {


    const lop = document.getElementById('dslop');
    malop = lop.value;

    console.log(malop)
    // // console.log(lop.value)
    //
    // malop = 'L10A1_2023'
    fetch(`/user/nhapdiem/loadmon/${malop}`, {
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
                    option.text = `${mon.TenMonHoc}`;
                    monHocSelect.add(option);
                });

            } else {
                alert(data.error);
            }
        })
}
