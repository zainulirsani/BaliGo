from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout

def check_admin_role(request):
    if request.user.is_superuser == True or request.user.role == 'adm_outlet' or request.user.role == 'adm_gudang':
        return True
    else:
        try:
            auth_logout(request)
        except:
            pass
        return False

# Just Super admin
def super_admin_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            superadmin = request.user.is_superuser
            active = request.user.is_active
            if active == True and superadmin == True :
                return func(request, *args, **kwargs)
            else:
                # if request.user.is_authenticated:
                #     auth_logout(request)
                return redirect(path_url)
        return wrapper
    return decorator

# Super admin , admin gudang , admin outlet bisa mengakses
def user_admin_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            superadmin = request.user.is_superuser
            admin_role = request.user.role
            active = request.user.is_active
            if active == True and (superadmin == True or admin_role == 'adm_gudang' or admin_role == 'adm_outlet'):
                return func(request, *args, **kwargs)
            else:
                # if request.user.is_authenticated:
                #     auth_logout(request)
                return redirect(path_url)
        return wrapper
    return decorator

# Super admin dan Admin Gudang saja yg bisa mengakses
def admin_gudang_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            superadmin = request.user.is_superuser
            admin_role = request.user.role
            active = request.user.is_active
            if active == True and (superadmin == True or admin_role == 'adm_gudang'):
                return func(request, *args, **kwargs)
            else:
                # if request.user.is_authenticated:
                #     auth_logout(request)
                return redirect(path_url)
        return wrapper
    return decorator

# Super admin dan Admin Outlet saja yg bisa mengakses
def admin_outlet_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            superadmin = request.user.is_superuser
            admin_role = request.user.role
            active = request.user.is_active
            if active == True and (superadmin == True or admin_role == 'adm_outlet'):
                return func(request, *args, **kwargs)
            else:
                # if request.user.is_authenticated:
                #     auth_logout(request)
                return redirect(path_url)
        return wrapper
    return decorator

# Super admin dan Kurir saja yang bisa mengakses
def kurir_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            superadmin = request.user.is_superuser
            role = request.user.role
            active = request.user.is_active
            if active == True and (superadmin == True or role == 'kurir'):
                return func(request, *args, **kwargs)
            else:
                # if request.user.is_authenticated:
                #     auth_logout(request)
                return redirect(path_url)
        return wrapper
    return decorator

def user_customer_check(path_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                active = request.user.is_active
                superadmin = request.user.is_superuser
                admin_role = request.user.role
                register = request.user.register_sebagai
                if active == True and (superadmin == False and admin_role != 'adm_gudang' and admin_role != 'adm_outlet') and (register == 'personal' or register == 'goverment' or register == 'company'):
                    return func(request, *args, **kwargs)
                else:
                    if request.user.is_authenticated:
                        auth_logout(request)
                        return redirect(path_url)
            else:
                return redirect(path_url)
        return wrapper
    return decorator