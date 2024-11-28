from itertools import count
from math import ceil

from sqlalchemy import func
from QUANLIHOCSINH import app, db
import models
import unidecode
import hashlib
import cloudinary
from cloudinary import uploader
from datetime import datetime
from enum import Enum
from sqlalchemy import or_
import random


def Load_Permission():
    permissons = (db.session.query(models.PermissionUser.UserID, models.Permission.Value)
                  .join(models.PermissionUser, models.Permission.PermissionID == models.PermissionUser.PermissionID)
                  .join(models.Account, models.Account.id == models.PermissionUser.UserID).all())

    return permissons


def Load_MonHoc():
    return models.MonHoc.query.all()


def Check_login(username, password):
    if username and password:
        passw = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return models.Account.query.filter(
            models.Account.TenDangNhap.__eq__(username.strip()),
            models.Account.MatKhau.__eq__(passw.strip()),
            models.Account.Active.__eq__(True)
        ).first()


def Check_Email(email):
    userinfor = models.UserInfor.query.filter(models.UserInfor.Email.__eq__(email)).first()
    return userinfor


def UpdatePassAccount(email, passnew):
    acc = models.Account.query.filter(models.Account.id.__eq__(Check_Email(email).UserID)).first()

    if acc:
        pass_new_maHoa = hashlib.md5(passnew.encode('utf-8')).hexdigest()

        acc.MatKhau = pass_new_maHoa

        db.session.commit()


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


def Check_Username_Exits(username):
    return models.Account.query.filter(models.Account.TenDangNhap.__eq__(username)).first()


def Add_User(username, password, lastname, fristname, ngaysinh, gioitinh, diachi, email, permission, sdt: list[str],
             monhoc=None, avatar=None):
    passwrd = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))

    user = models.Account(id=idac,
                          TenDangNhap=username.strip(),
                          MatKhau=passwrd)

    if permission == "Giảng viên" and monhoc:
        user.role = models.Role.GiangVien
        giangvien = models.GiangVien(MaGiangVien=idac, MaMonHoc=Get_MonHoc_By_TenMonHoc(monhoc))
        db.session.add(giangvien)

    else:
        user.role = models.Role.NhanvienBoPhanKhac

    db.session.add(user)

    inforuser = models.UserInfor(UserID=idac, Ho=lastname.strip(), Ten=fristname.strip(), NgaySinh=ngaysinh,
                                 GioiTinh=gioitinh,
                                 DiaChi=diachi.strip(), Email=email.strip())

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        inforuser.Image = res.get('secure_url')

    db.session.add(inforuser)

    if sdt:
        for i in sdt:
            phone = models.Phone(Number=str(i), UserID=idac)
            db.session.add(phone)

    db.session.commit()


def ActiveAccount(id):
    acc = models.Account.query.get(id)
    if acc:
        acc.Active = True
        db.session.commit()


def Load_PermissionALL():
    return models.Permission.query.all()


def Load_LopALL():
    return models.Lop.query.all()


def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))


def AddToken(value, email):
    token = models.Token(Value=value, Email=email)
    db.session.add(token)
    db.session.commit()


def GetToken(value):
    res = models.Token.query.filter(models.Token.Value.__eq__(value)).first()
    return res if res else None


def LoadEmailConfirm(value):
    return models.Token.query.filter(models.Token.Value.__eq__(value)).first().Email


def add_HocSinh(diemTbDauVao, firstname, lastname, ngaysinh, gioitinh, diachi, email, sdt=None, avatar=None):
    idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))

    hocsinh = models.HocSinh(MaHocSinh=idac, DiemTbDauVao=diemTbDauVao)
    db.session.add(hocsinh)

    password_hash = hashlib.md5(idac.encode('utf-8')).hexdigest()

    accoutHocSinh = models.Account(id=idac, TenDangNhap="HocSinh" + str(idac), MatKhau=password_hash,
                                   role=models.Role.HocSinh)
    db.session.add(accoutHocSinh)

    inforHocSinh = models.UserInfor(UserID=idac, Ho=firstname, Ten=lastname, NgaySinh=ngaysinh, GioiTinh=gioitinh,
                                    DiaChi=diachi,
                                    Email=email)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        inforHocSinh.Image = res.get('secure_url')

    db.session.add(inforHocSinh)

    if sdt:
        for i in sdt:
            phone = models.Phone(Number=str(i), UserID=idac)
            db.session.add(phone)

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


def HocSinhNotLop(tb=None):
    if tb:
        HocSinhNotLop = db.session.query(models.HocSinh).filter(models.HocSinh.MaHocSinh.notin_(
            db.session.query(models.LopHocSinh.MaHocSinh)
        )).order_by(models.HocSinh.DiemTbDauVao.desc()).limit(tb).all()
    else:
        HocSinhNotLop = db.session.query(models.HocSinh).filter(models.HocSinh.MaHocSinh.notin_(
            db.session.query(models.LopHocSinh.MaHocSinh)
        )).order_by(models.HocSinh.DiemTbDauVao.desc()).all()

        HocSinhNotLop = [LoadHSinfo(hs.MaHocSinh, key="info") for hs in HocSinhNotLop]

    return HocSinhNotLop


def Get_Sum_HS_Lop(malop):
    return db.session.query(func.count(models.LopHocSinh.MaHocSinh)).filter(
        models.LopHocSinh.MaLop.__eq__(malop)).scalar()


def UpdateSiSo(MaLop, SiSo):
    lop = db.session.query(models.Lop).filter(models.Lop.MaLop == MaLop).first()

    if lop:
        si_so = db.session.query(func.count(models.LopHocSinh.MaHocSinh)).filter(
            models.LopHocSinh.MaLop == MaLop).scalar()

        lop.SiSo = SiSo

        db.session.commit()


def Insert_HS_Remain(sohocsinhconlai, solopcanchia, tb, remaining):
    if sohocsinhconlai <= 0 or not remaining:
        return 0

    siso = app.config["MAX_SS_LOP"]
    condition = int(siso - tb)
    remaining.reverse()

    if len(remaining) >= condition:
        for i in range(1, condition + 1):
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
                                           NamTaoLop="2024")
            UpdateSiSo(MaLop="L10A" + str(solopcanchia), SiSo=siso)
            db.session.add(lophocsinh)
    else:
        for i in range(1, len(remaining) + 1):
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
                                           NamTaoLop="2024")
            UpdateSiSo(MaLop="L10A" + str(solopcanchia), SiSo=int(tb + len(remaining)))
            db.session.add(lophocsinh)

    db.session.commit()
    sohocsinhconlai = sohocsinhconlai - int(min(condition, len(remaining)))

    remaining = HocSinhNotLop(sohocsinhconlai) if sohocsinhconlai > 0 else []

    return Insert_HS_Remain(sohocsinhconlai, solopcanchia - 1, tb, remaining)


def Division_Class(solopcanchia):
    tb = Cnt_Sum_HocSinh_Not_Lop() / solopcanchia

    if tb >= app.config["MAX_SS_LOP"]:
        return 0

    for i in range(1, solopcanchia + 1):
        lop = models.Lop(MaLop="L10A" + str(i), TenLop="10A" + str(i), SiSo=int(tb), MaKhoi="1")
        db.session.add(lop)
        db.session.commit()

        HocSinh = HocSinhNotLop(int(tb))
        for j in HocSinh:
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(i), MaHocSinh=j.MaHocSinh, NamTaoLop="2024")
            db.session.add(lophocsinh)

        db.session.commit()

    remaining = HocSinhNotLop(Cnt_Sum_HocSinh_Not_Lop())

    if len(remaining) >= 0:
        Insert_HS_Remain(len(remaining), int(solopcanchia), int(tb), remaining)


def GetPerMissionByValue(value):
    return models.Permission.query.filter(models.Permission.Value.__eq__(value)).first().PermissionID


def GetPerMission(id=None, value=None):
    if id:
        return models.Permission.query.filter(models.Permission.PermissionID.__eq__(id)).first()
    if value:
        return models.Permission.query.filter(models.Permission.Value.__eq__(value)).first()


def GetUserNameByID(username):
    return models.Account.query.filter(models.Account.TenDangNhap.__eq__(username)).first().id


def GetLopByTen(tenLop):
    return db.session.query(models.Lop.TenLop, models.Lop.SiSo, models.Lop.MaLop).filter(
        models.Lop.TenLop == tenLop).first()


def GetMonHoc(mamonhoc=None, tenmonhoc=None):
    return (
        db.session.query(models.MonHoc.TenMonHoc, models.MonHoc.MaMonHoc)
        .filter(
            or_(
                models.MonHoc.MaMonHoc == mamonhoc,
                models.MonHoc.TenMonHoc == tenmonhoc
            )
        )
        .first()
    )


def GetHocKi(tenhocki, namhoc):
    return db.session.query(models.HocKi.MaHocKi).filter(models.HocKi.TenHocKi == tenhocki,
                                                         models.HocKi.NamHoc == namhoc).first()


def CheckPermissionUserExit(permissionid, userid):
    return models.PermissionUser.query.filter(models.PermissionUser.PermissionID == permissionid,
                                              models.PermissionUser.UserID == userid).first()


def AddPermissionUser(permissionid, userid):
    if not CheckPermissionUserExit(permissionid, userid):
        perrmissionuser = models.PermissionUser(PermissionID=permissionid, UserID=userid)
        db.session.add(perrmissionuser)
        db.session.commit()
        return True

    return False


def GetUserInforByUserID(userid):
    return db.session.query(models.UserInfor.Ho, models.UserInfor.Ten).filter(models.UserInfor.UserID == userid).first()


class TypeDiem(Enum):
    PHUT15 = "15 phút"
    TIET1 = "1 tiết"
    CUOIKI = "cuối kì"


def LoadLop(ma, key, page, mamonhoc=None, mahocki=None):
    lop_hocsinh = {}

    hocsinh = (db.session.query(models.LopHocSinh.MaLop, models.LopHocSinh.MaHocSinh)
               .join(models.HocSinh, models.HocSinh.MaHocSinh == models.LopHocSinh.MaHocSinh)
               .filter(models.LopHocSinh.MaLop == 'L' + ma + str(page))
               .all())

    if key == "info":
        lop_hocsinh[ma + str(page)] = [LoadHSinfo(mahocsinh=hs.MaHocSinh, key="info") for hs in hocsinh]
        return lop_hocsinh
    if key == "diem" and mamonhoc:

        max15phut = 0
        max1tiet = 0

        diemdshocsinh = []
        for hs in hocsinh:
            hs_diem = {
                "MaHocSinh" : hs.MaHocSinh,
                "HoTen": GetUserInforByUserID(hs.MaHocSinh),
                **LoadHSinfo(hs.MaHocSinh, key="diem", typediem=TypeDiem, mamonhoc=mamonhoc, mahocki=mahocki)
            }
            diemdshocsinh.append(hs_diem)

            max15phut = max(max15phut, len(hs_diem['15phut']))
            max1tiet = max(max1tiet, len(hs_diem['1tiet']))

        return {
            "diemdshocsinh": diemdshocsinh,
            "max15phut": max15phut,
            "max1tiet": max1tiet
        }


def LoadHSinfo(mahocsinh, key, typediem=TypeDiem, mamonhoc=None, mahocki=None):
    if key == "info":
        inforhocsinh = (db.session.query(models.UserInfor.UserID, models.UserInfor.Ho, models.UserInfor.Ten,
                                         models.HocSinh.DiemTbDauVao, models.UserInfor.GioiTinh,
                                         models.UserInfor.NgaySinh, models.UserInfor.DiaChi)
                        .join(models.Account, models.Account.id == models.UserInfor.UserID)
                        .join(models.HocSinh, models.HocSinh.MaHocSinh == models.Account.id)
                        .filter(models.UserInfor.UserID == mahocsinh)
                        .all())
        return inforhocsinh

    if key == "diem" and typediem:

        diem15phut = []
        diem1tiet = []
        cuoiki = []

        inforhocsinh = (db.session.query(models.HocSinh.MaHocSinh, models.Diem.TypeDiem, models.Diem.SoDiem,
                                         models.Diem.MaMonHoc, models.Diem.MaHocKi)
                        .join(models.Diem, models.HocSinh.MaHocSinh == models.Diem.MaHocSinh)
                        .filter(models.HocSinh.MaHocSinh == mahocsinh, models.Diem.TypeDiem.in_([TypeDiem.PHUT15.value,
                                                                                                 TypeDiem.TIET1.value,
                                                                                                 TypeDiem.CUOIKI.value]),
                                models.Diem.MaMonHoc == mamonhoc,
                                models.Diem.MaHocKi == mahocki)
                        .all())

        for diem in inforhocsinh:

            if diem.TypeDiem == TypeDiem.PHUT15.value:
                diem15phut.append(diem.SoDiem)
            elif diem.TypeDiem == TypeDiem.TIET1.value:
                diem1tiet.append(diem.SoDiem)
            elif diem.TypeDiem == TypeDiem.CUOIKI.value:
                cuoiki.append(diem.SoDiem)

        return {
            "15phut": diem15phut,
            "1tiet": diem1tiet,
            "diemthi": cuoiki
        }

    return None


#
# def LoadHSinfo(mahocsinh, key="diem"):
#     inforhocsinh = (db.session.query(models.HocSinh.MaHocSinh, models.Diem.TypeDiem, models.Diem.SoDiem,
#                                      models.Diem.MaMonHoc, models.Diem.MaHocKi)
#                     .join(models.Diem, models.HocSinh.MaHocSinh == models.Diem.MaHocSinh)
#                     .filter(models.HocSinh.MaHocSinh == mahocsinh)
#                     .all())
#
#     return inforhocsinh


def removeHocSinh(malop, mahocsinh):
    hocsinh = models.LopHocSinh.query.filter(
        models.LopHocSinh.MaLop == malop,
        models.LopHocSinh.MaHocSinh == mahocsinh
    ).first()

    if hocsinh:
        db.session.delete(hocsinh)
        db.session.commit()
        return True
    return False


def CheckHocSinhExitsLop(mahocsinh, malop):
    return models.LopHocSinh.query.filter(models.LopHocSinh.MaHocSinh == mahocsinh,
                                          models.LopHocSinh.MaLop == malop).first()


def addHocSinhToLop(mahocsinh, malop):
    currentyear = str(datetime.now().year)
    lophocsinh = models.LopHocSinh(MaHocSinh=mahocsinh, MaLop=malop, NamTaoLop=currentyear)
    db.session.add(lophocsinh)
    db.session.commit()
    return True


def SoLop(maxsslop):
    currentyear = str(datetime.now().year)
    return ceil((db.session.query(models.LopHocSinh.NamTaoLop == currentyear).count()) / maxsslop)


def Solop1(maxsslop):
    currentyear = str(datetime.now().year)
    return (db.session.query(models.LopHocSinh.NamTaoLop == currentyear).count()) / maxsslop


def LoadMonHocOfLop(tenlop):
    malop = GetLopByTen(tenlop).MaLop

    if not malop:
        return []

    return (db.session.query(models.Hoc.MaLop, models.Hoc.MaMonHoc, models.Hoc.MaHocKi)
            .filter(models.Hoc.MaLop == malop)
            .all())


Ho = ["Phan", "Ly", "Thanh", "La", "Hoang"]
Ten = ["Trung", "Trinh", "A", "D", "E", "G", "B"]


def them():
    for i in range(1, 425):
        idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))
        hocsinh = models.HocSinh(MaHocSinh=idac, DiemTbDauVao=float(random.randint(1, 10)))
        db.session.add(hocsinh)

        password_hash = hashlib.md5(str(i).encode('utf-8')).hexdigest()

        accoutHocSinh = models.Account(id=idac, TenDangNhap="HocSinhmoi" + str(i), MatKhau=password_hash,
                                       role=models.Role.HocSinh)
        db.session.add(accoutHocSinh)

        inforHocSinh = models.UserInfor(UserID=idac, Ho=Ho[(i % 5)], Ten=Ten[(i % 7)], NgaySinh="2008-11-12",
                                        GioiTinh="Nam", DiaChi="Bình định", Email="test" + str(i) + "@gmail.com",
                                        Image=None)
        db.session.add(inforHocSinh)

        db.session.commit()


# c
#     for i in range(1, 11):
#         lop = models.Lop( MaLop = "L10A" + str(i) , TenLop = "10A" + str(i) , SiSo = 40 , MaKhoi =1 )
#         db.session.add(lop)
#
#     db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        lop_hocsinh = LoadLop(ma="10A", key="diem", mamonhoc = 'MH1', page=2, mahocki=1)


        if lop_hocsinh and 'diemdshocsinh' in lop_hocsinh:
            for hs in lop_hocsinh['diemdshocsinh']:
                print(f"Họ tên: {hs['HoTen']}")

                for i in hs.get('15phut', []):
                    print(f"Điểm 15 phút: {i}")

                for i in hs.get('1tiet', []):
                    print(f"Điểm 1 tiết: {i}")

                for i in hs.get('diemthi', []):
                    print(f"Điểm cuối kỳ: {i}")


            print(f"Max 15 phút: {lop_hocsinh['max15phut']}")
            print(f"Max 1 tiết: {lop_hocsinh['max1tiet']}")
        else:
            print("Không có dữ liệu học sinh.")

            # # In ra thông tin
            # print(f"Họ tên: {ho_ten['Ho']} {ho_ten['Ten']}")
            # print("Điểm 15 phút:", diem_15phut)
            # print("Điểm 1 tiết:", diem_1tiet)
            # print("Điểm cuối kỳ:", diem_cuoiki)
            # print("-" * 20)

        # for info in hs:
        #     # print(
        #         # f" Mã học sinh: {info.UserID} ,Họ: {info.Ho}, Tên: {info.Ten}, Giới tính: {info.GioiTinh}, Ngày sinh: {info.NgaySinh}, Địa chỉ: {info.DiaChi}")
        #
        #     print(f"Họ: {info.HoTen},  MaHocSinh: {info.MaHocSinh} , Điểm: {info.SoDiem}, Loại điểm : {info.TypeDiem} ")
        # dshocsinh = HocSinhNotLop()
        #
        # for i in dshocsinh:
        #     for info in i:
        #         print(
        #             f" Mã học sinh: {info.UserID} ,Họ: {info.Ho}, Điểm: {info.DiemTbDauVao} Tên: {info.Ten}, Giới tính: {info.GioiTinh}, Ngày sinh: {info.NgaySinh}, Địa chỉ: {info.DiaChi}")

        # print(Solop1(40))
        # print(LoadMonHocOfLop('10A1'))
        # print(GetLopByID('L' + '10A1').MaLop)

        # for i in LoadHSinfo('HS0_92', key = "diem" ):
        #     print(i)

        # print(LoadHSinfo('HS0_92' , key = "info"))

        # print(GetMonHoc(mamonhoc = 'MH1').TenMonHoc)
        # for ten_lop, danh_sach_hoc_sinh in lop_hocsinh.items():
        #
        #     print(f"Lớp: {ten_lop}")
        #
        #     for hs in danh_sach_hoc_sinh:
        #         for info in hs:
        #             print(
        #                          f" Mã học sinh: {info.UserID} ,Họ: {info.Ho}, Tên: {info.Ten}, Giới tính: {info.GioiTinh}, Ngày sinh: {info.NgaySinh}, Địa chỉ: {info.DiaChi}")
        #
        # #
