from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('enabled', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='groups_updated')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='groups_deleted')
    deleted_at = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField(default=1)

    class Meta:
        db_table = 'groups'

class UserGroup(models.Model):
    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('ADMIN', 'Admin'),
        ('OWNER', 'Owner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_groups')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usergroups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='usergroups_updated')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_groups'
        unique_together = ('user', 'group')

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permissions'

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rolepermissions_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')

class AccessControl(models.Model):
    entity_type = models.CharField(max_length=50)
    entity_id = models.BigIntegerField()
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='access_controls')
    granted_to_type = models.CharField(max_length=20)  # 'USER' ou 'ROLE'
    granted_to_id = models.BigIntegerField()
    is_allowed = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accesscontrols_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accesscontrols_updated')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'access_controls'
        unique_together = ('entity_type', 'entity_id', 'permission', 'granted_to_type', 'granted_to_id') 