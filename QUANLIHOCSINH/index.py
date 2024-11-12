
from QUANLIHOCSINH import app, login
from flask import render_template, request, url_for, redirect, session
from flask_login import login_user, logout_user, current_user
import utils



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html' )


@app.route("/signin", methods=["POST", "GET"])
def signinuser():
    error_mess= ""
    if request.method == "POST":
        username = request.form["username-signin"]
        password = request.form["password-signin"]
        user = utils.Check_login(username, password)
        if user:
            login_user(user=user)
            print(current_user.id)
            return redirect(url_for("index"))
        else:
            error_mess= "Đăng nhập thất bại! Vui lòng nhập lại tên đăng nhập và mật khẩu"
            return render_template('signin.html', error_mess=error_mess)

    return redirect(url_for('index.html'))



@app.route("/signup", methods=["POST", "GET"])
def signupuser():
    error_mess = ""
    if request.method.__eq__("POST"):
        username = request.form["username-signup"]
        password = request.form["password-signup"]
        password_repeat = request.form["password-repeat"]
        permission = request.form["permission"]
        monhoc= request.form["monhoc"]
        diachi = request.form["diachi"]
        email = request.form["email"]
        fristname = request.form["fristname"]
        lastname = request.form["lastname"]
        ngaysinh = request.form["ngaysinh"]
        sex= request.form['gioitinh']
        sdt = request.form["sdt"]
        try:
            if password.__eq__(password_repeat):
                utils.Add_User(username=username, passw=password, ho=lastname,ten = fristname ,
                               ngaysinh= ngaysinh, gioitinh= sex, diachi= diachi,email=email,image = None,
                               permission=permission, TenMonHoc=monhoc , sdt = sdt)
                return redirect(url_for("index"))
            else:
                error_mess= "Mật khẩu và xác nhận mật khẩu không giống!!"
                return render_template('signup.html', error_mess=error_mess)
        except Exception as ex:
            error_mess = str(ex)
            return render_template('signup.html', error_mess=error_mess)
    return render_template('signup.html', error_mess=error_mess)



@app.route('/send_email' , methods=["POST", "GET"])
def send_email():
    if request.method == "POST":
        try:
            email_rec = request.form.get("email-confirm")
            Pass_Confirm_Email = utils.rand_Pass_Confirm_Email()
            utils.AddToken(Pass_Confirm_Email, email_rec)
            utils.Send_Email(Pass_Confirm_Email, email_rec)
            return render_template('signup.html', flag = "need_confirm")
        except Exception as ex:
            return render_template('signup.html', error_mess = str(ex))
    return redirect(url_for('index'))


@app.route('/confirmpassemail' , methods=["POST", "GET"])
def confirmpassemail():
    error_mess=""
    if request.method == "POST":
        pass_confirm_email = request.form["pass-confirm-email"]
        try:
            if pass_confirm_email.__eq__(utils.GetToken(pass_confirm_email)):
                return render_template('signup.html', flag= "confirm" , monhoc = utils.Load_MonHoc() )
            else:
                error_mess = "Mã xác nhận không hợp lệ!!"
                return render_template("signup.html",flag = "need_confirm", error_mess=error_mess)
        except Exception as ex:
                return render_template("signup.html",flag = "need_confirm",error_mess=str(ex))

    return redirect(url_for('index'))


@app.context_processor
def commom_response():
    if current_user.is_authenticated:
        return {
            'roles': utils.Load_Permission_User(current_user.id),
        }
    return {}

@app.route('/user/<id>')
def Login_User_Success(id):
    return render_template('user.html')

@app.route('/capnhatthongtin')
def capnhatthongtin():
    return render_template('capnhatthongtin.html', Permission = utils.Load_PermissionALL())

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route("/user/tiepnhanhocsinh")
def tiepnhanhocsinh():
    return render_template("tiepnhanhocsinh.html"  )

@app.route("/user/nhapdiem")
def nhapdiem():
    return render_template("nhapdiem.html")


@app.route("/user/xuatdiem")
def xuatdiem():
    return render_template("xuatdiem.html")

@app.route("/user/dieuchinhdanhsachlop")
def dieuchinhdanhsachlop():
    return render_template("dieuchinhdanhsachlop.html")

@app.route('/user/tiepnhanhocsinh/<TenDangNhap>' ,methods=["POST", "GET"] )
def SaveInforHocSinh(TenDangNhap):
    if request.method == "POST":
        diachi = request.form['diachi']
        email= request.form['email']
        sdt = request.form['sdt']
        ho = request.form['lastname']
        ten = request.form['firstname']
        birthday = request.form['ngaysinh']
        sex = request.form['gioitinh']
        diemTbDauVao = request.form['diemTbDauVao']
        try:
            utils.add_HocSinh(float(diemTbDauVao), ho, ten, ngaysinh=birthday, gioitinh=sex, diachi=diachi, email= email , image=None)
            return render_template('tiepnhanhocsinh.html', mess = "Lưu thông tin thành công!")
        except Exception as ex:
            return render_template('tiepnhanhocsinh.html', mess = str(ex))
    return redirect(url_for('index'))

@login.user_loader
def user_load(id):
    return utils.Get_User_By_ID(id=id)

if __name__== "__main__":
    from QUANLIHOCSINH.admin import *
    app.run(debug=True)


