



from QUANLIHOCSINH import app, db
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pandas as pd

dataframe1 = pd.read_excel(os.getcwd() + '\\templates\\layout\\infor.xlsx', dtype={"Số điện thoại": str})


def rand_Pass_Confirm_Email():
    return str(random.randint(10000, 99999))


def Send_Email(subject,content, email_rec):
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
    # Chuyển dữ liệu thành danh sách dictionary
    for i, row in df.iterrows():
        dic.append({
            "Họ": row["Họ"],
            "Tên": row["Tên"],
            "Điểm": row["Điểm"],
            "Ngày sinh": row["Ngày sinh"],
            "Giới tính": row["Giới tính"],
            "Địa chỉ": row["Địa chỉ"],
            "Email": row["Email"],
            "Số điện thoại": row["Số điện thoại"]
        })

    # page_size = 40
    # start = (page - 1) * page_size
    # end = start + page_size
    #
    # df_page = df.iloc[start:end]
    #
    # dic_page = df_page.to_dict(orient="records")

    return dic

def Remove_Permission_User_Exits(permissionvalue, username):


    return True


if __name__ == '__main__':
    with app.app_context():
        print(dataframe1)
