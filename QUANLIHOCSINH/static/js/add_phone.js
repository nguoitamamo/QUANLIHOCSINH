ngaysinhs = document.getElementsByClassName('ngaysinh');

let currentDate = new Date();


let year = currentDate.getFullYear();


for (var i = 0; i < ngaysinhs.length; i++) {

    age = parseInt(year) - parseInt(ngaysinhs[i].textContent)

    if (age < 15 || age > 20) {
        ngaysinhs[i].closest('tr').style.color = "red";
    }

}


function Add_phone_User(element) {

    element.remove();
    const p_container = document.getElementsByClassName('p_phone');
    for (let p of p_container) {
        p.style.marginLeft = "0"
    }

    const newDiv = document.createElement('div');
    newDiv.className = 'w3-container';


    newDiv.innerHTML = `
        <p  class="signup_phone p_phone">
            <i class="fa-solid fa-mobile-screen-button"></i>
            <input type="text" name="sdt" placeholder="  Số điện thoại..">
            <i class="fa-solid fa-plus add_phone" style="cursor: pointer;" onclick="Add_phone_User(this)"></i>
        </p>
    `;

    document.getElementById('infor_user').appendChild(newDiv);
}
