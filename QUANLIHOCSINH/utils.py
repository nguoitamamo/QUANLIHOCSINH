from itertools import islice

from QUANLIHOCSINH import app, db
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pandas as pd
from math import ceil
from dao import GetLopByMa, GetHocSinhByTenHoTenEmailPhone, LoadLop

dataframe1 = pd.read_excel(os.getcwd() + '\\templates\\layout\\infor.xlsx', dtype={"Số điện thoại": str})


def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))


def Send_Email(subject, content, email_rec):
    email = "2251052130truong@ou.edu.vn"
    passw = "18072004@Hnt"
    email_send = email_rec
    mail_content = content

    smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_session.starttls()
    smtp_session.login(email, passw)  #

    message = MIMEMultipart()
    message['From'] = email
    message['To'] = email_send
    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))

    smtp_session.sendmail(email, email_send, message.as_string())

    smtp_session.quit()
    print("Email đã được gửi thành công!")


def LoadFile(file):
    df = pd.read_excel(file, dtype={"Số điện thoại": str})

    dic = []

    for i, row in df.iterrows():
        dic.append({
            "STT": row["STT"],
            "Họ": row["Họ"],
            "Tên": row["Tên"],
            "Điểm": row["Điểm"],
            "Ngày sinh": row["Ngày sinh"],
            "Giới tính": row["Giới tính"],
            "Địa chỉ": row["Địa chỉ"],
            "Email": row["Email"],
            "Số điện thoại": row["Số điện thoại"]
        })

    return dic


def Pagination_Data(data, page, total_record=10):
    total_page = ceil(len(data) / total_record)

    start = (page - 1) * total_record
    end = start + total_record

    df_page = list(islice(data, start, end))

    return {
        "dic_page": df_page,
        "total_page": total_page
    }


def SaveIntoSession(dshocsinh):
    dic = []

    for hs in dshocsinh:
        for info in hs:
            dic.append({
                "UserID": info.UserID,
                "Họ": info.Ho,
                "Tên": info.Ten,
                "Điểm": info.DiemTbDauVao,
                "Ngày sinh": info.NgaySinh,
                "Giới tính": info.GioiTinh,
                "Địa chỉ": info.DiaChi
            })

    return dic


# class UserInfor():
#     def __init__(self):


def SuggestedLop(ds, keyword):
    res = []

    l, r = 0, len(ds) - 1

    for i in range(len(keyword)):
        c = keyword[i]

        while l <= r and (len(ds[l]) <= i or ds[l][i] != c):
            l += 1

        while l <= r and (len(ds[r]) <= i or ds[r][i] != c):
            r -= 1

    res.append([])
    remain = r - l + 1
    for j in range(min(5, remain)):
        res[-1].append(ds[l + j])

    return res


def CalDiemTbHocSinh(diemhk1, diemhk2, max_15phut_hocki1,max_1tiet_hocki1,
                     max_15phut_hocki2,max_1tiet_hocki2, namtaolop= None):

    dshocsinh= []
    for i in range(len(diemhk1['diemdshocsinh'])):
        dshocsinh.append(DiemHocSinh(mahocsinh=diemhk1['diemdshocsinh'][i]['MaHocSinh'],
                                           hoten=diemhk1['diemdshocsinh'][i]['HoTen'],
                                           listdiem15phuthk1=diemhk1['diemdshocsinh'][i]['15phut'],
                                           listdiem1tiethk1=diemhk1['diemdshocsinh'][i]['1tiet'],
                                           listdiem15phuthk2=diemhk2['diemdshocsinh'][i]['15phut'],
                                           listdiem1tiethk2=diemhk2['diemdshocsinh'][i]['1tiet'],
                                           listdiemcuoikihk1=diemhk1['diemdshocsinh'][i]['diemthi'],
                                           listdiemcuoikihk2=diemhk2['diemdshocsinh'][i]['diemthi'],
                                           max_15phut_hocki1=max_15phut_hocki1,
                                           max_1tiet_hocki1=max_1tiet_hocki1,
                                           max_15phut_hocki2=max_15phut_hocki2,
                                           max_1tiet_hocki2=max_1tiet_hocki2,
                                           namtaolop=namtaolop))
    return dshocsinh

def InfoDiemHocSinh(inputsearch, malop, mamonhoc, namhoc, namtaolop = None):
    if namtaolop:
        hocsinhs = GetHocSinhByTenHoTenEmailPhone(inputsearch=inputsearch, namtaolop=namtaolop)
    else:
        hocsinhs = GetHocSinhByTenHoTenEmailPhone(inputsearch=inputsearch, malop=malop)

    hocsinhs = [hs['MaHocSinh'] for hs in hocsinhs]

    diemhk1 = LoadLop(listmahocsinh=hocsinhs, key="diem", mamonhoc=mamonhoc, mahocki='1_' + namhoc)
    diemhk2 = LoadLop(listmahocsinh=hocsinhs, key="diem", mamonhoc=mamonhoc, mahocki='2_' + namhoc)

    max_15phut_hocki1 = diemhk1['max15phut']
    max_1tiet_hocki1 = diemhk1['max1tiet']
    max_15phut_hocki2 = diemhk2['max15phut']
    max_1tiet_hocki2 = diemhk2['max1tiet']

    return diemhk1, diemhk2, max_15phut_hocki1, max_1tiet_hocki1, max_15phut_hocki2, max_1tiet_hocki2



def DiemHocSinh(mahocsinh, hoten, listdiem15phuthk1, listdiem1tiethk1, listdiemcuoikihk1,
                listdiem15phuthk2, listdiem1tiethk2, listdiemcuoikihk2,
                max_15phut_hocki1, max_1tiet_hocki1,
                max_15phut_hocki2, max_1tiet_hocki2,  namtaolop=None ):
    return {
        "MaHocSinh": mahocsinh,
        "HoTen": hoten,
        "TBHK1": CalTinhDiemTb(listdiem15phuthk1,
                               listdiem1tiethk1,
                               listdiemcuoikihk1,
                               max15phut=max_15phut_hocki1,
                               max1tiet=max_1tiet_hocki1),

        "TBHK2": CalTinhDiemTb(listdiem15phuthk2,
                               listdiem1tiethk2,
                               listdiemcuoikihk2,
                               max15phut=max_15phut_hocki2,
                               max1tiet=max_1tiet_hocki2),

        "MaLop": GetLopByMa(mahocsinh=mahocsinh, namtaolop=namtaolop)[0] if namtaolop else None

    }


def CalTinhDiemTb(listdiem15phut, listdiem1tiet, listcuoiki, max15phut, max1tiet):
    tb15phut = 0
    tb1tiet = 0
    cuoiki = 0

    if len(listdiem15phut) > 0:
        tb15phut = sum(listdiem15phut) / max15phut
    if len(listdiem1tiet):
        tb1tiet = sum(listdiem1tiet) / max1tiet
    if len(listcuoiki) > 0:
        cuoiki = listcuoiki[0]

    return round(tb15phut * app.config["15PHUT"] + tb1tiet * app.config["1TIET"] + cuoiki * app.config["CUOIKY"], 1)
