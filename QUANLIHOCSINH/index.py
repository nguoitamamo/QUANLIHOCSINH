import os

from werkzeug.utils import secure_filename

from QUANLIHOCSINH import app, login
from flask import render_template, request, url_for, redirect, session
from flask_login import login_user, logout_user, current_user
import utils, dao



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route("/signin", methods=["POST", "GET"])
def signinuser():
    error_mess = ""
    if request.method == "POST":
        username = request.form["username-signin"]
        password = request.form["password-signin"]

        user = dao.Check_login(username, password)

        if user:
            login_user(user=user)
            return redirect(url_for("index"))

        else:
            error_mess = "Đăng nhập thất bại! Vui lòng nhập lại tên đăng nhập và mật khẩu!"
            return render_template('signin.html', error_mess=error_mess)

    return redirect(url_for('index'))


@app.route("/signup", methods=["POST", "GET"])
def signupuser():
    error_mess = ""
    if request.method.__eq__("POST"):
        username = request.form["username-signup"]
        password = request.form["password-signup"]
        password_repeat = request.form["password-repeat"]
        permission = request.form["permission"]
        monhoc = request.form.get("monhoc") if "monhoc" in request.form else None
        diachi = request.form["diachi"]
        email = request.form["email"]
        fristname = request.form["fristname"]
        lastname = request.form["lastname"]
        ngaysinh = request.form["ngaysinh"]
        sex = request.form['gioitinh']
        sdt = request.form["sdt"]

        try:
            if password.__eq__(password_repeat):

                dao.Add_User(username=username, passw=password, ho=lastname, ten=fristname,
                             ngaysinh=ngaysinh, gioitinh=sex, diachi=diachi, email=email, image=None,
                             permission=permission, TenMonHoc=monhoc, sdt=sdt)
                return redirect(url_for("capnhatthongtin"))
            else:

                error_mess = "Mật khẩu và xác nhận mật khẩu không giống!!"
                return render_template('signup.html', error_mess=error_mess)

        except Exception as ex:

            error_mess = str(ex)
            return render_template('signup.html', error_mess=error_mess)

    return render_template('signup.html', error_mess=error_mess)


@app.route('/send_email', methods=["POST", "GET"])
def send_email():
    if request.method == "POST":
        try:
            email_rec = request.form.get("email-confirm")
            Pass_Confirm_Email = utils.rand_Pass_Confirm_Email()
            dao.AddToken(Pass_Confirm_Email, email_rec)
            utils.Send_Email(Pass_Confirm_Email, email_rec)
            return render_template('signup.html', flag="need_confirm")
        except Exception as ex:
            return render_template('signup.html', error_mess=str(ex))
    return redirect(url_for('index'))


@app.route('/confirmpassemail', methods=["POST", "GET"])
def confirmpassemail():
    error_mess = ""
    if request.method == "POST":
        pass_confirm_email = request.form["pass-confirm-email"]
        try:
            if pass_confirm_email.__eq__(dao.GetToken(pass_confirm_email)):
                return render_template('signup.html', flag="confirm", monhoc=dao.Load_MonHoc(),
                                       pass_confirm_email=dao.LoadEmailConfirm(pass_confirm_email))
            else:
                error_mess = "Mã xác nhận không hợp lệ!!"
                return render_template("signup.html", flag="need_confirm", error_mess=error_mess)
        except Exception as ex:
            return render_template("signup.html", flag="need_confirm", error_mess=str(ex))

    return redirect(url_for('index'))


@app.context_processor
def commom_response():
    if current_user.is_authenticated:
        return {
            'roles': dao.Load_Permission_User(current_user.id),

        }
    return {}


# @app.route('/user/<id>')
# def Login_User_Success(id):
#     return render_template('user.html')

@app.route('/capnhatthongtin')
def capnhatthongtin():
    Permission = dao.Load_PermissionALL()
    return render_template('capnhatthongtin.html', Permission=Permission)


@app.route('/user/lapdanhsachlop')
def lapdanhsachlop():
    if dao.Cnt_Sum_HocSinh_Not_Lop() != int(0):
        dao.Division_Class(12)
    page = request.args.get('page', 1)
    lophocsinh = dao.LoadLop(12, page=int(page))
    return render_template("lapdanhsachlop.html", lophocsinh=lophocsinh)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route("/user/tiepnhanhocsinh")
def tiepnhanhocsinh():
    return render_template("tiepnhanhocsinh.html")


@app.route("/user/nhapdiem")
def nhapdiem():
    return render_template("nhapdiem.html")


@app.route("/user/xuatdiem")
def xuatdiem():
    return render_template("xuatdiem.html")


@app.route('/user/dieuchinhdanhsachlop')
def dieuchinhdanhsachlop():
    page = request.args.get('page', 1)
    lophocsinh = dao.LoadLop(12, page=int(page))
    return render_template("dieuchinhdanhsachlop.html", lophocsinh=lophocsinh)


@app.route('/user/tiepnhanhocsinh/<TenDangNhap>', methods=["POST", "GET"])
def SaveInforHocSinh(TenDangNhap):
    if request.method == "POST":
        diachi = request.form['diachi']
        email = request.form['email']
        sdt = request.form['sdt']
        ho = request.form['lastname']
        ten = request.form['firstname']
        birthday = request.form['ngaysinh']
        sex = request.form['gioitinh']
        diemTbDauVao = request.form['diemTbDauVao']
        try:
            dao.add_HocSinh(float(diemTbDauVao), ho, ten, ngaysinh=birthday, gioitinh=sex, diachi=diachi, email=email,
                            image=None)
            return render_template('tiepnhanhocsinh.html', mess="Lưu thông tin thành công!")
        except Exception as ex:
            return render_template('tiepnhanhocsinh.html', mess=str(ex))
    return redirect(url_for('index'))


@app.route('/capnhatthongtin/<TenDangNhap>', methods=["POST", "GET"])
def UpdateInforUser(TenDangNhap):
    if request.method == "POST":

        permission = request.form.getlist('checkbox_permission')
        PermissionUser = []
        for i in permission:
            PermissionUser.append({i: current_user.id})

        if permission:
            print(permission)
            session["PermissionUser"] = PermissionUser
            return redirect(url_for('index'))
        else:
            error_mess = "Không có lựa chọn nào được chọn!"
            return render_template('capnhatthongtin.html', error_mess=error_mess, TenDangNhap=TenDangNhap)

    return render_template('capnhatthongtin.html', TenDangNhap=TenDangNhap)


@app.route('/approvepermission', methods=["POST", "GET"])
def approvepermission():
    if request.method == "POST":
        userid = request.form["userid"]
        permissionid = request.form["permissionid"]

        dao.AddPermissionUser(permissionid=permissionid, userid=userid)

        for index, i in enumerate(session["PermissionUser"]):
            for key in i.keys():
                if key == permissionid and i[key] == userid:
                    session["PermissionUser"].pop(index)
                    break

        session.modified = True

        error_mess = "Thêm thành công!"

        return {}

    return render_template('index.html')


@app.route('/dieuchinhdanhsachlop/<TenDangNhap>/addhocsinh', methods=["POST", "GET"])
def addhocsinh(TenDangNhap):
    if request.method == "POST":
        print("daa addd")
        return redirect(url_for('index'))


@app.route('/dieuchinhdanhsachlop/<TenDangNhap>/removehocsinh', methods=["POST", "GET"])
def removehocsinh(TenDangNhap):
    if request.method == "POST":
        print("daa remove")

        return redirect(url_for('index'))


@app.route('/signin/quenmatkhau', methods=["POST", "GET"])
def sendpassforgotpassword():
    if request.method == "POST":

        try:
            email = request.form['email-forgot-pass']
            if dao.Check_Email(email):
                Pass_Confirm_Email = utils.rand_Pass_Confirm_Email()

                dao.AddToken(Pass_Confirm_Email, email)

                utils.Send_Email(Pass_Confirm_Email, email)

                return render_template('signin.html', state="sent", email=email)

            else:
                error_mess = "Email này chưa được đăng kí!"
                return render_template('signin.html', error_mess=error_mess)

        except Exception as ex:
            return render_template('signin.html', error_mess=str(ex))

    return redirect(url_for('index'))


@app.route('/signin/quenmatkhau/xacnhan/<email>', methods=["POST", "GET"])
def checkpass(email):
    error_mess = ""

    if request.method == "POST":

        pass_confirm_email = request.form["pass-confirm-email"]

        try:
            token = dao.GetToken(pass_confirm_email)

            if token and pass_confirm_email == token.Value:
                return render_template('signin.html', state="confirmed", email=email)
            else:
                error_mess = "Mã xác nhận không hợp lệ!!"
                return render_template("signin.html", state="sent", email=email, error_mess=error_mess)

        except Exception as ex:
            return render_template("signin.html", state="sent", error_mess=str(ex))

    return redirect(url_for('index'))


@app.route('/signin/capnhatmatkhau/<email>', methods=["POST", "GET"])
def updatepass(email):
    error_mess = ""

    if request.method == "POST":

        pass_new = request.form["pass-new"]
        pass_new_confirm = request.form["pass-new-confirm"]

        try:
            if not pass_new.__eq__(pass_new_confirm):
                error_mess = "Mật khẩu và xác nhận mật khẩu phải giống nhau!"
                return render_template('signin.html', state="confirmed", email=email, error_mess=error_mess)
            else:
                dao.UpdatePassAccount(email, pass_new)
                return redirect(url_for('index'))

        except Exception as ex:
            return render_template('signin.html', state="confirmed", error_mess=str(ex))


@app.route('/user/tiepnhanhocsinh', methods=['POST', 'GET'])
def uploaddanhsachhocsinh():
    if request.method == 'POST':

        file = request.files.get('file')


        if not file or file.filename == '':
            return render_template('tiepnhanhocsinh.html', mess="Bạn chưa chọn file!")

        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            try:

                page = request.args.get('page', 1)
                dic = utils.LoadFile(file, page = int(page))


                # Render giao diện danh sách học sinh
                return render_template('tiepnhanhocsinh.html', data=dic, file = file)
            except Exception as e:
                return render_template('tiepnhanhocsinh.html', mess=f"Lỗi khi xử lý file: {e}")
        else:
            return render_template('tiepnhanhocsinh.html',
                                   mess="File không đúng định dạng. Vui lòng upload file .xlsx hoặc .xls.")
    return render_template('tiepnhanhocsinh.html')


@app.route('/user/tiepnhanhocsinh')
def dividelistdshocsinh():

    page = request.args.get('page', 1)


    # if not filepath:
    #     return "Not file"
    #
    #
    # dic = utils.LoadFile(filepath, int(page))


    return render_template('tiepnhanhocsinh.html' )



@login.user_loader
def user_load(id):
    return dao.Get_User_By_ID(id=id)


if __name__ == "__main__":
    from QUANLIHOCSINH.admin import *

    app.run(debug=True)
