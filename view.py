from flask_admin.form.upload import thumbgen_filename
from jinja2 import Markup
from flask import redirect,url_for
from flask_admin.contrib.sqla import ModelView, view
from flask_login import current_user
from flask_admin import form
from config import config_data
import datetime

class UserModelView(ModelView):
    can_delete = True
    page_size = 50
    create_modal = True
    edit_modal=True

    l1 = ['student','admin']
    l2 = []
    for i in range(0, len(l1)):
        l2.append((l1[i], l1[i]))
    form_choices = {
        'access': l2
    }

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True

class PostsModelView(ModelView):
    can_delete=True
    page_size = 50
    create_modal = True
    edit_modal = True

    column_exclude_list = ['content','slug']
    form_excluded_columns=['slug','date']

    def on_model_change(self, form, model, is_created):
        if is_created and not model.slug:
            model.slug = str(model.title).replace(' ','').strip()
            model.date = datetime.datetime.now()

    def _list_thumbnail(view, context, model, name):
        print(f'name: {name}')
        if name == 'image':
            return model.image
        else:
            return ''

    column_formatters = {
        'image': _list_thumbnail,
    }
    form_extra_fields = {
        'image': form.ImageUploadField('image', base_path=config_data["image_file_path"], thumbnail_size=(100, 100, True)),
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True

class MessageModelView(ModelView):
    can_delete = True
    can_create = False
    page_size = 50
    create_modal = True
    edit_modal=True
    # column_searchable_list = ('studentid')
    form_excluded_columns = ['studentid','message','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.reply == '')

    def on_model_change(self, form, model, is_created):
        if is_created and not model.date:
            model.date = datetime.datetime.now()

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True

class MessageModelView2(ModelView):
    can_delete = True
    can_create = False
    page_size = 50
    create_modal = True
    edit_modal=True
    # column_searchable_list = ('studentid')
    form_excluded_columns = ['studentid','message','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.reply != '')


    def on_model_change(self, form, model, is_created):
        if is_created and not model.date:
            model.date = datetime.datetime.now()


    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True

class SuggestionModelView(ModelView):
    can_create=False
    can_delete=True
    can_edit=True
    page_size = 50
    create_modal = True
    edit_modal = True
    form_excluded_columns=['id','requestee','message','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.approved == False)

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True


class SuggestionModelView2(ModelView):
    can_create=False
    can_delete=True
    can_edit=True
    page_size = 50
    create_modal = True
    edit_modal = True
    form_excluded_columns=['id','requestee','message','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.approved == True)

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True



class ConcernModelView(ModelView):
    can_create=False
    can_delete=True
    can_edit=True
    page_size = 50
    create_modal = True
    edit_modal = True
    form_excluded_columns=['id','requestee','message','image','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.approved == False)

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True


class ConcernModelView2(ModelView):
    can_create=False
    can_delete=True
    can_edit=True
    page_size = 50
    create_modal = True
    edit_modal = True
    form_excluded_columns=['id','requestee','message','image','date']

    def get_query(self):
        return self.session.query(self.model).filter(self.model.approved == True)

    def is_accessible(self):
        if current_user.is_authenticated :
            if current_user.access == 'admin':
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        return True
        