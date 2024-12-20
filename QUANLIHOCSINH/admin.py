from pstats import Stats

from QUANLIHOCSINH import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
import models
from flask import redirect,request
import dao
from flask_login import current_user, logout_user
admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')

class AdminView(ModelView):
    column_display_pk = True
    can_export = True
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(models.Role.Admin)


class ThongbaoView(AdminView):

    column_list = ['PermissionID', 'UserID']

    column_searchable_list = ['PermissionID', 'UserID']
    # column_exclute_list = ['']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'UserID': 'Mã người dùng'
    }
    list_template  = 'admin/thongbao.html'


class ViewMonHoc(AdminView):
    # column_list = ['MaMonHoc', 'UserID']

    # column_searchable_list = [''] tìm kieesm
    # column_exclute_list = ['']

    column_labels = {
        'MaMonHoc': 'Mã môn học',
        'TenMonHoc': 'Tên môn học'
    }


class ViewAccout(AdminView):


    # def get_query(self):
    #     return super(ViewAccout, self).get_query().filter(models.Account.Active == True)
    #
    # # Đảm bảo bộ đếm cũng áp dụng bộ lọc Active = True
    # def get_count_query(self):
    #     return super(ViewAccout, self).get_count_query().filter(models.Account.Active == True)

    column_searchable_list = ['TenDangNhap', 'id', 'NgayTao']

    column_labels = {
        'id': 'Mã người dùng',
        'TenDangNhap': 'Tên đăng nhập',
        'NgayTao': 'Ngày tạo',
        'Active': 'Trạng thái'

    }

class ThongTinUser(AdminView):

    column_list = ['Ho', 'Ten', 'NgaySinh', 'GioiTinh', 'DiaChi', 'Email']

    # def get_query(self):
    #     # Lấy danh sách học sinh chưa có lớp
    #     hoc_sinh_chua_lop = dao.HocSinhNotLop(449)  # Dựng phương thức này trả về danh sách học sinh chưa có lớp
    #     # Tạo truy vấn lọc các học sinh chưa có lớp
    #     query = super(ThongTinUser, self).get_query()
    #     return query.filter(models.UserInfor.UserID.in_([i.MaHocSinh for i in hoc_sinh_chua_lop]))

    column_searchable_list = ['Ho', 'Ten', 'NgaySinh', 'GioiTinh', 'DiaChi', 'Email']

    column_labels = {
        'UserID' : 'Mã người dùng',
        'Ho': 'Họ',
        'Ten': 'Tên',
        'NgaySinh': 'Ngày sinh',
        'GioiTinh': 'Giới tính',
        'DiaChi': 'Địa chỉ',
        'Email': 'Email'
    }

class ViewLop(AdminView):

    # column_list = ['MaMonHoc', 'UserID']

    column_searchable_list = ['MaLop', 'TenLop']
    # column_exclute_list = ['']

    column_labels = {
        'MaLop': 'Mã lớp',
        'TenLop': 'Tên lớp',
        'SiSo' : 'Sĩ số'
    }


class ViewLopHocSinh(AdminView):

    can_export = True
    column_list = ['MaLop', 'MaHocSinh', 'NamTaoLop']

    column_searchable_list = ['id' , 'MaLop', 'MaHocSinh', 'NamTaoLop']
    # column_exclute_list = ['']

    column_labels = {
        'MaLop': 'Mã lớp',
        'MaHocSinh' : 'Mã học sinh',
        'NamTaoLop' : 'Ngày tạo'
    }


class ViewPerMission(AdminView):
    can_export = True

    column_searchable_list = ['Value']
    # column_exclute_list = ['']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'Value': 'Quyền'
    }

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(models.Role.Admin)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class ThongKeView(AuthenticatedView):
    @expose('/')
    def index(self):
        danh_sach_mon_hoc = dao.Load_MonHoc()
        danh_sach_hoc_ki = dao.load_hoc_ki()

        return self.render('admin/baocaothongke.html', danh_sach_mon_hoc=danh_sach_mon_hoc, danh_sach_hoc_ki=danh_sach_hoc_ki)

    @expose('/submit', methods=["POST"])
    def submit(self):
        danh_sach_mon_hoc = dao.Load_MonHoc()
        danh_sach_hoc_ki = dao.load_hoc_ki()

        MonHoc = request.form.get('MonHoc')
        HocKi = request.form.get('HocKi')

        danh_sach_lop_hoc = dao.LoadLopHoc(MonHoc, HocKi)
        TenMonHoc = ""
        TenHocKi = ""
        TenNamHoc = ""
        ds_lop = []

        for MH in danh_sach_mon_hoc:
            if MonHoc == MH.MaMonHoc:
                TenMonHoc = MH.TenMonHoc
        for Hk in danh_sach_hoc_ki:
            if HocKi == Hk.MaHocKi:
                TenHocKi = Hk.TenHocKi
                TenNamHoc = Hk.NamHoc

        stt = 0
        for lop in danh_sach_lop_hoc:
            stt += 1
            soluongdat = dao.tinh_so_luong_dat_cua_lop(lop.MaLop, MonHoc, HocKi)
            tile = round((soluongdat / lop.SiSo) * 100, 2) if lop.SiSo != 0 else 0
            ds_lop.append([stt, lop.TenLop, lop.SiSo, soluongdat, tile])

        return self.render('admin/baocaothongke.html',
                           danh_sach_mon_hoc=danh_sach_mon_hoc,
                           danh_sach_hoc_ki=danh_sach_hoc_ki,
                           TenMonHoc=TenMonHoc,
                           TenHocKi=TenHocKi,
                           TenNamHoc=TenNamHoc,
                           Lop=ds_lop)

admin.add_view(ViewAccout(models.Account, db.session, name="Tài khoản"))
admin.add_view(ThongTinUser(models.UserInfor, db.session, name="Thông tin tài khoản"))
admin.add_view(ViewMonHoc(models.MonHoc, db.session, name="Môn học"))
admin.add_view(ViewLop(models.Lop, db.session, name="Lớp"))
admin.add_view(ViewLopHocSinh(models.LopHocSinh, db.session, name="Lớp-Học sinh"))
admin.add_view(ViewPerMission(models.Permission, db.session, name="Quyền"))

admin.add_view(ThongbaoView(models.PermissionUser, db.session, name="Thông báo "))

admin.add_view(ThongKeView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))