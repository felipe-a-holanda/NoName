from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User, UserProfile
from .forms import UserProfileForm
from django.utils.translation import ugettext_lazy as _


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'name', 'email', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    #form = UserProfileForm


    list_display = ['name', 'hometown', 'birthday']
    raw_id_fields = ['hometown']
    #list_filter = ['language']
    
    def name(self, obj):
        return obj.user.name

    def birthday2(self, obj):
        if obj.hometown:

            return obj.birthday.astimezone(obj.hometown.timezone).replace(tzinfo=None)
        else:
            return obj.birthday

    #birthday.short_description = "Payment time stamp"
