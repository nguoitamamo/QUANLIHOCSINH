
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, DateTime, Boolean,Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from QUANLIHOCSINH import db, app
from enum import unique
from enum import Enum as Emun1



class Role(Emun1):
    Admin = 1
    GiangVien = 2
    NhanvienBoPhanKhac = 3
    HocSinh = 4



class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    id = Column(String(20), primary_key=True)
    TenDangNhap = Column(String(30), nullable=False, unique=True)
    MatKhau = Column(String(50), nullable=False)
    NgayTao = Column(DateTime, default=datetime.today())
    Active = Column(Boolean, default=False)
    UserInfor = relationship("UserInfor", backref='account', uselist= False, lazy=True)
    PermissionUsers = relationship("PermissionUser", backref='account', lazy=True)
    HocSinh = relationship("HocSinh", backref='account', uselist= False, lazy=True)
    role = Column(Enum(Role), default=Role.GiangVien)


class UserInfor(db.Model):
    __tablename__ = 'userinfor'
    UserID = Column(String(20),  ForeignKey('account.id'), primary_key=True)
    Ho = Column(String(20) , nullable=False)
    Ten = Column(String(50), nullable=False)
    Image = Column(String(100), default = 'https://res.cloudinary.com/ddkpaw2gy/image/upload/v1732349173/avatarhocsinh_udeelp.png')
    NgaySinh = Column(Date, nullable=False)
    GioiTinh = Column(String(20), nullable=False)
    DiaChi = Column(String(100), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    Phones = relationship('Phone', backref='userinfor', lazy=True)


class Token(db.Model):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Value = Column(String(5), nullable=False)
    Email = Column(String(50), nullable=False)


class Phone(db.Model):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Number = Column(String(11), nullable=False)
    UserID = Column(String(20), ForeignKey('userinfor.UserID')  , nullable=False)


class Permission(db.Model):
    __tablename__ = 'permission'
    PermissionID = Column(Integer, primary_key=True, autoincrement=True)
    Value = Column(String(50), nullable=False)
    PermissionUsers = relationship("PermissionUser", backref='permission', lazy=True)

    def __repr__(self):
        return f"<Role(Permission={self.PermissionID}, Value='{self.Value}')>"


class PermissionUser(db.Model):
    __tablename__ = 'permissionuser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    PermissionID = Column(Integer, ForeignKey('permission.PermissionID'), nullable=False)
    UserID = Column(String(20), ForeignKey('account.id'), nullable=False)

    def __repr__(self):
        return f"<Permission(Permission={self.PermissionID}, Value='{self.Value}')>"


# class Admin(db.Model):
#     __tablename__ = 'admin'
#     AdminID = Column(String(20),ForeignKey('account.id') , primary_key=True)
#
#
#
# class NhanVienBoPhanKhac(db.Model):
#     __tablename__ = 'nhanvienbophankhac'
#     MaNV = Column(String(20), ForeignKey('account.id'),primary_key=True)


class MonHoc(db.Model):
    __tablename__ = 'monhoc'
    MaMonHoc = Column(String(20), primary_key=True)
    TenMonHoc = Column(String(30), nullable=False)
    GiangViens = relationship('GiangVien', backref='monhoc', lazy=True)
    Diems = relationship('Diem', backref='monhoc', lazy=True)
    Hocs = relationship('Hoc', backref='monhoc', lazy=True)


class GiangVien(db.Model):
    __tablename__ = 'giangvien'
    MaGiangVien = Column(String(20), ForeignKey('account.id'), primary_key=True)
    MaMonHoc = Column(String(20), ForeignKey('monhoc.MaMonHoc'), nullable=False)
    Hocs = relationship('Hoc', backref='giangvien', lazy=True)





class Khoi(db.Model):
    __tablename__="khoi"
    MaKhoi = Column(Integer, primary_key=True, autoincrement=True)
    TenKhoi = Column(String(50), nullable=False)
    Lops = relationship('Lop', backref='khoi', lazy=True)


class Lop(db.Model):
    __tablename__="lop"
    MaLop = Column(String(20), primary_key=True)
    TenLop = Column(String(20), nullable=False)
    SiSo = Column(Integer, nullable=False)
    MaKhoi = Column(Integer, ForeignKey('khoi.MaKhoi'), nullable=False)
    LopHocSinhs = relationship('LopHocSinh', backref='lop', lazy=True)
    Hocs = relationship('Hoc', backref='lop', lazy=True)


class Hoc(db.Model):
    __tablename__ = 'hoc'
    Ma = Column ( Integer, primary_key=True, autoincrement=True)
    MaLop = Column( String(20),ForeignKey('lop.MaLop'), nullable=False)
    MaMonHoc = Column(String(20), ForeignKey('monhoc.MaMonHoc'), nullable=False)
    MaGiangVien = Column(String(20), ForeignKey('giangvien.MaGiangVien'), nullable=False)
    MaHocKi = Column(Integer, ForeignKey('hocki.MaHocKi'), nullable=False)


class HocSinh(db.Model):
    __tablename__ = "hocsinh"  # Corrected typo here
    MaHocSinh = Column(String(20), ForeignKey('account.id'),primary_key=True)
    DiemTbDauVao = Column(Float, nullable=False)
    Lop_HocSinhs = relationship('LopHocSinh', backref='hocsinh', lazy=True)
    Diems = relationship('Diem', backref='hocsinh', lazy=True)


class LopHocSinh(db.Model):
    __tablename__="lophocsinh"
    id = Column(Integer, primary_key=True, autoincrement=True)
    MaLop = Column(String(20), ForeignKey('lop.MaLop'),nullable=False)
    MaHocSinh = Column(String(20), ForeignKey('hocsinh.MaHocSinh'), nullable=False)
    NamTaoLop = Column(String(10), nullable=False)


class HocKi(db.Model):
    __tablename__="hocki"
    MaHocKi = Column(Integer, primary_key=True, autoincrement=True)
    TenHocKi = Column(String(20), nullable=True)
    NamHoc = Column(String(20), nullable=True)
    Diems = relationship('Diem', backref='hocki', lazy=False)
    Hocs = relationship('Hoc', backref='hocki', lazy=True)


class Diem(db.Model):
    DiemID = Column(Integer, primary_key=True, autoincrement=True)
    SoDiem = Column(Float, nullable=False)
    TypeDiem = Column(String(30), nullable=False)
    MaHocSinh = Column(String(20), ForeignKey('hocsinh.MaHocSinh'), nullable=False)
    MaMonHoc = Column(String(20), ForeignKey('monhoc.MaMonHoc'), nullable=False)
    MaHocKi = Column(Integer, ForeignKey('hocki.MaHocKi'), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

       # accout1 = [Account(id ='U001', TenDangNhap="Adim", MatKhau="123"),
       #          Account(id ='U002', TenDangNhap="GiangVien", MatKhau="123"),
       #          Account(id ='U003', TenDangNhap="NhanVien", MatKhau="123"),
       #          Account(id ='U004', TenDangNhap="HocSinh", MatKhau="1231"),
       #          Account(id ='U005', TenDangNhap="HocSinh", MatKhau="1231"),
       #          Account(id ='U006', TenDangNhap="HocSinh", MatKhau="1231")]
       #
       # for i in accout1:
       #     db.session.add(i)
       #
       # db.session.commit()

        # userinfor1 = [UserInfor(UserID='U001', Ho='Huynh Ngoc', Ten='Truong', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi', Email="abc@gmail.com"),
        #               UserInfor(UserID='U002', Ho='Nguyen Thanh', Ten='Trinh', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi', Email="abc1@gmail.com"),
        #               UserInfor(UserID='U003', Ho='Nguyễn', Ten='Anh', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi' ,Email="abc2@gmail.com"),
        #               UserInfor(UserID='U004', Ho='Nguyễn', Ten='Anh', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi', Email="abc3@gmail.com"),
        #               UserInfor(UserID='U005', Ho='Nguyễn', Ten='Anh', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi', Email="abc4@gmail.com"),
        #               UserInfor(UserID='U006', Ho='Nguyễn', Ten='Anh', NgaySinh=datetime(2000, 1, 1), GioiTinh='Nam', DiaChi='123 Lê Lợi' ,Email="abc5@gmail.com")]
        #
        # for i in userinfor1:
        #     db.session.add(i)
        #
        #
        # phone1 = [Phone(Number='0123456723', UserID='U001'),
        #           Phone(Number='0123456711', UserID='U001'),
        #           Phone(Number='0123456700', UserID='U002'),
        #           Phone(Number='0123888800', UserID='U003'),
        #           Phone(Number='0126666630', UserID='U004'),
        #           Phone(Number='0123777730', UserID='U005'),
        #           Phone(Number='0128888820', UserID='U006')]
        # for i in phone1:
        #     db.session.add(i)
        #
        #
        # permission1 = [Permission(Value='Tiếp nhận học sinh'),
        #                 Permission(Value='Nhập điểm'),
        #                 Permission(Value='Xuất điểm'),
        #                 Permission(Value='Điều chỉnh danh sách lớp'),
        #                 Permission(Value='Thống kê báo cáo'),
        #                 Permission(Value='Thay đổi quy định')]
        # for i in permission1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng PermissionUser
        # permission_user1 = [ PermissionUser(PermissionID=1, UserID='U001'),
        #                     PermissionUser(PermissionID=2, UserID='U001'),
        #                     PermissionUser(PermissionID=3, UserID='U001'),
        #                     PermissionUser(PermissionID=4, UserID='U001'),
        #                     PermissionUser(PermissionID=5, UserID='U001'),
        #                     PermissionUser(PermissionID=6, UserID='U001'),
        #                     PermissionUser(PermissionID=2, UserID='U002'),
        #                     PermissionUser(PermissionID=3, UserID='U002'),
        #                     PermissionUser(PermissionID=1, UserID='U003'),
        #                     PermissionUser(PermissionID=4, UserID='U003')]
        # for i in permission_user1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng Admin
        # admin1 = Admin(AdminID='U001')
        # db.session.add(admin1)
        #
        # # Thêm dữ liệu vào bảng NhanVienBoPhanKhac
        # nhanvien1 = NhanVienBoPhanKhac(MaNV='U003')
        # db.session.add(nhanvien1)
        #
        # # Thêm dữ liệu vào bảng MonHoc
        # monhoc1 = MonHoc(MaMonHoc='MH001', TenMonHoc='Toán học')
        # db.session.add(monhoc1)
        #
        # # Thêm dữ liệu vào bảng GiangVien
        # giangvien1 = GiangVien(MaGiangVien='U002', MaMonHoc='MH001')
        # db.session.add(giangvien1)
        #
        # # Thêm dữ liệu vào bảng Khoi
        # khoi1 = [ Khoi(TenKhoi='Khối 10'),
        #         Khoi(TenKhoi='Khối 11'),
        #         Khoi(TenKhoi='Khối 12')]
        # for i in khoi1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng Lop
        # lop1 = [ Lop(MaLop='L10A4', TenLop='Lớp 10A4', SiSo=30, MaKhoi=1),
        #         Lop(MaLop='L11A4', TenLop='Lớp 11A4', SiSo=30, MaKhoi=2),
        #         Lop(MaLop='L12A4', TenLop='Lớp 12A4', SiSo=30, MaKhoi=3)]
        # for i in lop1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng HocSinh
        #
        # hocsinh1 = [HocSinh(MaHocSinh='U004', DiemTbDauVao=8.5),
        #              HocSinh(MaHocSinh='U005', DiemTbDauVao=8.5),
        #              HocSinh(MaHocSinh='U006', DiemTbDauVao=8.5)]
        # for i in hocsinh1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng LopHocSinh
        # lophocsinh1 = [ LopHocSinh(MaLop='L10A4', MaHocSinh='U004'),
        #                 LopHocSinh(MaLop='L11A4', MaHocSinh='U005'),
        #                 LopHocSinh(MaLop='L12A4', MaHocSinh='U006')]
        # for i in lophocsinh1:
        #     db.session.add(i)
        #
        # # Thêm dữ liệu vào bảng HocKi
        # hocki1 = HocKi(TenHocKi='Học kỳ 1', NamHoc=2024)
        # db.session.add(hocki1)
        #
        # # Thêm dữ liệu vào bảng Diem
        # diem1 = [Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U004', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U004', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='1 tiết', MaHocSinh='U004', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='Cuối kì', MaHocSinh='U004', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U005', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U005', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='1 tiết', MaHocSinh='U005', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='Cuối kì', MaHocSinh='U005', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U006', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='15 phút', MaHocSinh='U006', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='1 tiết', MaHocSinh='U006', MaMonHoc='MH001', MaHocKi=1),
        #         Diem(SoDiem=9.0, TypeDiem='Cuối kì', MaHocSinh='U006', MaMonHoc='MH001', MaHocKi=1)]
        # for i in diem1:
        #     db.session.add(i)
        #
        # # Lưu tất cả các thay đổi
        # db.session.commit()
