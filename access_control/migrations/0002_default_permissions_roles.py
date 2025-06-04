from django.db import migrations


def create_permissions_and_roles(apps, schema_editor):
    Permission = apps.get_model('access_control', 'Permission')
    Role = apps.get_model('access_control', 'Role')

    permission_codenames = [
        'can_add_permission',
        'can_change_permission',
        'can_delete_permission',
        'can_view_permission',
        'can_add_role',
        'can_change_role',
        'can_delete_role',
        'can_view_role',
        'can_assign_permission_to_role',
        'can_remove_permission_from_role',
        'can_assign_role_to_user',
        'can_remove_role_from_user',
        'can_assign_target_to_user',
        'can_remove_target_from_user',
        'can_view_activity',
        'can_view_activity_target',
    ]

    permissions = []
    for codename in permission_codenames:
        perm, _ = Permission.objects.get_or_create(
            codename=codename, defaults={'name': codename}
        )
        permissions.append(perm)

    roles = {}
    for role_name in ['admin', 'manager', 'user']:
        role, _ = Role.objects.get_or_create(name=role_name)
        roles[role_name] = role

    # Give all permissions to the admin role
    admin_role = roles['admin']
    admin_role.permissions.add(*permissions)


def remove_permissions_and_roles(apps, schema_editor):
    Permission = apps.get_model('access_control', 'Permission')
    Role = apps.get_model('access_control', 'Role')
    admin_role = Role.objects.filter(name='admin').first()
    if admin_role:
        admin_role.permissions.clear()
    Permission.objects.filter(codename__in=[
        'can_add_permission',
        'can_change_permission',
        'can_delete_permission',
        'can_view_permission',
        'can_add_role',
        'can_change_role',
        'can_delete_role',
        'can_view_role',
        'can_assign_permission_to_role',
        'can_remove_permission_from_role',
        'can_assign_role_to_user',
        'can_remove_role_from_user',
        'can_assign_target_to_user',
        'can_remove_target_from_user',
        'can_view_activity',
        'can_view_activity_target',
    ]).delete()
    Role.objects.filter(name__in=['admin', 'manager', 'user']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('access_control', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_permissions_and_roles, remove_permissions_and_roles),
    ]
