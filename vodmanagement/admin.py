from django.contrib import admin
# Register your models here.
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.core.management import call_command
from vodmanagement.api.serializers import *
from vodmanagement.custom_widget import KindEditor
from django import forms
from django.contrib import messages
from uuslug import uuslug
import re

from django.conf import settings
from .models import *
from .utils import *
from django.utils.translation import ugettext_lazy


class VodForm(forms.ModelForm):
    '''docstring for VodForm'''

    def __init__(self, *args, **kwargs):
        super(VodForm, self).__init__(*args, **kwargs)
        # if (self.instance.image.name is '' or self.instance.image.name is None) \
        #         and (self.instance.video.name is '' or self.instance.video.name is None):
        #     print('save path is empty')
        #     self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())
        # else:
        #     print('save path is:', self.instance.save_path)
        #     self.fields['save_path'] = forms.ChoiceField(choices=get_save_path_choice(self.instance.save_path))
        #     # self.fields['save_path'].widget.attrs['disabled='disabled''] = True
        # for instance in self.fields['category'].queryset:
        #     create_category_path(name=instance.name)

    def clean_title(self):
        print('vod form clean')
        data = self.cleaned_data['title']
        return data

    def clean(self):
        print('vod form clean all')
        return super(VodForm, self).clean()

    # def save(self, commit=True):
    #     instance = super(VodForm, self).save(commit=False)
    #     instance.save()
    #     self.save_m2m()
    #     return instance

    class Meta:
        model = Vod
        fields = (
            'category',
            'save_path',
            'video',
            'title',
            'image',
            'year',
            'description',
            'slug',
            'search_word',
        )
        widgets = {
            'description': KindEditor(),
        }


@admin.register(Vod)
class VodModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'category', 'file_size', 'duration', 'definition', 'year', 'region',
                    'view_count', 'timestamp', 'colored_active']  # image_tag
    list_display_links = ['image_tag', 'timestamp']  # image_tag
    list_editable = ['category', 'title', 'definition', 'year']
    list_filter = ['year', 'category']
    # filter_horizontal = ['video_list']
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    search_fields = ['title', 'description', 'search_word']
    actions = ['delete_hard', 'copy_objects', 'clear_view_count', 'activate_vod', 'deactivate_vod', 'backup']
    form = VodForm
    fieldsets = [
        ('描述', {'fields': ['category', 'save_path', 'year', 'region', 'description', 'select_name', 'active']}),
        ('文件', {'fields': ['image', 'video', 'title']}),
        ('视频列表', {'fields': ['video_list']}),
        ('高级', {'fields': ['slug', 'search_word'], 'classes': ['collapse']})
    ]

    change_form_template = 'vodmanagement/change_form.html'
    add_form_template = 'vodmanagement/change_form.html'

    # def get_form(self, request, *args, **kwargs):
    #     form = super(VodModelAdmin, self).get_form(request, *args, **kwargs)
    #     form.base_fields['creator'].initial = request.user
    #     return form

    def save_model(self, request, obj, form, change):
        # obj.creator = request.user
        super(VodModelAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, object):
        try:
            delete_hard(object.image.path)
        except:
            pass
        try:
            delete_hard(object.video.path)
        except:
            pass
        object.delete()

    def delete_hard(self, request, queryset):
        for obj in queryset:
            # try:
            #     delete_hard(obj.image.path)
            # except:
            #     pass
            # try:
            #     delete_hard(obj.video.path)
            # except:
            #     pass
            obj.image.delete()
            obj.video.delete()
            obj.delete()

    delete_hard.short_description = '删除硬盘上的文件'

    def copy_objects(self, request, queryset):
        for obj in queryset:
            for i in range(4):
                new_obj = obj
                new_obj.pk = None
                # new_obj.slug = create_slug(new_obj)
                new_obj.slug = uuslug(new_obj.title, instance=new_obj)
                new_obj.save()
        self.message_user(request, '%s item successfully copyed.' % queryset.count()
                          , messages.SUCCESS)

    def activate_vod(self, request, queryset):
        for item in queryset:
            item.active = 1
            item.save()
        self.message_user(request, '%s个节目成功激活.' % queryset.count()
                          , messages.SUCCESS)

    activate_vod.short_description = '激活节目列表'

    def deactivate_vod(self, request, queryset):
        for item in queryset:
            item.active = 0
            item.save()
        self.message_user(request, '%s个节目成功取消激活.' % queryset.count()
                          , messages.SUCCESS)

    deactivate_vod.short_description = '取消激活节目'

    def clear_view_count(self, request, queryset):
        queryset.update(view_count=0)
        self.message_user(request, '%s item successfully cleared view count.' % queryset.count()
                          , messages.SUCCESS)

    class Media:
        pass
        # js = ('http://code.jquery.com/jquery.min.js',)
        # class Meta:
        # model = Vod


class MyAdminForm(forms.ModelForm):
    class Meta:
        model = VideoCategory
        widgets = {
            'type': forms.RadioSelect,
        }
        fields = '__all__'


@admin.register(VideoCategory)
class VideoCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_description', 'colored_level', 'type', 'isSecret']
    list_editable = ['isSecret']
    search_fields = ['name']
    filter_horizontal = ['subset']
    ordering = ['level']
    form = MyAdminForm
    fieldsets = [
        ('描述', {'fields': ['name', 'level', 'subset']}),
        ('高级', {'fields': ['isSecret', 'type'], 'classes': ['collapse']})
    ]

    def category_description(self, obj):
        return str(obj)

    category_description.short_description = '分类名称'


class LinkModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_editable = ['category']


class MultipleUploadForm(forms.ModelForm):
    '''docstring for VodForm'''

    def __init__(self, *args, **kwargs):
        super(MultipleUploadForm, self).__init__(*args, **kwargs)
        self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())

    class Meta:
        model = MultipleUpload
        fields = '__all__'


class RestoreForm(forms.ModelForm):
    '''docstring for VodForm'''

    def __init__(self, *args, **kwargs):
        super(RestoreForm, self).__init__(*args, **kwargs)
        # self.fields['save_path'] = forms.ChoiceField(choices=save_path_choices())

    class Meta:
        model = Restore
        fields = '__all__'


@admin.register(MultipleUpload)
class MultipleUploadModelAdmin(admin.ModelAdmin):
    form = MultipleUploadForm
    change_form_template = 'vodmanagement/MultipleUpload/change_form.html'
    add_form_template = 'vodmanagement/MultipleUpload/change_form.html'


@admin.register(Restore)
class RestoreModelAdmin(admin.ModelAdmin):
    actions = ['restore_db']
    form = RestoreForm
    list_display = ['filename', 'timestamp']
    list_display_links = ['timestamp']
    readonly_fields = ['dump_file']
    fieldsets = [
        ('基本', {'fields': ['filename']}),
        ('高级', {'fields': ['dump_file', 'upload_restore_file'], 'classes': ['collapse']})
    ]
    # readonly_fields = ['dump_file']
    # change_form_template = 'vodmanagement/change_form.html'
    # add_form_template = 'vodmanagement/change_form.html'

    def restore_db(self, request, queryset):
        if len(queryset) > 1:
            return self.message_user(request, '只能选择一个数据来恢复！', messages.ERROR)
        for item in queryset:
            try:
                call_command('dbrestore', '--database', 'default', '-i', Path(item.dump_file).name)
            except Exception as e:
                return self.message_user(request, '数据库未备份完成，请稍后再试!', messages.ERROR)
        self.message_user(request, '成功恢复数据', messages.SUCCESS)

    restore_db.short_description = '恢复数据'

admin.site.register(FileDirectory)
admin.site.register(VideoRegion)
