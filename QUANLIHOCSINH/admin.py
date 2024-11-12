from QUANLIHOCSINH import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import models

admin = Admin(app= app , name= "E-commerce Administration", template_mode='bootstrap4')

admin.add_view(ModelView(models.Account, db.session))
admin.add_view(ModelView(models.MonHoc, db.session))
admin.add_view(ModelView(models.Lop, db.session))
admin.add_view(ModelView(models.LopHocSinh, db.session))