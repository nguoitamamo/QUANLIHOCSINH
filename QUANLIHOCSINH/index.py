import itertools
import math
from datetime import datetime

from QUANLIHOCSINH import app, login
from flask import render_template, request, url_for, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user
import utils, dao

from math import ceil


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
        username = request.form["txt_username_signin"]
        password = request.form["txt_password_signin"]

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
        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat = request.form.get("passwordrepeat")
        try:
            if dao.Check_Username_Exits(username):
                error_mess = "Tên đăng nhập đã tồn tại!!"
                return render_template('signup.html', error_mess=error_mess, flag="confirm")
            else:
                if password.__eq__(password_repeat):

                    avatar = request.files.get("avatar")

                    sdt = list(request.form.getlist('sdt'))

                    permission = request.form.getlist('checkbox_permission')

                    PermissionUser = []
                    for i in permission:
                        PermissionUser.append({dao.GetPerMission(id=i).Value: username})

                    if permission:
                        session["PermissionUser"] = PermissionUser

                    activeaccount = request.form.get("activeaccount")

                    if "activeaccount" not in session:
                        session["activeaccount"] = []

                    if activeaccount == "on" and username not in session["activeaccount"]:
                        session["activeaccount"].append(username)
                        session.modified = True

                    data = request.form.copy()

                    del data['passwordrepeat']
                    del data["sdt"]
                    del data["checkbox_permission"]
                    del data["activeaccount"]

                    dao.Add_User(avatar=avatar, sdt=sdt, **data)

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
            utils.Send_Email(subject="Mã xác nhận", content=Pass_Confirm_Email, email_rec=email_rec)
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
                                       pass_confirm_email=dao.LoadEmailConfirm(pass_confirm_email),
                                       Permission=dao.Load_PermissionALL())
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
            'Permission': dao.Load_Permission()

        }
    return {'Permission': dao.Load_Permission()}


@app.route('/capnhatthongtin')
def capnhatthongtin():
    Permission = dao.Load_PermissionALL()
    return render_template('capnhatthongtin.html', Permission=Permission)


@app.route('/user/lapdanhsachlop')
def lapdanhsachlop():

    solop = len(dao.GetMaLop(dao.CurrentYear()))

    sum_hoc_sinh_not_lop = dao.Cnt_Sum_HocSinh_Not_Lop() #tổng học sinh not lớp
    sum_siso_all_lop_current = dao.CntSiSoLopCurrent(solop = solop, key = 'L10A') #tổng học sinh của tất các các lớp
    sum_all_hoc_sinh_all_lop = solop*app.config["MAX_SS_LOP"] # max sĩ số all lớp

    if  sum_hoc_sinh_not_lop > ( sum_all_hoc_sinh_all_lop - sum_siso_all_lop_current ):
        solop = ceil(sum_hoc_sinh_not_lop/app.config["MAX_SS_LOP"])
        solopthem = ceil(  (sum_all_hoc_sinh_all_lop - sum_siso_all_lop_current + sum_hoc_sinh_not_lop ) / app.config["MAX_SS_LOP"] )

        dao.Division_Class(solopcanchia=solop, solopthem=solopthem)


    page = request.args.get('page', 1)
    malop = 'L10A' + str(page) + '_' + dao.CurrentYear()
    lophocsinh = dao.LoadLop(malop=malop, key="info")

    return render_template("lapdanhsachlop.html", lophocsinh=lophocsinh,
                           solop=solop, dslopcheckbox=dao.LoadKhoiAll(), lop='10A' + str(page))


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
    if "socot15phut" not in session:
        session['socot15phut'] = 3

    if "socot1tiet" not in session:
        session['socot1tiet'] = 3

    lop = dao.LoadLopEdHoc()

    return render_template("nhapdiem.html", dslopcheckbox=lop)


@app.route('/user/nhapdiem/loadmon/<malop>', methods=["POST"])
def loadmoninlop(malop):
    try:

        monhocs = dao.LoadMonHocOfLop(malop)

        monhocs = [{"TenMonHoc": monhoc[0]} for monhoc in monhocs]

        return jsonify({
            "success": True,
            "dsmonhoc": monhocs
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/user/nhapdiem/column15phut/<state>', methods=['PUT'])
def column15phut(state):
    try:

        socot15phut = session['socot15phut']

        if state == 'them':

            socot15phut = socot15phut + 1

            if socot15phut > 5:
                return jsonify({'success': False,
                                'error': "Tối đa 5 cột!"})

            session['socot15phut'] = int(socot15phut)

            session.modified = True


        else:

            socot15phut = socot15phut - 1

            if socot15phut < 1:
                return jsonify({'success': False,
                                'error': "Tối thiếu 1 cột!"})

            session['socot15phut'] = int(socot15phut)

            session.modified = True

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})


@app.route('/user/nhapdiem/column1tiet/<state>', methods=['PUT'])
def addcolumn1tiet(state):
    try:
        socot1tiet = session['socot1tiet']

        if state == 'them':

            socot1tiet = socot1tiet + 1

            if socot1tiet > 3:
                return jsonify({'success': False,
                                'error': "Tối đa 3 cột!"})

            session['socot1tiet'] = int(socot1tiet)

            session.modified = True

        else:

            socot1tiet = socot1tiet - 1

            if socot1tiet < 1:
                return jsonify({'success': False,
                                'error': "Tối thiểu 1 cột!"})

            session['socot1tiet'] = int(socot1tiet)

            session.modified = True

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})


@app.route('/user/nhapdiem/diemdshocsinh/<malop>/<monhoc>/<hocky>/<namhoc>/<state>', methods=['POST'])
def diemdshocsinh(malop, monhoc, hocky, namhoc, state):

    if malop in session:
        del session[malop]

        session.modified= True

    data = request.json
    diemdshocsinh = data.get("diemdshocsinh")
    diemdshocsinh.pop(0)


    mahocki = dao.GetHocKi(tenhocki=hocky, namhoc=namhoc.replace(" ", "")).MaHocKi

    mamonhoc = dao.GetMonHoc(tenmonhoc=monhoc).MaMonHoc

    if state == 'luu':

        for info in diemdshocsinh:
            dao.AddDiemHocSinhList(maHocSinh=info['maHocSinh'],
                                   mamonhoc=mamonhoc,
                                   mahocki=mahocki,
                                   typeDiem=dao.TypeDiem.PHUT15.value,
                                   diemListNew=info['diem15phut'])
            dao.AddDiemHocSinhList(maHocSinh=info['maHocSinh'],
                                   mamonhoc=mamonhoc,
                                   mahocki=mahocki,
                                   typeDiem=dao.TypeDiem.TIET1.value,
                                   diemListNew=info['diem1tiet'])

            if info.get('diemthi'):
                dao.AddDiemHocSinhList(
                    maHocSinh=info['maHocSinh'],
                    mamonhoc=mamonhoc,
                    mahocki=mahocki,
                    typeDiem=dao.TypeDiem.CUOIKI.value,
                    diemListNew=info['diemthi'].split(",")
                )
        return jsonify({'success': True,
                        'state': "Lưu thông tin thành công!"})
    else:

        if malop not in session:
            session[malop] = []

        for info in diemdshocsinh:
            if info.get('maHocSinh')  == 'subHeader':
                continue
            hs_diem = {
                        "MaHocSinh": info['maHocSinh'],
                        "HoTen": info['hoten'],
                        "15phut": info['diem15phut'],
                        "1tiet": info['diem1tiet'],
                        "diemthi": info['diemthi'].split(",")

                        }
            session[malop].append(hs_diem)


        session.modified= True
        for i in session[malop]:
            print(
                f"MaHocSinh: {i.get('MaHocSinh', 'N/A')}, "
                f"HoTen: {i.get('HoTen', 'N/A')}, "
                f"15phut: {i.get('15phut', 'N/A')}, "
                f"1tiet: {i.get('1tiet', 'N/A')}, "
                f"DiemThi: {i.get('diemthi', 'N/A')}"
            )


        return jsonify({'success': True,
                        'state': "Lưu thông tin thành công!"})


@app.route("/user/xuatdiem")
def xuatdiem():
    return render_template("xuatdiem.html")


@app.route('/user/dieuchinhdanhsachlop')
def dieuchinhdanhsachlop():
    if session.get('dshocsinhnotlop'):
        session.get('dshocsinhnotlop').clear()
        session.modified = True

    solop = len(dao.GetMaLop(dao.CurrentYear()))

    page = int(request.args.get('page', 1))

    malop = 'L10A' + str(page) + '_' + dao.CurrentYear()

    lophocsinh = dao.LoadLop(malop=malop, key="info")


    dshocsinhnotlop = dao.HocSinhNotLop()

    print(dshocsinhnotlop)

    return render_template("dieuchinhdanhsachlop.html", lophocsinh=lophocsinh,
                           solop=solop,
                           dshocsinhnotlop=dshocsinhnotlop,
                           lop='10A' + str(page))



@app.route('/user/dieuchinhdanhsachlop/addhocsinh/<hocsinhid>', methods=["POST"])
def savehocsinhtosession(hocsinhid):
    if "dshocsinhnotlop" not in session:
        session['dshocsinhnotlop'] = []

    if hocsinhid not in session.get('dshocsinhnotlop'):
        session['dshocsinhnotlop'].append(hocsinhid)

        session.modified = True

        return jsonify({"success": True})


@app.route('/user/dieuchinhdanhsachlop/addhocsinh/ds/<tenlop>', methods=["POST"])
def addhocsinhtolop(tenlop):
    try:

        for i in session['dshocsinhnotlop']:
            print(i)

        bool = dao.addHocSinhToLop(listmahocsinh = session.get("dshocsinhnotlop"), malop='L' + str(tenlop) + '_' + dao.CurrentYear())
        if not bool:
            return jsonify({"success": False, "error": "Lớp đã đầy!"})

        session.get('dshocsinhnotlop').clear()
        session.modified = True

        return jsonify({"success": True})

    except Exception as ex:
        return jsonify({"success": False, "error" : "Lớp đã đầy!"})


@app.route('/user/dieuchinhdanhsachlop/removehocsinh/<hocsinhid>', methods=["POST"])
def removehocsinhtosession(hocsinhid):
    for index, i in enumerate(session['dshocsinhnotlop']):
        if i == hocsinhid:
            session['dshocsinhnotlop'].pop(index)
            session.modified = True

            return jsonify({"success": True})


@app.route('/user/tiepnhanhocsinh', methods=["POST", "GET"])
def SaveInforHocSinh():
    if request.method == "POST":
        try:
            diemTbDauVao = float(request.form['diemTbDauVao'])
            avatar = request.files.get('avatar')
            sdt = list(request.form.getlist('sdt'))

            ngaysinh = request.form.get('ngaysinh')

            age = int(dao.CurrentYear()) - int(datetime.strptime(ngaysinh, '%Y-%m-%d').year)

            data = request.form.copy()

            if 15 <= age <= 20:
                del data['diemTbDauVao']
                del data['sdt']

                dao.add_HocSinh(diemTbDauVao=diemTbDauVao, sdt=sdt, avatar=avatar, **data)
                return render_template('tiepnhanhocsinh.html', mess="Lưu thông tin thành công!")
            else:
                return render_template('tiepnhanhocsinh.html', mess="Độ tuổi từ 15 đến 20!", **data)

        except Exception as ex:
            return render_template('tiepnhanhocsinh.html', mess=str(ex))
    return redirect(url_for('index'))


@app.route('/capnhatthongtin/<TenDangNhap>', methods=["POST", "GET"])
def UpdateInforUser(TenDangNhap):
    if request.method == "POST":

        permission = request.form.getlist('checkbox_permission')
        PermissionUser = []
        for i in permission:
            PermissionUser.append({dao.GetPerMission(i).Value: current_user.TenDangNhap})

        if permission:
            session["PermissionUser"] = PermissionUser
            return redirect(url_for('index'))
        else:
            error_mess = "Không có lựa chọn nào được chọn!"
            return render_template('capnhatthongtin.html', error_mess=error_mess, TenDangNhap=TenDangNhap)

    return render_template('capnhatthongtin.html', TenDangNhap=TenDangNhap)


@app.route('/approvepermission', methods=["PUT"])
def approvepermission():
    data = request.json

    permissionvalue = data.get("permissionvalue")
    username = data.get("username")

    permissionid = dao.GetPerMission(value=permissionvalue).PermissionID

    userid = dao.GetUserNameByID(username)

    success = dao.AddPermissionUser(permissionid=permissionid, userid=userid)

    for index, i in enumerate(session.get("PermissionUser")):
        for key in i.keys():

            if key == permissionvalue and i[key] == username:
                session["PermissionUser"].pop(index)
                break

    session.modified = True

    return jsonify({"success": success})


@app.route('/acctiveaccount', methods=["POST"])
def acctiveaccount():
    activeuser = request.json
    username = activeuser.get('username')

    dao.ActiveAccount(dao.GetUserNameByID(username))

    if username in session["activeaccount"]:
        session["activeaccount"].remove(username)
        session.modified = True

    return jsonify({"success": True})


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


@app.route('/user/uploaddanhsachhocsinh', methods=['POST'])
def uploaddanhsachhocsinh():
    if request.method == 'POST':

        file = request.files.get('file')

        if not file:
            return render_template('tiepnhanhocsinh.html', mess="Bạn chưa chọn file!")

        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            try:

                dic = utils.LoadFile(file)
                session["dshocsinh"] = dic

                page = request.args.get('page', 1)
                data_page = utils.Pagination_Data(session["dshocsinh"], int(page))

                return render_template('tiepnhanhocsinh.html',
                                       data=data_page['dic_page'],
                                       total_page=data_page['total_page']
                                       )

            except Exception as e:
                return render_template('tiepnhanhocsinh.html', mess=f"Lỗi khi xử lý file: {e}")
        else:
            return render_template('tiepnhanhocsinh.html',
                                   mess="File không đúng định dạng. Vui lòng upload file .xlsx hoặc .xls.")
    return render_template('tiepnhanhocsinh.html')


@app.route('/user/uploaddanhsachhocsinh')
def dividelistdshocsinh():
    page = request.args.get('page', 1)

    data_page = utils.Pagination_Data(session["dshocsinh"], int(page))

    return render_template('tiepnhanhocsinh.html',
                           data=data_page['dic_page'],
                           total_page=data_page['total_page'])


@app.route('/user/uploaddanhsachhocsinh/updatesdt', methods=["put"])
def updatesdthocsinh():
    data = request.json
    stt = data.get('STT')
    sdt = data.get('sdt')

    for i in session.get('dshocsinh'):
        if i['STT'] == stt:
            i['Số điện thoại'] = sdt
            session.modified = True
            return jsonify({"success": True})

    return jsonify({"success": True})


@app.route('/user/uploaddanhsachhocsinh/removehocsinh/<int:stt>', methods=['delete'])
def removedhocinfile(stt):
    for index, i in enumerate(session.get('dshocsinh')):
        if i['STT'] == stt:
            session['dshocsinh'].pop(index)
            session.modified = True
            return jsonify({"success": True})

    return jsonify({"success": False})


@app.route('/user/uploaddanhsachhocsinh/savedshocsinh', methods=["POST"])
def saveinforDshocsinh():
    # def add_HocSinh(diemTbDauVao, firstname, lastname, ngaysinh, gioitinh, diachi, email, sdt=None, avatar=None):

    try:
        for i in session.get('dshocsinh'):
            dao.add_HocSinh(diemTbDauVao=round(float(i['Điểm']), 1), firstname=i['Tên'], lastname=i['Họ'],
                            ngaysinh=i['Ngày sinh'], gioitinh=i['Giới tính'], diachi=i['Địa chỉ'],
                            email=i['Email'], sdt=i['Số điện thoại'].rsplit('/'))

        return jsonify({"success": True,
                        "error": "Lưu thành công!"})
    except Exception as e:
        return jsonify({"success": False,
                        "error": str(e)})


@app.route('/user/dieuchinhdanhsachlop/removehocsinh/<tenlop>/<mahocsinh>', methods=['post'])
def removehs(tenlop, mahocsinh):
    try:
        malop = 'L' + tenlop + '_' + dao.CurrentYear()

        res = dao.removeHocSinh(malop, mahocsinh)

        return jsonify({"success": res})

    except Exception as e:
        return jsonify({"success": False})


@app.route('/user/nhapdiem/lop', methods=['POST'])
def getinfolop():
    if request.method == 'POST':

        data = request.form.copy()

        mamonhoc = dao.GetMonHoc(tenmonhoc=data['monhoc']).MaMonHoc

        mahocki = dao.GetHocKi(tenhocki=data['hocky'], namhoc=data['namhoc'].replace(" ", "")).MaHocKi

        dslop = dao.LoadLopEdHoc()

        dshocsinh = []

        max15phut = 1
        max1tiet = 1

        if data['searchhocsinh']:

            hocsinhs = dao.GetHocSinhByTenHoTenEmailPhone(inputsearch = data['searchhocsinh'], malop=data['dslop'])

            for hs in hocsinhs:
                hs_diem = {
                    "UserID": hs['MaHocSinh'],
                    "HoTen": hs['HoTen'],
                    **dao.LoadHSinfo(hs['MaHocSinh'], key="diem",  mamonhoc=mamonhoc, mahocki=mahocki)
                }
                dshocsinh.append(hs_diem)

                max15phut = max(max15phut, len(hs_diem['15phut']))
                max1tiet = max(max1tiet, len(hs_diem['1tiet']))




        else:

            dshocsinh = dao.LoadLop(malop=data['dslop'], key="diem", mamonhoc=mamonhoc, mahocki=mahocki)


            max15phut = dshocsinh["max15phut"]
            max1tiet = dshocsinh["max1tiet"]

            if data['dslop'] not in session:
                dshocsinh = dshocsinh['diemdshocsinh']
            else:
                dshocsinh = session[data['dslop']]


        session['socot15phut'] = max15phut if max15phut > session['socot15phut'] else session['socot15phut']

        session['socot1tiet'] = max1tiet if max1tiet > session['socot1tiet'] else session['socot1tiet']

        session.modified = True


        return render_template('nhapdiem.html', dshocsinh=dshocsinh,
                                   dslopcheckbox=dslop, malop =data['dslop'],  **data)

    return redirect(url_for('index'))



# @app.route('user/nhapdiem/timkiemhocsinh')
# def nhapdiemtimkiemhocsinh():


@app.route("/user/baocaothongke")
def baocaothongke():
    danh_sach_mon_hoc = dao.Load_MonHoc()
    danh_sach_hoc_ki = dao.load_hoc_ki()

    return render_template("baocaothongke.html",danh_sach_mon_hoc=danh_sach_mon_hoc,danh_sach_hoc_ki=danh_sach_hoc_ki)

@app.route("/user/baocaothongke/submit",methods=["GET","POST"])
def submit():
    danh_sach_mon_hoc = dao.Load_MonHoc()
    danh_sach_hoc_ki = dao.load_hoc_ki()

    if request.method == 'POST':
        MonHoc = request.form.get('MonHoc')
        HocKi = request.form.get('HocKi')

        danh_sach_lop_hoc = dao.LoadLopHoc(MonHoc,HocKi)
        TenMonHoc = ""
        TenHocKi = ""
        TenNamHoc = ""
        ds_lop = []
        for MH in danh_sach_mon_hoc:
            if MonHoc == MH.MaMonHoc:
                TenMonHoc = MH.TenMonHoc
        for Hk in danh_sach_hoc_ki:
            if int(HocKi) == Hk.MaHocKi:
                TenHocKi = Hk.TenHocKi
                TenNamHoc = Hk.NamHoc

        stt = 0
        for lop in danh_sach_lop_hoc:
            stt += 1
            soluongdat = dao.tinh_so_luong_dat_cua_lop(lop.MaLop, MonHoc, HocKi)
            tile = round((soluongdat / lop.SiSo) * 100,2) if lop.SiSo != 0 else 0
            ds_lop.append([stt, lop.TenLop, lop.SiSo, soluongdat, tile])

    return  render_template("baocaothongke.html",danh_sach_mon_hoc=danh_sach_mon_hoc,danh_sach_hoc_ki=danh_sach_hoc_ki,TenMonHoc=TenMonHoc,TenHocKi=TenHocKi,TenNamHoc=TenNamHoc,Lop=ds_lop)


# @app.route('/user/nhapdiem/lop/search/<keyword>/<field>/<malop>', methods=['GET'])
# def search(keyword, field, malop):
#     if field == "lop":
#         lop = dao.LoadLopEdHoc()
#
#         dslop = [i.TenLop for i in lop]
#
#         print(dslop)
#
#         suggestionEdOfKeyword = utils.SuggestedLop(ds=dslop, keyword=keyword)
#
#         print(suggestionEdOfKeyword)
#
#     elif field == "monhoc":
#
#         monhocs = dao.LoadMonHocOfLop(malop)
#
#         # monhocs là list trong list - > chuyển về string trong list
#         monhocs = list(itertools.chain(*monhocs))
#
#         suggestionEdOfKeyword = utils.SuggestedLop(ds=monhocs, keyword=keyword)
#
#     return jsonify(suggestionEdOfKeyword)


@app.route('/user/danhsachlop')
def danhsachlop():
    solop = int(dao.SoLop((app.config["MAX_SS_LOP"])))

    page = int(request.args.get('page', 1))

    malop = 'L10A' + str(page) + '_' + dao.CurrentYear()

    lophocsinh = dao.LoadLop(malop=malop, key="info")

    dshocsinhnotlop = dao.HocSinhNotLop()

    return render_template("danhsachlop.html", lophocsinh=lophocsinh,
                           solop=solop,
                           dshocsinhnotlop=dshocsinhnotlop,
                           lop='10A' + str(page),
                           dskhoi=dao.LoadKhoiAll())


# @app.route('/user/nhapdiem/timkiemhocsinh', methods=['POST', 'GET'])
# def findhocsinh():
#
#     input = request.form.get('searchhocsinh')
#
#     return render_template("nhapdiem.html")


# @app.route('/user/danhsachlop/<makhoi>', methods = ['POST'])
# def loadlopofkhoi(makhoi):
#
#
#


@app.route('/user/dieuchinhdanhsachlop/sapxeptudau', methods = ['POST'])
def sapxeptudau():

    dao.RemoveDshocsinhAllOfCurrentyear()

    lapdanhsachlop()

    return jsonify({"success": True})



@app.route('/user/dieuchinhdanhsachlop/taolop/ds/<tenlop>', methods=['POST'])
def taolop(tenlop):

    for i in session.get('dshocsinhnotlop'):
        print(i)

    if session.get('dshocsinhnotlop'):

        dao.CreateLop(tenlop=tenlop, listhocsinh = session.get('dshocsinhnotlop'))
    else:
        listidhocsinh = [[info.UserID for info in hs] for hs in dao.HocSinhNotLop()]
        dao.CreateLop(tenlop= tenlop, listhocsinh = listidhocsinh)

    return jsonify({"success": True})



@app.route('/user/dieuchinhdanhsachlop/timkiem/dshocsinh', methods=['POST','GET'])
def timkkiemhocsinhalllop():
    if request.method == 'POST':
        textinput = request.form.get('textinput')

        currentyear = dao.CurrentYear()

        hocsinhs = dao.GetHocSinhByTenHoTenEmailPhone(inputsearch=textinput, namtaolop=currentyear)


        dshocsinh = [ dao.LoadHSinfo(hs['MaHocSinh'], key="info" , keytimkiem="timkiem") for hs in hocsinhs ]

        solop = len(dao.GetMaLop(dao.CurrentYear()))

        dshocsinhnotlop = dao.HocSinhNotLop()

        return render_template("dieuchinhdanhsachlop.html", lophocsinh=dshocsinh,
                               solop=solop, dshocsinhnotlop=dshocsinhnotlop,
                               key="timkiem", textinput = textinput)


@login.user_loader
def user_load(id):
    return dao.Get_User_By_ID(id=id)
# @app.route("/user/baocaothongke/load_mon_hoc/")
# def load_mon_hoc():
#
#     return render_template("/baocaothongke.html")

if __name__ == "__main__":
    from QUANLIHOCSINH.admin import *

    app.run(debug=True)
