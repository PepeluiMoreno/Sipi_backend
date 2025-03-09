from rbac.utils import has_permission

def menu_apps(request):
    apps = []
    if has_permission(request.user, 'view_buildings', 'heritage_buildings'):
        apps.append({'name': 'heritage_buildings', 'url': 'heritage_buildings/'})
    if has_permission(request.user, 'view_documents', 'documents'):
        apps.append({'name': 'documents', 'url': 'documents/'})
    if has_permission(request.user, 'view_clients', 'clientes'):
        apps.append({'name': 'clientes', 'url': 'clientes/'})
    return {'menu_apps': apps}