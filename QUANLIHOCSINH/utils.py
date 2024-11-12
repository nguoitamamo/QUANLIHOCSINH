from argparse import Action
from tkinter import Image, image_names

from flask import session
from sqlalchemy import func
from sqlalchemy.orm.session import ACTIVE
from wtforms.validators import Email

from QUANLIHOCSINH import app, db
import models
import unidecode
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


def Load_Permission():
    permissons = (db.session.query(models.PermissionUser.UserID, models.Permission.Value)
                  .join(models.PermissionUser, models.Permission.PermissionID == models.PermissionUser.PermissionID)
                  .join( models.Account, models.Account.id == models.PermissionUser.UserID).all())

    return permissons



def Load_MonHoc():
    return models.MonHoc.query.all()


def Check_login(username, password):
    if username and password:
        passw = str( hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return models.Account.query.filter(
            models.Account.TenDangNhap.__eq__(username.strip()),
            models.Account.MatKhau.__eq__(passw.strip()),
            models.Account.Active.__eq__(True)
        ).first()


def convert_to_slug(input_string):
    # Chuyển sang không dấu
    no_accent_string = unidecode.unidecode(input_string)
    # Xóa khoảng trắng
    no_space_string = no_accent_string.replace(" ", "")
    return no_space_string.lower()

def Load_Permission_User(id):
    Role_user = []
    for role in Load_Permission():
        if role.UserID == id:
            Role_user.append({role.Value: convert_to_slug(role.Value)})
    return Role_user


def Get_User_By_ID(id):
    return models.Account.query.get(id)


def Get_Cnt_Accout_Current():
    return models.Account.query.count()
def ToAccountID():
    return "U" + str(Get_Cnt_Accout_Current())

def Get_MonHoc_By_TenMonHoc(TenMonHoc):
    monhoc = models.MonHoc.query.filter(models.MonHoc.TenMonHoc.__eq__(TenMonHoc)).first()
    return monhoc.MaMonHoc if monhoc else None


def Add_User(username, passw, ho, ten, ngaysinh, gioitinh, diachi, email,image,permission, TenMonHoc, sdt,*kwargs):
    passwrd = str(hashlib.md5(passw.strip().encode('utf-8')).hexdigest())
    IdUser = "U"+ str(Get_Cnt_Accout_Current() + 1)
    user = models.Account( id =IdUser,
                           TenDangNhap = username.strip(),
                           MatKhau = passwrd)
    db.session.add(user)
    inforuser = models.UserInfor(UserID = IdUser, Ho= ho.strip(), Ten= ten.strip(), NgaySinh = ngaysinh, GioiTinh= gioitinh, DiaChi = diachi.strip(), Email = email.strip(), Image = image)
    db.session.add(inforuser)
    if permission == "Giảng viên":
        giangvien = models.GiangVien(MaGiangVien = IdUser, MaMonHoc = Get_MonHoc_By_TenMonHoc(TenMonHoc) )
        db.session.add(giangvien)
    elif permission == "Admin":
        admin = models.Admin(UserID = IdUser)
        db.session.add(admin)
    else:
        nhanvien = models.NhanVienBoPhanKhac(UserID = IdUser)
        db.session.add(nhanvien)

    phone = models.Phone(Number = sdt , UserID = IdUser)
    db.session.add(phone)
    db.session.commit()




def Load_PermissionALL():
    return models.Permission.query.all()

def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))

def AddToken(value, email):
    token = models.Token (Value = value, Email= email)
    db.session.add(token)
    db.session.commit()

def GetToken(value):
    return models.Token.query.filter(models.Token.Value == value).first().Value
def Send_Email(PassConfirm, email_rec):

    email = "2251052130truong@ou.edu.vn"
    passw = "18072004@Hnt"
    email_send = email_rec
    mail_content = PassConfirm

    smtp_session  = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_session .starttls()
    smtp_session .login(email, passw)  #

    message = MIMEMultipart()
    message['From'] = email
    message['To'] = email_send
    message['Subject'] = "Mã xác nhận"
    message.attach(MIMEText(mail_content, 'plain'))

    smtp_session .sendmail(email, email_send, message.as_string())

    smtp_session .quit()
    print("Email đã được gửi thành công!")


def add_HocSinh(diemdauvao,ho, ten, ngaysinh, gioitinh, diachi, email,image, *kwargs):
    idac = "U"+ str(Get_Cnt_Accout_Current() + 1)
    hocsinh = models.HocSinh( MaHocSinh = idac, DiemTbDauVao = diemdauvao)
    db.session.add(hocsinh)
    password_hash = hashlib.md5("111".encode('utf-8')).hexdigest()
    accoutHocSinh = models.Account( id = idac, TenDangNhap = "HocSinh" + str(idac), MatKhau = password_hash, Active = False )
    db.session.add(accoutHocSinh)
    inforHocSinh = models.UserInfor(UserID = idac, Ho= ho, Ten= ten, NgaySinh = ngaysinh, GioiTinh= gioitinh, DiaChi = diachi, Email = email, Image = image)
    db.session.add(inforHocSinh)
    db.session.commit()

def Cnt_Sum_HocSinh_Not_Lop():
    so_luong_hoc_sinh_chua_co_lop = (
        db.session.query(func.count(models.HocSinh.MaHocSinh))
        .filter(models.HocSinh.MaHocSinh.notin_(
            db.session.query(models.LopHocSinh.MaHocSinh)
        ))
        .scalar()
    )
    return so_luong_hoc_sinh_chua_co_lop
def Cnt_Sum_Lop(khoi):
    return db.session.query(func.count(models.Lop.MaKhoi)).filter(models.Khoi.MaKhoi.__eq__(khoi)).scalar()


def HocSinhNotLop(tb):
    HocSinhNotLop = db.session.query(models.HocSinh) \
        .filter(models.HocSinh.MaHocSinh.notin_(
            db.session.query(models.LopHocSinh.MaHocSinh)
        )) \
        .order_by(models.HocSinh.DiemTbDauVao.desc()) \
        .limit(tb) \
        .all()
    return HocSinhNotLop

def Get_Sum_HS_Lop(malop):
    return db.session.query(func.count(models.LopHocSinh.MaHocSinh)).filter(models.LopHocSinh.MaLop.__eq__(malop)).scalar()


def Insert_HS_Remain(sohocsinhconlai, solopcanchia, tb, remaining):
    if sohocsinhconlai <= 0 or not remaining:
        return 0

    condition = int(40 - tb)
    if len(remaining) >= condition:
        for i in range(1, condition + 1):
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh)
            db.session.add(lophocsinh)
    else:
        for i in range(1, len(remaining) + 1):
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh)
            db.session.add(lophocsinh)

    db.session.commit()
    sohocsinhconlai = sohocsinhconlai -  int(min(condition, len(remaining)))
    print(sohocsinhconlai)
    remaining = HocSinhNotLop(sohocsinhconlai) if sohocsinhconlai > 0 else []
    print(len(remaining))
    return Insert_HS_Remain(sohocsinhconlai, solopcanchia - 1, tb, remaining)

def Division_Class(solopcanchia):

    tb = Cnt_Sum_HocSinh_Not_Lop() / solopcanchia
    if tb >= 40:
        return 0
    for i in range(1, solopcanchia + 1):
        lop = models.Lop(MaLop="L10A" + str(i), TenLop="10a" + str(i), SiSo=40, MaKhoi="1")
        db.session.add(lop)
        db.session.commit()
        HocSinh = HocSinhNotLop(int(tb))
        for j in HocSinh:
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(i), MaHocSinh=j.MaHocSinh)
            db.session.add(lophocsinh)
        db.session.commit()
    remaining = HocSinhNotLop(Cnt_Sum_HocSinh_Not_Lop())
    print(len(remaining))
    if len(remaining) >=0:
        Insert_HS_Remain(len(remaining), int(solopcanchia), int(tb), remaining)



# Ho = [ "Huỳnh", "Nguyễn", "Thanh", "La" ]
# Ten =["Trương", "Trình", "A", "D"]
#
# def them():
#     for i in range(104,455):
#         hocsinh = models.HocSinh(MaHocSinh = "U" + str(i), DiemTbDauVao = float(random.randint(1,10)))
#         db.session.add(hocsinh)
#         password_hash = hashlib.md5(str(i).encode('utf-8')).hexdigest()
#         accoutHocSinh = models.Account(id="U" + str(i), TenDangNhap="HocSinh" + str(i), MatKhau=password_hash, Active=False)
#         db.session.add(accoutHocSinh)
#         inforHocSinh = models.UserInfor(UserID="U" + str(i), Ho=Ho[(i%4)], Ten=Ten[(i%4)], NgaySinh="2024-11-12", GioiTinh="Nam",DiaChi="Bình định", Email="hocsinh" + str(i) + "@gmail.com", Image=None)
#         db.session.add(inforHocSinh)
#         db.session.commit()
#
#     return 0

# def them():
#     for i in range(1, 11):
#         lop = models.Lop( MaLop = "L10A" + str(i) , TenLop = "10A" + str(i) , SiSo = 40 , MaKhoi =1 )
#         db.session.add(lop)
#
#     db.session.commit()





if __name__ == '__main__':
    with app.app_context():
        print(Cnt_Sum_HocSinh_Not_Lop())



