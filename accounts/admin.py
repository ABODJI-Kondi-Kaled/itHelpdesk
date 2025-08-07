from django.contrib import admin
from django import forms

# from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
# from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Traduction
from django.utils.translation import gettext_lazy as _

from .models import Profile, User

# Creating a custom admin Form

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if pass1 and pass2 and pass1 != pass2:
            raise ValueError(_('Passwords don\'t match'))
        
        return pass2
    
    def save(self, commit=True):
        """
        Args:
            - commit : Bool that defines if the intance of the model user should be save in db or not
        
        """
        user = super().save(commit=False)

        user.set_password(self.cleaned_data.get('password2'))

        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # fields to be added in the Admin panel

    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',

    ]

    list_filter = ['is_active', 'is_staff', 'groups']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets =(
        (None, {'fields':('email', 'password')}),
        (_('Personal Informations'), {
            'fields': ('last_name', 'first_name')
        }),
        (_('Permissions'), {
            'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),

        (_('Important Dates'), {
            'fields':('last_login',)
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes':('wide',),
                'fields':[
                    'email', 'last_name', 'first_name',
                    'is_active', 'is_staff', 'is_superuser', 
                    'groups', 'user_permissions',           
                ]
            },
        ),
    )

admin.site.register(User, UserAdmin)   

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user.email',
        'bio'
    ]

    search_fields='user.email'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def has_add_permission(self, request):
        
            return request.user.is_superuser
        
    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser or request.user == obj.user:
            return True
        if not obj:
            return True # Allow view of the changelist
        
    def has_view_permission(self, request, obj = None):
        return self.has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj = None):
        return False # Block deletion for all accounts

admin.site.register(Profile, ProfileAdmin)


