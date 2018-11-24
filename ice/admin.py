from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

# class AssetAdmin(admin.ModelAdmin):
#     list_display = ('asset_type', 'name', 'sn', 'manufactory', 'management_ip',)


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users, Includes all the required fields.
    plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'token')

    def clean_password2(self):
        # Check that the two password entries are matched
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users profile. Includes all the fields on the user,
    but replaces the password field with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see"
                   "this user password, but you can change the password"
                   "using<a href=\"../password/\">this form</a>"))

    class Meta:
        model = UserProfile
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):

        return self.initial["password"]


class UserProfileAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'name', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tel', 'mobile', 'memo')}),
        ('API TOKEN info', {'fields': ('token',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('账户有效期', {'fields': ('valid_begin_time', 'valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin')}
         ),
    )

    search_fields = ('email',)
    ordering = ['email']
    filter_horizontal = ()


class ServerInline(admin.TabularInline):
    model = Server
    exclude = ('memo',)
    # readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'sn', 'name', 'manufactory', 'management_ip', 'idc', 'department', 'admin', 'trade_date', 'status')
    inlines = [ServerInline]
    search_fields = ['sn']
    # list_filter = ['idc','manufactory', 'department', 'asset_type']
    # choice_fields = ('status')
    choice_fields = ('asset_type', 'status')
    fk_fields = ('manufactory', 'idc', 'department', 'admin')
    list_per_page = 10
    list_filter = ('asset_type', 'status', 'manufactory', 'idc', 'department', 'admin', 'trade_date')
    dynamic_fk = 'asset_type'
    # dynamic_list_display = ('model', 'sub_asset_type', 'os_type', 'os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Server)
admin.site.register(IDC)
admin.site.register(Department)
admin.site.register(Contract)
admin.site.register(Manufactory)
admin.site.register(Tag)
admin.site.register(Software)
