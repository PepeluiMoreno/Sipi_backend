from rbac.models import Application, Permission, Role, RolePermission

def register_application():
    """
    Registers the heritage_buildings application and its transactions in RBAC.
    """
    # Create or get the application
    app, created = Application.objects.get_or_create(
        name='heritage_buildings',
        defaults={'description': 'Application for managing heritage buildings'}
    )

    # Define the transactions (permissions)
    transactions = [
        {'code': 'view_buildings', 'description': 'View heritage buildings'},
        {'code': 'create_buildings', 'description': 'Create heritage buildings'},
        {'code': 'edit_buildings', 'description': 'Edit heritage buildings'},
        {'code': 'delete_buildings', 'description': 'Delete heritage buildings'},
    ]

    # Create permissions
    for transaction in transactions:
        Permission.objects.get_or_create(
            code=transaction['code'],
            application=app,
            defaults={'description': transaction['description']}
        )

    # Create the admin role for this application
    admin_role, created = Role.objects.get_or_create(
        name='heritage_buildings_admin',
        application=app,
        defaults={'description': 'Administrator role for heritage buildings'}
    )

    # Assign all permissions to the admin role
    for permission in Permission.objects.filter(application=app):
        RolePermission.objects.get_or_create(role=admin_role, permission=permission)

    return app