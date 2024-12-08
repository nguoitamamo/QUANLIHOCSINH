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


def CurrentYear():
    return str(datetime.now().year)


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


def LoadLopEdHoc():
    return (
        db.session.query(models.Lop.MaLop, models.Lop.TenLop)
        .join(models.Hoc, models.Hoc.MaLop == models.Lop.MaLop)
        .distinct()
        .all()
    )


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


def LoadKhoiAll():
    return db.session.query(models.Khoi.TenKhoi, models.Khoi.MaKhoi).all()


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
#             lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
#                                            NamTaoLop="2024")
#             UpdateSiSo(MaLop="L10A" + str(solopcanchia), SiSo=siso)
#             db.session.add(lophocsinh)
#     else:
#         for i in range(1, len(remaining) + 1):
#             lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia), MaHocSinh=remaining[i - 1].MaHocSinh,
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
#         lop = models.Lop(MaLop="L10A" + str(i) + "_" + namht, TenLop="10A" + str(i), SiSo=int(tb), MaKhoi="1")
#         db.session.add(lop)
#         db.session.commit()


def CreateLop(tenlop, listhocsinh):
    currentyear = CurrentYear()

    malop = 'L' + tenlop + '_' + currentyear
    lop = models.Lop(MaLop=malop, TenLop=tenlop, SiSo=len(listhocsinh), MaKhoi=1)
    db.session.add(lop)
    for hocsinhid in listhocsinh:
        lophocsinh = models.LopHocSinh(MaLop=malop, MaHocSinh=hocsinhid, NamTaoLop=currentyear)
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
        lop = models.Lop(MaLop="L10A" + str(i) + "_" + namht, TenLop="10A" + str(i), SiSo=int(tb), MaKhoi="1")
        db.session.add(lop)
        db.session.commit()

        HocSinh = HocSinhNotLop(int(tb))
        for j in HocSinh:
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(i) + "_" + namht, MaHocSinh=j.MaHocSinh, NamTaoLop=namht)
            db.session.add(lophocsinh)

        db.session.commit()

    remaining = bd - tb * lopbd

    if remaining > 0:

        lop = models.Lop(MaLop="L10A" + str(solopcanchia) + "_" + namht, TenLop="10A" + str(solopcanchia),
                         SiSo=int(remaining), MaKhoi="1")
        db.session.add(lop)
        db.session.commit()

        HocSinh = HocSinhNotLop(int(remaining))
        for j in HocSinh:
            lophocsinh = models.LopHocSinh(MaLop="L10A" + str(solopcanchia) + "_" + namht, MaHocSinh=j.MaHocSinh,
                                           NamTaoLop=namht)
            db.session.add(lophocsinh)

        db.session.commit()


def GetPerMissionByValue(value):
    return models.Permission.query.filter(models.Permission.Value.__eq__(value)).first().PermissionID


def GetPerMission(id=None, value=None):
    if id:
        return models.Permission.query.filter(models.Permission.PermissionID.__eq__(id)).first()
    if value:
        return models.Permission.query.filter(models.Permission.Value.__eq__(value)).first()


def GetUserNameByID(username):
    return models.Account.query.filter(models.Account.TenDangNhap.__eq__(username)).first().id


def GetLopByMa(malop=None, mahocsinh=None, namtaolop=None):
    if mahocsinh:
        return db.session.query(models.LopHocSinh.MaLop).filter(models.LopHocSinh.MaHocSinh == mahocsinh,
                                                                models.LopHocSinh.NamTaoLop == namtaolop).first()
    if malop:
        return db.session.query(models.Lop.TenLop, models.Lop.SiSo, models.Lop.MaLop).filter(
            models.Lop.MaLop == malop).first()

    return None


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


def GetIDByPhone(number, malop):
    return (db.session.query(models.Phone.UserID).join(models.LopHocSinh, models.LopHocSinh.MaLop == malop)
            .filter(models.Phone.Number == number).first())


def GetIDByHoTenEmail(inputsearch, malop):
    return (db.session.query(
        models.UserInfor.UserID,
        models.UserInfor.Ho,
        models.UserInfor.Ten
    ).join(models.LopHocSinh, models.LopHocSinh.MaHocSinh == models.UserInfor.UserID)
            .filter(
        models.LopHocSinh.MaLop == malop,
        or_(
            func.concat(models.UserInfor.Ho, models.UserInfor.Ten).ilike(f"%{inputsearch}%"),
            models.UserInfor.Email == inputsearch
        )
    ).all())


def GetHocSinhByTenHoTenEmailPhone(inputsearch, malop=None, namtaolop=None):
    res = []

    inputsearch = inputsearch.replace(" ", "")

    phone = GetIDByPhone(inputsearch, malop)
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

        # ds = GetIDByHoTenEmail("test103@gmail.com", "L10A1_2024")
        for i in dsmalop:
            for user in GetIDByHoTenEmail(inputsearch=inputsearch, malop=i[0]):
                res.append({"MaHocSinh": user.UserID,
                            "MaLop": GetLopByMa(mahocsinh=user.UserID, namtaolop=CurrentYear())})

    return res


# def GetHocSinhByTenEmailPhone(inputsearch):
#     result = db.session.query(models.UserInfor.UserID, models.UserInfor.Ho , models.UserInfor.Ten).filter(
#         or_(
#             func.concat(models.UserInfor.Ho, models.UserInfor.Ten) == inputsearch,
#             models.UserInfor.Email == inputsearch
#         )
#     ).join(
#         models.Phone, models.UserInfor.UserID == models.Phone.UserID, isouter=True
#     ).filter(
#         or_(
#             models.Phone.Number == inputsearch
#             # models.Phone.Number == None  # Nếu không có số điện thoại
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
    user = db.session.query(models.UserInfor.Ho, models.UserInfor.Ten).filter(models.UserInfor.UserID == userid).first()
    return user.Ho + " " + user.Ten


class TypeDiem(Enum):
    PHUT15 = "15 phút"
    TIET1 = "1 tiết"
    CUOIKI = "cuối kì"


def LoadLop(malop, key, mamonhoc=None, mahocki=None):
    dshocsinh = []

    hocsinh = (db.session.query(models.LopHocSinh.MaLop, models.LopHocSinh.MaHocSinh)
               .filter(models.LopHocSinh.MaLop == malop).all())

    if key == "info":
        dshocsinh = [LoadHSinfo(mahocsinh=hs.MaHocSinh, key="info") for hs in hocsinh]

        return dshocsinh

    if key == "diem":

        max15phut = 0
        max1tiet = 0

        for hs in hocsinh:
            hs_diem = {
                "MaHocSinh": hs.MaHocSinh,
                "HoTen": GetUserInforByUserID(hs.MaHocSinh),
                **LoadHSinfo(hs.MaHocSinh, key="diem", mamonhoc=mamonhoc, mahocki=mahocki)
            }
            dshocsinh.append(hs_diem)

            max15phut = max(max15phut, len(hs_diem['15phut']))
            max1tiet = max(max1tiet, len(hs_diem['1tiet']))

        return {
            "diemdshocsinh": dshocsinh,
            "max15phut": max15phut,
            "max1tiet": max1tiet
        }


def LoadHSinfo(mahocsinh, key, keytimkiem=None, mamonhoc=None, mahocki=None):
    if key == "info":
        if keytimkiem:
            inforhocsinh = (db.session.query(models.LopHocSinh.MaLop, models.UserInfor.UserID, models.UserInfor.Ho,
                                             models.UserInfor.Ten,
                                             models.HocSinh.DiemTbDauVao, models.UserInfor.GioiTinh,
                                             models.UserInfor.NgaySinh, models.UserInfor.DiaChi)
                            .join(models.Account, models.Account.id == models.UserInfor.UserID)
                            .join(models.HocSinh, models.HocSinh.MaHocSinh == models.Account.id)
                            .join(models.LopHocSinh, models.LopHocSinh.MaHocSinh == models.HocSinh.MaHocSinh)
                            .filter(models.UserInfor.UserID == mahocsinh, models.LopHocSinh.MaHocSinh == mahocsinh,
                                    models.LopHocSinh.NamTaoLop == CurrentYear())
                            .all())


        else:
            inforhocsinh = (db.session.query(models.UserInfor.UserID, models.UserInfor.Ho, models.UserInfor.Ten,
                                             models.HocSinh.DiemTbDauVao, models.UserInfor.GioiTinh,
                                             models.UserInfor.NgaySinh, models.UserInfor.DiaChi)
                            .join(models.Account, models.Account.id == models.UserInfor.UserID)
                            .join(models.HocSinh, models.HocSinh.MaHocSinh == models.Account.id)
                            .filter(models.UserInfor.UserID == mahocsinh)
                            .all())
        return inforhocsinh
    if key == "diem":

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
        lop = models.Lop.query.filter(models.Lop.MaLop == malop).first()
        lop.SiSo = lop.SiSo - 1
        db.session.delete(hocsinh)
        db.session.commit()
        return True
    return False


def CheckHocSinhExitsLop(mahocsinh, malop):
    return models.LopHocSinh.query.filter(models.LopHocSinh.MaHocSinh == mahocsinh,
                                          models.LopHocSinh.MaLop == malop).first()


def addHocSinhToLop(listmahocsinh, malop):
    lop = models.Lop.query.filter(models.Lop.MaLop == malop).first()

    print(lop)
    print(lop.SiSo)

    if (40 - lop.SiSo) < len(listmahocsinh):
        return False

    for mahocsinh in listmahocsinh:
        lop.SiSo = lop.SiSo + 1
        lophocsinh = models.LopHocSinh(MaHocSinh=mahocsinh, MaLop=malop, NamTaoLop=CurrentYear())
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
    return models.Diem.query.filter(models.Diem.MaHocSinh == mahocsinh,
                                    models.Diem.MaMonHoc == mamonhoc,
                                    models.Diem.MaHocKi == mahocki,
                                    models.Diem.TypeDiem == typeDiem).all()


def AddDiemHocSinh(mahocsinh, mamonhoc, mahocki, typediem, sodiem):
    diem = models.Diem(SoDiem=sodiem,
                       TypeDiem=typediem,
                       MaHocSinh=mahocsinh,
                       MaMonHoc=mamonhoc,
                       MaHocKi=mahocki)

    db.session.add(diem)
    db.session.commit()

    return True


def RemoveDshocsinhAllOfCurrentyear():
    currentyear = CurrentYear()

    lophocsinhcurrent = db.session.query(models.LopHocSinh).filter(models.LopHocSinh.NamTaoLop == currentyear).delete()

    lopcurrent = db.session.query(models.Lop).filter(models.Lop.MaLop.ilike(f"%{currentyear}%")).delete()

    db.session.commit()
    return True


# def SoLop(maxsslop):
#     return ceil(
#         db.session.query(models.LopHocSinh).filter(models.LopHocSinh.NamTaoLop == CurrentYear()).count() / maxsslop)


def GetMaLop(namtaolop):
    dslop = db.session.query(
        models.LopHocSinh.MaLop
    ).filter(
        models.LopHocSinh.NamTaoLop == namtaolop
    ).distinct().all()

    return dslop


def CntSiSoLopCurrent(solop, key):
    cntalllopcurrentyear = sum(GetLopByMa(malop=key + str(i) + '_' + CurrentYear()).SiSo for i in range(1, solop + 1))
    return cntalllopcurrentyear


def Solop1(maxsslop):
    return db.session.query(models.LopHocSinh).filter(models.LopHocSinh.NamTaoLop == CurrentYear()).count()


def LoadMonHocOfLop(malop):
    monhocs = (db.session.query(models.MonHoc.TenMonHoc).
               join(models.Hoc, models.Hoc.MaMonHoc == models.MonHoc.MaMonHoc).
               join(models.Lop, models.Lop.MaLop == models.Hoc.MaLop).
               filter(models.Lop.MaLop == malop)).all()

    return monhocs


Ho = ["Phan", "Ly", "Thanh", "La", "Hoang"]
Ten = ["Trung", "Trinh", "A", "D", "E", "G", "B"]


def them():
    for i in range(3000, 3031):
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
        # lop_hocsinh = LoadLop(malop = 'L10A1_2023',key = "diem",  mamonhoc='MH1', mahocki=1)
        #
        # # for i in lophocsinh:
        # #     print(i)
        # #
        # for i in lop_hocsinh['diemdshocsinh']:
        #     print(f"mahocsinh: {i['MaHocSinh']} , hoten : {i['HoTen']} , 15phut : {i['15phut']} , 1tiet : {i['1tiet']} , cuoiki : {i['diemthi']}")
        #
        # # #
        # # for i in lophocsinh:
        # #     print(i)
        #
        # # diem = GetDiemExit(mahocsinh='HS437_59', mamonhoc='MH1', mahocki=1, typeDiem='cuối kì')
        # #
        # # print(type(diem))
        # #
        # # for i in diem:
        #     print(i)
        #
        # if lop_hocsinh and 'diemdshocsinh' in lop_hocsinh:
        #     for hs in lop_hocsinh['diemdshocsinh']:
        #         print(f"Họ tên: {hs['HoTen']}")
        #
        #         for i in hs.get('15phut', []):
        #             print(f"Điểm 15 phút: {i}")
        #
        #         for i in hs.get('1tiet', []):
        #             print(f"Điểm 1 tiết: {i}")
        #
        #         for i in hs.get('diemthi', []):
        #             print(f"Điểm cuối kỳ: {i}")
        #
        #     print(f"Max 15 phút: {lop_hocsinh['max15phut']}")
        #     print(f"Max 1 tiết: {lop_hocsinh['max1tiet']}")
        # else:
        #     print("Không có dữ liệu học sinh.")

        # In ra thông tin
        # print(f"Họ tên: {ho_ten['Ho']} {ho_ten['Ten']}")
        # print("Điểm 15 phút:", diem_15phut)
        # print("Điểm 1 tiết:", diem_1tiet)
        # print("Điểm cuối kỳ:", diem_cuoiki)
        # print("-" * 20)

        # for hs in danh_sach_hoc_sinh:
        #     for info in hs:
        #         print(
        #             f" Mã học sinh: {info.UserID} ,Họ: {info.Ho}, Tên: {info.Ten}, Giới tính: {info.GioiTinh}, Ngày sinh: {info.NgaySinh}, Địa chỉ: {info.DiaChi}")

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
        # tb = ceil(427 / 11)
        # print(f"kq: {int(tb)} , type : {type(tb)}")
        # solop = ceil((Cnt_Sum_HocSinh_Not_Lop() / app.config["MAX_SS_LOP"]))
        # print(solop)
        # print(CurrentYear())
        # malop = GetLopByMa(mahocsinh = 'HS102_75', namtaolop = CurrentYear())
        # print(malop[0][1:].split('_')[0])
        # print(GetHocSinhByTenHoTenEmailPhone(inputsearch="test103@gmail.com",namtaolop="2024"))
        # print(GetIDByHoTenEmail(inputsearch="test103@gmail.com", malop = "L10A1_2024"))

        # res = []
        # dsmalop = GetMaLop("2024")
        # print(dsmalop)
        # print()
        #
        # ds = GetIDByHoTenEmail("test103@gmail.com", "L10A1_2024")
        #
        # for malop in dsmalop:
        #     for user in ds:
        #         res.append({"MaHocSinh": user.UserID,
        #                     "HoTen": user.Ho + ' ' + user.Ten})
        #         print(len(res))
        #
        # print(res)
        print(LoadHSinfo(mahocsinh='HS377_98', key="info"))
