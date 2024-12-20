from itertools import count
from math import ceil
from models import Permission, PermissionUser, Account, Role, Lop, LopHocSinh, MonHoc, UserInfor, Diem, HocSinh, HocKi, \
    GiangVien, Phone, Hoc, Token, Khoi
from flask_sqlalchemy.model import Model
from sqlalchemy import func
from QUANLIHOCSINH import app, db
import models
import unidecode
import hashlib
import cloudinary
from cloudinary import uploader
from datetime import datetime
from enum import Enum
from sqlalchemy import or_, and_
import random


def CurrentYear():
    return str(datetime.now().year)


def Load_Permission():
    permissons = (db.session.query(PermissionUser.UserID, Permission.Value)
                  .join(PermissionUser, Permission.PermissionID == PermissionUser.PermissionID)
                  .join(Account, Account.id == PermissionUser.UserID).all())

    return permissons


def Load_MonHoc():
    return MonHoc.query.all()


def load_hoc_ki():
    return HocKi.query.all()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    A = Account.query.filter(Account.TenDangNhap.__eq__(username.strip()),
                             Account.MatKhau.__eq__(password))
    if role:
        A = A.filter(Account.role.__eq__(Role.Admin))

    return A.first()


def them():
    idac = "Admin123"
    password_hash = str(hashlib.md5("123".encode('utf-8')).hexdigest())

    user = Account(id=idac,
                   TenDangNhap="Admin",
                   MatKhau=password_hash,
                   Active=True,
                   role=Role.Admin)

    db.session.add(user)

    inforHocSinh = UserInfor(UserID=idac, Ho="Phan", Ten="Thanh Trinh", NgaySinh="2004-12-11",
                             GioiTinh="Nam", DiaChi="Bình định", Email="2251052129trinh@ou.edu.vn",
                             Image=None)
    db.session.add(inforHocSinh)

    db.session.commit()


def Check_login(username, password):
    if username and password:
        passw = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return Account.query.filter(
            Account.TenDangNhap.__eq__(username.strip()),
            Account.MatKhau.__eq__(passw.strip()),
            Account.Active.__eq__(True)
        ).first()


def Check_Email(email):
    userinfor = UserInfor.query.filter(UserInfor.Email.__eq__(email)).first()
    return userinfor


def UpdatePassAccount(email, passnew):
    acc = Account.query.filter(Account.id.__eq__(Check_Email(email).UserID)).first()

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
    return Account.query.get(id)


def Get_Cnt_Accout_Current():
    return Account.query.count()


def ToAccountID():
    return "U" + str(Get_Cnt_Accout_Current())


def Get_MonHoc_By_TenMonHoc(TenMonHoc):
    monhoc = MonHoc.query.filter(MonHoc.TenMonHoc.__eq__(TenMonHoc)).first()
    return monhoc.MaMonHoc if monhoc else None


def Check_Username_Exits(username):
    return Account.query.filter(Account.TenDangNhap.__eq__(username)).first()


def Add_User(username, password, lastname, fristname, ngaysinh, gioitinh, diachi, email, permission, sdt: list[str],
             monhoc=None, avatar=None):
    passwrd = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))

    user = Account(id=idac,
                   TenDangNhap=username.strip(),
                   MatKhau=passwrd)

    if permission == "Giảng viên" and monhoc:
        user.role = Role.GiangVien
        giangvien = GiangVien(MaGiangVien=idac, MaMonHoc=Get_MonHoc_By_TenMonHoc(monhoc))
        db.session.add(giangvien)

    else:
        user.role = Role.NhanvienBoPhanKhac

    db.session.add(user)

    inforuser = UserInfor(UserID=idac, Ho=lastname.strip(), Ten=fristname.strip(), NgaySinh=ngaysinh,
                          GioiTinh=gioitinh,
                          DiaChi=diachi.strip(), Email=email.strip())

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        inforuser.Image = res.get('secure_url')

    db.session.add(inforuser)

    if sdt:
        for i in sdt:
            phone = Phone(Number=str(i), UserID=idac)
            db.session.add(phone)

    db.session.commit()


def ActiveAccount(id):
    acc = Account.query.get(id)
    if acc:
        acc.Active = True
        db.session.commit()


def Load_PermissionALL():
    return Permission.query.all()


def LoadLopEdHoc():
    return (
        db.session.query(Lop.MaLop, Lop.TenLop)
        .join(Hoc, Hoc.MaLop == Lop.MaLop)
        .distinct()
        .all()
    )


def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))


def AddToken(value, email):
    token = Token(Value=value, Email=email)
    db.session.add(token)
    db.session.commit()


def GetToken(value):
    res = Token.query.filter(Token.Value.__eq__(value)).first()
    return res if res else None


def LoadEmailConfirm(value):
    return Token.query.filter(Token.Value.__eq__(value)).first().Email


def LoadKhoi(makhoi=None):
    if makhoi:
        return db.session.query(Khoi.TenKhoi).filter(Khoi.MaKhoi == makhoi).first().TenKhoi
    else:
        return db.session.query(Khoi.TenKhoi, Khoi.MaKhoi).all()


def add_HocSinh(diemTbDauVao, firstname, lastname, ngaysinh, gioitinh, diachi, email, sdt=None, avatar=None):
    idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))

    hocsinh = HocSinh(MaHocSinh=idac, DiemTbDauVao=diemTbDauVao)
    db.session.add(hocsinh)

    password_hash = hashlib.md5(idac.encode('utf-8')).hexdigest()

    accoutHocSinh = Account(id=idac, TenDangNhap="HocSinh" + str(idac), MatKhau=password_hash,
                            role=Role.HocSinh)
    db.session.add(accoutHocSinh)

    inforHocSinh = UserInfor(UserID=idac, Ho=firstname, Ten=lastname, NgaySinh=ngaysinh, GioiTinh=gioitinh,
                             DiaChi=diachi,
                             Email=email)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        inforHocSinh.Image = res.get('secure_url')

    db.session.add(inforHocSinh)

    if sdt:
        for i in sdt:
            phone = Phone(Number=str(i), UserID=idac)
            db.session.add(phone)

    db.session.commit()


def Cnt_Sum_HocSinh_Not_Lop():
    so_luong_hoc_sinh_chua_co_lop = (
        db.session.query(func.count(HocSinh.MaHocSinh))
        .filter(HocSinh.MaHocSinh.notin_(
            db.session.query(LopHocSinh.MaHocSinh)
        ))
        .scalar()
    )
    return so_luong_hoc_sinh_chua_co_lop


def Cnt_Sum_Lop(khoi):
    return db.session.query(func.count(Lop.MaKhoi)).filter(Khoi.MaKhoi.__eq__(khoi)).scalar()


def HocSinhNotLop(tb=None):
    if tb:
        HocSinhNotLop = db.session.query(HocSinh).filter(HocSinh.MaHocSinh.notin_(
            db.session.query(LopHocSinh.MaHocSinh)
        )).order_by(HocSinh.DiemTbDauVao.desc()).limit(tb).all()
    else:
        HocSinhNotLop = db.session.query(HocSinh).filter(HocSinh.MaHocSinh.notin_(
            db.session.query(LopHocSinh.MaHocSinh)
        )).order_by(HocSinh.DiemTbDauVao.desc()).all()

        HocSinhNotLop = [LoadHSinfo(hs.MaHocSinh, key="info") for hs in HocSinhNotLop]

    return HocSinhNotLop


def Get_Sum_HS_Lop(malop):
    return db.session.query(func.count(LopHocSinh.MaHocSinh)).filter(
        LopHocSinh.MaLop.__eq__(malop)).scalar()


# def count_loai_diem(type_diem,ma_hoc_sinh, ma_mon_hoc, ma_hoc_ki):
#     count = db.session.query(func.count(Diem.DiemID)).filter(
#        Diem.TypeDiem == type_diem,
#        Diem.MaHocSinh == ma_hoc_sinh,
#         Diem.MaMonHoc == ma_mon_hoc,
#         Diem.MaHocKi == ma_hoc_ki
#     ).a
#     return count
def tinh_diem_trung_binh(diem_15_phut, diem_1_tiet, diem_cuoi_ki):
    # Tính tổng điểm
    tong_diem = sum(diem_15_phut) * 1 + sum(diem_1_tiet) * 2 + diem_cuoi_ki * 3
    tong_trong_so = len(diem_15_phut) * 1 + len(diem_1_tiet) * 2 + 3  # Tổng trọng số

    # Tính điểm trung bình
    diem_trung_binh = tong_diem / tong_trong_so
    return round(diem_trung_binh, 2)


def Tinh_Diem_Trung_Binh_Mon_Hoc_Sinh(MaHocSinh, MaMonHoc, MaHocKi):
    # Lấy tất cả các điểm của học sinh, môn học và học kỳ chỉ trong một lần truy vấn
    diem = db.session.query(Diem.TypeDiem, Diem.SoDiem).filter(
        Diem.MaHocSinh == MaHocSinh,
        Diem.MaMonHoc == MaMonHoc,
        Diem.MaHocKi == MaHocKi
    ).all()

    # Phân loại điểm dựa trên TypeDiem
    diem_15_phut = [float(d[1]) for d in diem if d[0] == "15 phút"]
    diem_1_tiet = [float(d[1]) for d in diem if d[0] == "1 tiết"]
    diem_cuoi_ki = next((float(d[1]) for d in diem if d[0] == "cuối kì"), 0.0)

    # Tính điểm trung bình
    return float(tinh_diem_trung_binh(diem_15_phut, diem_1_tiet, diem_cuoi_ki))


def tinh_so_luong_dat_cua_lop(MaLop, MaMonHoc, MaHocKi):
    # Lấy danh sách học sinh trong lớp
    ds_hoc_sinh = db.session.query(LopHocSinh.MaHocSinh).filter(
        LopHocSinh.MaLop == MaLop
    ).all()

    # Chuyển danh sách học sinh thành một danh sách các mã học sinh
    ma_hoc_sinh_list = [hs[0] for hs in ds_hoc_sinh]

    # Lấy tất cả điểm của các học sinh trong lớp cho môn học và học kỳ
    diem = db.session.query(Diem.MaHocSinh, Diem.TypeDiem, Diem.SoDiem).filter(
        Diem.MaHocSinh.in_(ma_hoc_sinh_list),
        Diem.MaMonHoc == MaMonHoc,
        Diem.MaHocKi == MaHocKi
    ).all()

    # Phân loại điểm theo học sinh
    diem_theo_hoc_sinh = {}
    for ma_hs, type_diem, so_diem in diem:
        if ma_hs not in diem_theo_hoc_sinh:
            diem_theo_hoc_sinh[ma_hs] = {"15 phút": [], "1 tiết": [], "cuối kì": 0.0}
        if type_diem == "15 phút":
            diem_theo_hoc_sinh[ma_hs]["15 phút"].append(float(so_diem))
        elif type_diem == "1 tiết":
            diem_theo_hoc_sinh[ma_hs]["1 tiết"].append(float(so_diem))
        elif type_diem == "cuối kì":
            diem_theo_hoc_sinh[ma_hs]["cuối kì"] = float(so_diem)

    # Tính số lượng đạt
    soluongdat = 0
    for ma_hs, diem in diem_theo_hoc_sinh.items():
        diem_15_phut = diem["15 phút"]
        diem_1_tiet = diem["1 tiết"]
        diem_cuoi_ki = diem["cuối kì"]
        diem_trung_binh = tinh_diem_trung_binh(diem_15_phut, diem_1_tiet, diem_cuoi_ki)
        if diem_trung_binh >= 5.0:
            soluongdat += 1

    return soluongdat


def UpdateSiSo(MaLop, SiSo):
    lop = db.session.query(Lop).filter(Lop.MaLop == MaLop).first()

    if lop:
        si_so = db.session.query(func.count(LopHocSinh.MaHocSinh)).filter(
            LopHocSinh.MaLop == MaLop).scalar()

        lop.SiSo = SiSo

        db.session.commit()


#
#
# def Insert_HS_Remain(sohocsinhconlai, solopcanchia, tb, remaining):
#     if sohocsinhconlai <= 0 or not remaining:
#         return 0
#
#     siso = app.config["MAX_SS_LOP"]
#     condition = int(siso - tb)
#     remaining.reverse()
#
#     if len(remaining) >= condition:
#         for i in range(1, condition + 1):
#             lophocsinh = LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
#                                            NamTaoLop="2024")
#             UpdateSiSo(MaLop="L10A" + str(solopcanchia), SiSo=siso)
#             db.session.add(lophocsinh)
#     else:
#         for i in range(1, len(remaining) + 1):
#             lophocsinh = LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
#                                            NamTaoLop="2024")
#             UpdateSiSo(MaLop="L10A" + str(solopcanchia), SiSo=int(tb + len(remaining)))
#             db.session.add(lophocsinh)
#
#     db.session.commit()
#     sohocsinhconlai = sohocsinhconlai - int(min(condition, len(remaining)))
#
#     remaining = HocSinhNotLop(sohocsinhconlai) if sohocsinhconlai > 0 else []
#
#     return Insert_HS_Remain(sohocsinhconlai, solopcanchia - 1, tb, remaining)dd


# def CreateLop(solopcanchia):
#     namht = CurrentYear()
#
#     for i in range(1, solopcanchia + 1):
#         lop = Lop(MaLop="L10A" + str(i) + "_" + namht, TenLop="10A" + str(i), SiSo=int(tb), MaKhoi="1")
#         db.session.add(lop)
#         db.session.commit()


def CreateLop(tenlop, listhocsinh):
    currentyear = CurrentYear()

    malop = 'L' + tenlop + '_' + currentyear
    lop = Lop(MaLop=malop, TenLop=tenlop, SiSo=len(listhocsinh), MaKhoi=1)
    db.session.add(lop)
    for hocsinhid in listhocsinh:
        lophocsinh = LopHocSinh(MaLop=malop, MaHocSinh=hocsinhid, NamTaoLop=currentyear)
        db.session.add(lophocsinh)

    db.session.commit()


def Division_Class(solopcanchia, solopthem=None):
    bd = Cnt_Sum_HocSinh_Not_Lop()

    tb = ceil(bd / solopcanchia)

    lopbd = int(bd / tb)

    namht = CurrentYear()

    if tb > app.config["MAX_SS_LOP"]:
        return 0

    for i in range(1, lopbd + 1):
        lop = Lop(MaLop="L10A" + str(i) + "_" + namht, TenLop="10A" + str(i), SiSo=int(tb), MaKhoi="1")
        db.session.add(lop)
        db.session.commit()

        HocSinh = HocSinhNotLop(int(tb))
        for j in HocSinh:
            lophocsinh = LopHocSinh(MaLop="L10A" + str(i) + "_" + namht, MaHocSinh=j.MaHocSinh, NamTaoLop=namht)
            db.session.add(lophocsinh)

        db.session.commit()

    remaining = bd - tb * lopbd

    if remaining > 0:

        lop = Lop(MaLop="L10A" + str(solopcanchia) + "_" + namht, TenLop="10A" + str(solopcanchia),
                         SiSo=int(remaining), MaKhoi="1")
        db.session.add(lop)
        db.session.commit()

        HocSinh = HocSinhNotLop(int(remaining))
        for j in HocSinh:
            lophocsinh = LopHocSinh(MaLop="L10A" + str(solopcanchia) + "_" + namht, MaHocSinh=j.MaHocSinh,
                                           NamTaoLop=namht)
            db.session.add(lophocsinh)

        db.session.commit()


def GetPerMissionByValue(value):
    return Permission.query.filter(Permission.Value.__eq__(value)).first().PermissionID


def GetPerMission(id=None, value=None):
    if id:
        return Permission.query.filter(Permission.PermissionID.__eq__(id)).first()
    if value:
        return Permission.query.filter(Permission.Value.__eq__(value)).first()


def GetUserNameByID(username):
    return Account.query.filter(Account.TenDangNhap.__eq__(username)).first().id


def GetLopByMa(malop=None, mahocsinh=None, namtaolop=None):
    if mahocsinh:
        return db.session.query(LopHocSinh.MaLop).filter(LopHocSinh.MaHocSinh == mahocsinh,
                                                                LopHocSinh.NamTaoLop == namtaolop).first()
    if malop:
        return db.session.query(Lop.TenLop, Lop.SiSo, Lop.MaLop).filter(
            Lop.MaLop == malop).first()

    return None


def GetMonHoc(mamonhoc=None, tenmonhoc=None):
    return (
        db.session.query(MonHoc.TenMonHoc, MonHoc.MaMonHoc)
        .filter(
            or_(
                MonHoc.MaMonHoc == mamonhoc,
                MonHoc.TenMonHoc == tenmonhoc
            )
        )
        .first()
    )


def GetIDByPhone(number):
    return (db.session.query(Phone.UserID)
            .filter(Phone.Number == number).first())


def GetIDByHoTenEmail(inputsearch, malop):
    return (db.session.query(
        UserInfor.UserID,
        UserInfor.Ho,
        UserInfor.Ten
    ).join(LopHocSinh, LopHocSinh.MaHocSinh == UserInfor.UserID)
            .filter(
        LopHocSinh.MaLop == malop,
        or_(
            func.concat(UserInfor.Ho, UserInfor.Ten).ilike(f"%{inputsearch}%"),
            UserInfor.Email == inputsearch
        )
    ).all())


def GetHocSinhByTenHoTenEmailPhone(inputsearch, malop=None, namtaolop=None):
    res = []

    inputsearch = inputsearch.replace(" ", "")

    phone = GetIDByPhone(inputsearch)
    if phone:
        res.append({"MaHocSinh": phone.UserID,
                    "HoTen": GetUserInforByUserID(phone.UserID)})

        return res

    if malop:

        for user in GetIDByHoTenEmail(inputsearch, malop):
            res.append({"MaHocSinh": user.UserID,
                        "HoTen": user.Ho + ' ' + user.Ten})

    else:
        dsmalop = GetMaLop(namtaolop)

        print(dsmalop)

        # ds = GetIDByHoTenEmail("test103@gmail.com", "L10A1_2024")
        for i in dsmalop:
            for user in GetIDByHoTenEmail(inputsearch=inputsearch, malop=i[0]):
                res.append({"MaHocSinh": user.UserID,
                            "HoTen": user.Ho + ' ' + user.Ten,
                            "MaLop": GetLopByMa(mahocsinh=user.UserID, namtaolop=namtaolop)
                            })

    return res


# def GetHocSinhByTenEmailPhone(inputsearch):
#     result = db.session.query(UserInfor.UserID, UserInfor.Ho , UserInfor.Ten).filter(
#         or_(
#             func.concat(UserInfor.Ho,UserInfor.Ten) == inputsearch,
#             UserInfor.Email == inputsearch
#         )
#     ).join(
#         Phone, UserInfor.UserID == Phone.UserID, isouter=True
#     ).filter(
#         or_(
#             Phone.Number == inputsearch
#             # Phone.Number == None  # Nếu không có số điện thoại
#         )
#     ).first()
#
#     if result:
#         return { "MaHocSinh" : result.UserID,
#                 "HoTen":result.Ho + " "  + result.Ten
#                  }
#
#     return None


def GetHocKi(tenhocki, namhoc):
    return db.session.query(HocKi.MaHocKi).filter(HocKi.TenHocKi == tenhocki,
                                                         HocKi.NamHoc == namhoc).first()


def CheckPermissionUserExit(permissionid, userid):
    return PermissionUser.query.filter(PermissionUser.PermissionID == permissionid,
                                              PermissionUser.UserID == userid).first()


def AddPermissionUser(permissionid, userid):
    if not CheckPermissionUserExit(permissionid, userid):
        perrmissionuser = PermissionUser(PermissionID=permissionid, UserID=userid)
        db.session.add(perrmissionuser)
        db.session.commit()
        return True

    return False


def GetUserInforByUserID(userid):
    user = db.session.query(UserInfor.Ho, UserInfor.Ten).filter(UserInfor.UserID == userid).first()
    return user.Ho + " " + user.Ten


class TypeDiem(Enum):
    PHUT15 = "15 phút"
    TIET1 = "1 tiết"
    CUOIKI = "cuối kì"


def LoadLopHoc(MaMonHoc, MaHocKi):
    return (db.session.query(Lop)
            .join(Hoc, Lop.MaLop == Hoc.MaLop)
            .join(HocKi, Hoc.MaHocKi == HocKi.MaHocKi)
            .join(MonHoc, Hoc.MaMonHoc == MonHoc.MaMonHoc)
            .filter(
        and_(
            HocKi.MaHocKi == MaHocKi,
            MonHoc.MaMonHoc == MaMonHoc
        )).all()
            )


def GetMaHocSinhOfLop(malop):
    hocscsinhs = (db.session.query(LopHocSinh.MaHocSinh)
                  .filter(LopHocSinh.MaLop == malop).all())

    return [mahocsinh[0] for mahocsinh in hocscsinhs]


def LoadLop(key, malop=None, mamonhoc=None, mahocki=None, listmahocsinh=None):
    dshocsinh = []
    if listmahocsinh:
        hocsinh = listmahocsinh
    else:
        hocsinh = GetMaHocSinhOfLop(malop)

    if key == "info":
        dshocsinh = [LoadHSinfo(mahocsinh=mahocsinh, key="info") for mahocsinh in hocsinh]

        return dshocsinh

    if key == "diem":

        max15phut = 0
        max1tiet = 0

        for mahocsinh in hocsinh:
            diem = LoadDiem1HocSinh(mahocsinh=mahocsinh, mamonhoc=mamonhoc, mahocki=mahocki)

            dshocsinh.append(diem)

            max15phut = max(max15phut, len(diem['15phut']))
            max1tiet = max(max1tiet, len(diem['1tiet']))

        return {
            "diemdshocsinh": dshocsinh,
            "max15phut": max15phut,
            "max1tiet": max1tiet
        }


def LoadDiem1HocSinh(mahocsinh, mamonhoc, mahocki):
    return {
        "MaHocSinh": mahocsinh,
        "HoTen": GetUserInforByUserID(mahocsinh),
        **LoadHSinfo(mahocsinh, key="diem", mamonhoc=mamonhoc, mahocki=mahocki)
    }


def TimKiemHocSinh(mahocsinh, namtaolop, key=None):
    if key == "info":
        return (db.session.query(LopHocSinh.MaLop, UserInfor.UserID, UserInfor.Ho,
                                 UserInfor.Ten,
                                 HocSinh.DiemTbDauVao, UserInfor.GioiTinh,
                                 UserInfor.NgaySinh, UserInfor.DiaChi)
                .join(Account, Account.id == UserInfor.UserID)
                .join(HocSinh, HocSinh.MaHocSinh == Account.id)
                .join(LopHocSinh, LopHocSinh.MaHocSinh == HocSinh.MaHocSinh)
                .filter(UserInfor.UserID == mahocsinh, LopHocSinh.MaHocSinh == mahocsinh,
                        LopHocSinh.NamTaoLop == namtaolop)
                .all())


def LoadHSinfo(mahocsinh, key, mamonhoc=None, mahocki=None):
    if key == "info":
        return (db.session.query(UserInfor.UserID, UserInfor.Ho, UserInfor.Ten,
                                 HocSinh.DiemTbDauVao, UserInfor.GioiTinh,
                                 UserInfor.NgaySinh, UserInfor.DiaChi)
                .join(Account, Account.id == UserInfor.UserID)
                .join(HocSinh, HocSinh.MaHocSinh == Account.id)
                .filter(UserInfor.UserID == mahocsinh)
                .all())

    if key == "diem":

        diem15phut = []
        diem1tiet = []
        cuoiki = []

        inforhocsinh = (db.session.query(HocSinh.MaHocSinh, Diem.TypeDiem, Diem.SoDiem,
                                         Diem.MaMonHoc, Diem.MaHocKi)
                        .join(Diem, HocSinh.MaHocSinh == Diem.MaHocSinh)
                        .filter(HocSinh.MaHocSinh == mahocsinh, Diem.TypeDiem.in_([TypeDiem.PHUT15.value,
                                                                                                 TypeDiem.TIET1.value,
                                                                                                 TypeDiem.CUOIKI.value]),
                                Diem.MaMonHoc == mamonhoc,
                                Diem.MaHocKi == mahocki)
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
#     inforhocsinh = (db.session.query(HocSinh.MaHocSinh, Diem.TypeDiem, Diem.SoDiem,
#                                      Diem.MaMonHoc, Diem.MaHocKi)
#                     .join(Diem, HocSinh.MaHocSinh == Diem.MaHocSinh)
#                     .filter(HocSinh.MaHocSinh == mahocsinh)
#                     .all())
#
#     return inforhocsinh


def removeHocSinh(malop, mahocsinh):
    hocsinh = LopHocSinh.query.filter(
        LopHocSinh.MaLop == malop,
        LopHocSinh.MaHocSinh == mahocsinh
    ).first()

    if hocsinh:
        lop = Lop.query.filter(Lop.MaLop == malop).first()
        lop.SiSo = lop.SiSo - 1
        db.session.delete(hocsinh)

        db.session.commit()
        return True
    return False


def CheckHocSinhExitsLop(mahocsinh, malop):
    return LopHocSinh.query.filter(LopHocSinh.MaHocSinh == mahocsinh,
                                          LopHocSinh.MaLop == malop).first()


def addHocSinhToLop(listmahocsinh, malop, namtaolop):
    lop = Lop.query.filter(Lop.MaLop == malop).first()

    print(lop)
    print(lop.SiSo)

    if (40 - lop.SiSo) < len(listmahocsinh):
        return False

    for mahocsinh in listmahocsinh:
        lop.SiSo = lop.SiSo + 1
        lophocsinh = LopHocSinh(MaHocSinh=mahocsinh, MaLop=malop, NamTaoLop=namtaolop)
        db.session.add(lophocsinh)

        db.session.commit()
    return True


def AddDiemHocSinhList(maHocSinh, mamonhoc, mahocki, typeDiem, diemListNew):
    diemListOLd = GetDiemExit(mahocsinh=maHocSinh, mamonhoc=mamonhoc, mahocki=mahocki, typeDiem=typeDiem)

    cntdiemnew = len(diemListNew)

    cntdiemold = len(diemListOLd)

    for i in range(1, cntdiemnew + 1):

        if diemListNew[i - 1] and i <= cntdiemold and diemListOLd[i - 1].SoDiem != diemListNew[i - 1]:
            diemListOLd[i - 1].SoDiem = diemListNew[i - 1]
            db.session.commit()

        else:
            if diemListNew[i - 1]:
                AddDiemHocSinh(
                    mahocsinh=maHocSinh,
                    mamonhoc=mamonhoc,
                    mahocki=mahocki,
                    typediem=typeDiem,
                    sodiem=diemListNew[i - 1]
                )


def GetDiemExit(mahocsinh, mamonhoc, mahocki, typeDiem):
    return Diem.query.filter(Diem.MaHocSinh == mahocsinh,
                                    Diem.MaMonHoc == mamonhoc,
                                    Diem.MaHocKi == mahocki,
                                    Diem.TypeDiem == typeDiem).all()


def AddDiemHocSinh(mahocsinh, mamonhoc, mahocki, typediem, sodiem):
    diem = Diem(SoDiem=sodiem,
                       TypeDiem=typediem,
                       MaHocSinh=mahocsinh,
                       MaMonHoc=mamonhoc,
                       MaHocKi=mahocki)

    db.session.add(diem)
    db.session.commit()

    return True


def RemoveDshocsinhAllOfCurrentyear():
    currentyear = CurrentYear()

    lophocsinhcurrent = db.session.query(LopHocSinh).filter(LopHocSinh.NamTaoLop == currentyear).delete()

    lopcurrent = db.session.query(Lop).filter(Lop.MaLop.ilike(f"%{currentyear}%")).delete()

    db.session.commit()
    return True


# def SoLop(maxsslop):
#     return ceil(
#         db.session.query(LopHocSinh).filter(LopHocSinh.NamTaoLop == CurrentYear()).count() / maxsslop)


def GetMaLop(namtaolop):
    dslop = db.session.query(
        LopHocSinh.MaLop
    ).filter(
        LopHocSinh.NamTaoLop == namtaolop
    ).distinct().all()

    return dslop


def CntSiSoLopCurrent(solop, key):
    cntalllopcurrentyear = sum(GetLopByMa(malop=key + str(i) + '_' + CurrentYear()).SiSo for i in range(1, solop + 1))
    return cntalllopcurrentyear


def Solop1(maxsslop):
    return db.session.query(LopHocSinh).filter(LopHocSinh.NamTaoLop == CurrentYear()).count()


def LoadMonHocOfLop(malop):
    monhocs = (db.session.query(MonHoc.TenMonHoc).
               join(Hoc, Hoc.MaMonHoc == MonHoc.MaMonHoc).
               join(Lop, Lop.MaLop == Hoc.MaLop).
               filter(Lop.MaLop == malop)).all()

    return monhocs


def LoadAllMon():
    return (db.session.query(MonHoc.TenMonHoc)).all()


Ho = ["Phan", "Ly", "Thanh", "La", "Hoang"]
Ten = ["Trung", "Trinh", "A", "D", "E", "G", "B"]


# def them():
#     for i in range(3000, 3031):
#         idac = "HS" + str(Get_Cnt_Accout_Current()) + "_" + str(random.randint(10, 99))
#         hocsinh = HocSinh(MaHocSinh=idac, DiemTbDauVao=float(random.randint(1, 10)))
#         db.session.add(hocsinh)
#
#         password_hash = hashlib.md5(str(i).encode('utf-8')).hexdigest()
#
#         accoutHocSinh = Account(id=idac, TenDangNhap="HocSinhmoi" + str(i), MatKhau=password_hash,
#                                        role=Role.HocSinh)
#         db.session.add(accoutHocSinh)
#
#         inforHocSinh = UserInfor(UserID=idac, Ho=Ho[(i % 5)], Ten=Ten[(i % 7)], NgaySinh="2008-11-12",
#                                         GioiTinh="Nam", DiaChi="Bình định", Email="test" + str(i) + "@gmail.com",
#                                         Image=None)
#         db.session.add(inforHocSinh)
#
#         db.session.commit()


# c
#     for i in range(1, 11):
#         lop = Lop( MaLop = "L10A" + str(i) , TenLop = "10A" + str(i) , SiSo = 40 , MaKhoi =1 )
#         db.session.add(lop)
#
#     db.session.commit()


def them():
    idac = "Admin123"
    password_hash = str(hashlib.md5("123".encode('utf-8')).hexdigest())

    user = Account(id=idac,
                          TenDangNhap="Admin",
                          MatKhau=password_hash,
                          Active=True,
                          role=Role.Admin)

    db.session.add(user)

    inforHocSinh = UserInfor(UserID=idac, Ho="Phan", Ten="Thanh Trinh", NgaySinh="2004-12-11",
                                    GioiTinh="Nam", DiaChi="Bình định", Email="2251052129trinh@ou.edu.vn",
                                    Image=None)
    db.session.add(inforHocSinh)

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        them()
        # lop_hocsinh = LoadLop(malop = 'L10A1_2023',key = "diem",  mamonhoc='MH1', mahocki=1)
        #
        #
        # print(lop_hocsinh)
        #
        # for i in lop_hocsinh['diemdshocsinh']:
        #     if sum(i['15phut']) != 0:
        #         print(f"trung binh: { sum(i['15phut']) / len(i['15phut']) }")
        # print(GetLopByMa(mahocsinh="HS587_52", namtaolop="2023"))
        # print(GetHocSinhByTenHoTenEmailPhone(inputsearch= "Trinh", namtaolop="2023") )

        print(GetHocSinhByTenHoTenEmailPhone(inputsearch="La", namtaolop="2023"))
