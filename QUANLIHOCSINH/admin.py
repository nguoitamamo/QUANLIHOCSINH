

from QUANLIHOCSINH import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import models
import dao

admin = Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')

class BaseView(ModelView):
    column_display_pk = True
    can_export = True


class ThongbaoView(BaseView):

    column_list = ['PermissionID', 'UserID']

    column_searchable_list = ['PermissionID', 'UserID']
    # column_exclute_list = ['']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'UserID': 'Mã người dùng'
    }
    list_template  = 'admin/thongbao.html'


class ViewMonHoc(BaseView):
    # column_list = ['MaMonHoc', 'UserID']

    # column_searchable_list = [''] tìm kieesm
    # column_exclute_list = ['']

    column_labels = {
        'MaMonHoc': 'Mã môn học',
        'TenMonHoc': 'Tên môn học'
    }


class ViewAccout(BaseView):


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

class ThongTinUser(BaseView):

    column_list = ['Ho', 'Ten', 'NgaySinh', 'GioiTinh', 'DiaChi', 'Email']

    def get_query(self):
        # Lấy danh sách học sinh chưa có lớp
        hoc_sinh_chua_lop = dao.HocSinhNotLop(449)  # Dựng phương thức này trả về danh sách học sinh chưa có lớp
        # Tạo truy vấn lọc các học sinh chưa có lớp
        query = super(ThongTinUser, self).get_query()
        return query.filter(models.UserInfor.UserID.in_([i.MaHocSinh for i in hoc_sinh_chua_lop]))

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

class ViewLop(BaseView):

    # column_list = ['MaMonHoc', 'UserID']

    column_searchable_list = ['MaLop', 'TenLop']
    # column_exclute_list = ['']

    column_labels = {
        'MaLop': 'Mã lớp',
        'TenLop': 'Tên lớp',
        'SiSo' : 'Sĩ số'
    }


class ViewLopHocSinh(BaseView):

    can_export = True
    column_list = ['MaLop', 'MaHocSinh', 'NamTaoLop']

    column_searchable_list = ['id' , 'MaLop', 'MaHocSinh', 'NamTaoLop']
    # column_exclute_list = ['']

    column_labels = {
        'MaLop': 'Mã lớp',
        'MaHocSinh' : 'Mã học sinh',
        'NamTaoLop' : 'Ngày tạo'
    }


class ViewPerMission(BaseView):
    can_export = True

    column_searchable_list = ['Value']
    # column_exclute_list = ['']

    column_labels = {
        'PermissionID': 'Mã quyền',
        'Value': 'Quyền'
    }

admin.add_view(ViewAccout(models.Account, db.session, name="Tài khoản"))
admin.add_view(ThongTinUser(models.UserInfor, db.session, name="Thông tin tài khoản"))
admin.add_view(ViewMonHoc(models.MonHoc, db.session, name="Môn học"))
admin.add_view(ViewLop(models.Lop, db.session, name="Lớp"))
admin.add_view(ViewLopHocSinh(models.LopHocSinh, db.session, name="Lớp-Học sinh"))
admin.add_view(ViewPerMission(models.Permission, db.session, name="Quyền"))

admin.add_view(ThongbaoView(models.PermissionUser, db.session, name="Thông báo "))
