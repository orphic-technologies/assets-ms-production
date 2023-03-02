
from django.shortcuts import render
from django.contrib.auth import (
    logout,
)
from django.http import JsonResponse
from .models import User
from products.models import Product, AssestAssign, Vendor, AssestReturn
from .forms import LoginForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .utils import validate_password
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
import json
import random
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime
from django.db.models import Q
# ---- for converting json value which is stringified in ajax
from urllib import parse
# -----------------------------------------------------------

# Create your views here.


def loginpage(request):
    if not request.session.has_key("user"):
        loginForm = LoginForm()
        return render(request, "login.html", {"form": loginForm})
    else:
        return HttpResponseRedirect("../home")


def home(request):
    if request.session.has_key("user"):
        assignedproduct = AssestAssign.objects.all()[:4][::-1]
        totalassets = Product.objects.filter(status='true')
        assignedassets = AssestAssign.objects.all()
        assignedquantity = assignedassets.count()
        availablequantity = totalassets.count() - assignedquantity

        totalquantity = availablequantity+assignedquantity
        if totalquantity != 0:
            availablepercent = (availablequantity/totalquantity)*100
            asiignpercent = (assignedquantity/totalquantity)*100
        else:
            availablepercent = 0
            asiignpercent = 0

        requiresrepair = totalassets.filter(
            condition_of_asset='Requires Repair', status='true').count()

        token_list = AssestAssign.objects.values_list(
            'token', flat=True
        ).distinct()
        group_by_token = {}
        for token in token_list:
            group_by_token[token] = AssestAssign.objects.filter(token=token)

        grouped_acc_to_token = tuple(group_by_token.items())[::-1]

        paginator = Paginator(grouped_acc_to_token, 3)
        page_number = request.GET.get("page")
        assignedproduct = paginator.get_page(page_number)
        # -------------------------------------------------------------------

        context = {
            "assetstoreturn": assignedproduct,
            "totalasset": totalquantity,
            "assignedassets": assignedquantity,
            "availableassets": availablequantity,
            "availablepercent": availablepercent,
            "asiignpercent": asiignpercent,
            "requiresrepair": requiresrepair,

        }
        return render(request, "index.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def search(request):
    if request.session.has_key("user"):
        # second is default parameter which is empty
        if request.method == "GET":
            query = request.GET.get("query", "")

            products = Product.objects.filter(Q(name_of_asset__icontains=query) | Q(asset_code=query) | Q(assets_pool__icontains=query) | Q(product_category__icontains=query) | Q(
                specifications__brand__icontains=query) | Q(asset_location__icontains=query) | Q(user__fullname__icontains=query)
                | Q(condition_of_asset__icontains=query) | Q(user__current_position__icontains=query) |
                Q(vendor__name_of_vendor__icontains=query)).filter(status='true')

            context = {
                "products": products,
            }
            return render(request, "search.html", context)
        else:
            products = Product.objects.filter(status='true')

            context = {
                "products": products,
            }
            return render(request, "search.html", context)
    else:
        return HttpResponseRedirect("../")


def assignasset(request, values):
    if request.session.has_key("user"):
        if request.method == "POST":
            return render(request, "assign.html")
        else:
            assetobjects = {}
            # ---- for converting json value which is stringified in ajax
            converted = parse.unquote(values)
            print(values)
            checkassets = json.loads(converted)
            for key, value in checkassets.items():
                assets = Product.objects.get(asset_code=key)
                assetobjects[assets] = value

            totaluser = User.objects.all()
            context = {
                "assetdict": assetobjects,
                "totaluser": totaluser,
                "assetdictsent": values,
            }
            return render(request, "assign.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def assignassettemplate(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            checkassets = request.POST.get("dictval")
            checkassets = json.loads(checkassets)
            return JsonResponse(checkassets)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def addassignasset(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            nameofstaff = request.POST.get("user")
            purpose = request.POST.get("purpose")
            date_of_issue = request.POST.get("dateofi")
            estimated_date_of_return = request.POST.get(
                "dateofe")
            asset_info = request.POST.get("hiddenvalue")
            asset_verified_by = User.objects.get(
                username=request.session['user'])
            print(nameofstaff)
            nameofstaff = User.objects.get(username=nameofstaff)

            # ---- for converting json value which is stringified in ajax
            converted = parse.unquote(asset_info)
            # -----------------------------------------------------------
            assignassets = json.loads(converted)
            token = f'{nameofstaff.username[:3]}{random.randint(1,999999)}{date_of_issue[-2:]}'

            for key, value in assignassets.items():
                assets = Product.objects.get(
                    asset_code=key)
                try:
                    # -- object pf product, with all the values to be stored
                    assetassign = AssestAssign(
                        nameofstaff=nameofstaff.fullname,
                        purpose=purpose,
                        date_of_issue=date_of_issue,
                        estimated_date_of_return=estimated_date_of_return,
                        asset_info=assets,
                        asset_verified_by=asset_verified_by,
                        token=token,
                    )
                    # -- this object is saved with all the above data
                    assetassign.save()
                    # ----------------------------------------------

                    # ----------- updating asset after assignment ----
                    assets.availale_status = 'false'
                    assets.save(update_fields=[
                        'availale_status'])
                    assets.user.add(nameofstaff)
                    assets.save()
                    # ------------------------------------------------

                except:
                    messages.error("The asset didn't assigned")
            response = HttpResponseRedirect("../product/usedassets/")
            print(request.COOKIES.get('valueincookie'))
            response.delete_cookie('valueincookie')
            print(request.COOKIES.get('valueincookie'))
            return response
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def loginUser(request):
    if not request.session.has_key("user"):
        if request.method == "POST":
            username = request.POST.get("username")
            valpassword = request.POST.get("password")
            valRemember = request.POST.get("rememberMe")

            # if user submit empty old password then the program will raise validation error
            if not username:
                data = {"error": "please enter your your email"}
                return JsonResponse(data)

            # if user submit empty new password then the program will raise validation error
            if not valpassword:
                data = {"error": "please enter your password"}
                return JsonResponse(data)

            # if user submit empty new password then the program will raise validation error
            try:
                verifyUser = User.objects.get(
                    username=username, password=valpassword, status='true')
            except:
                data = {"error": "user doesnt exists"}
                return JsonResponse(data)

            # session created
            request.session["user"] = verifyUser.username
            request.session["access"] = verifyUser.access
            request.session["fullname"] = verifyUser.fullname
            data = {"success": ""}
            return JsonResponse(data)
        else:
            return HttpResponseRedirect("../")
    else:
        return HttpResponseRedirect("../home")

# ------------------ function for logout --------------------------


def user_logout(request):
    if request.session.has_key("user"):
        del request.session["user"]
        del request.session["access"]
        del request.session["fullname"]

    logout(request)
    response = HttpResponseRedirect("../")
    response.delete_cookie('valueincookie')
    return response
# -----------------------------------------------------------------

# ------------------------ select user type ------------------------


@csrf_exempt
def selectusertype(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            return render(request, "adduserinitial.html")
        else:
            value = request.POST.get('user-staff')
            if value == 'staff':
                return render(request, "createstaff.html")
            else:
                return render(request, "createuser.html")
    else:
        return HttpResponseRedirect("../")
# -----------------------------------------------------------------

# ----------------- user/admin add -------------------------------------


@csrf_exempt
def userregister(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            username = request.POST.get("username")
            is_user_exists = User.objects.filter(username=username)
            if not is_user_exists:

                full_name = request.POST.get("fullname")
                if not full_name:
                    messages.error(
                        request, 'please provide fullname of the user')
                    return HttpResponseRedirect("/adduser/")

                user_name = request.POST.get("username")
                if not user_name:
                    messages.error(
                        request, 'please provide the username for the user')
                    return HttpResponseRedirect("/adduser/")

                password = request.POST.get("password")
                if not password:
                    messages.error(request, 'please provide the password')
                    return HttpResponseRedirect("/adduser/")

                if not validate_password(password):
                    messages.error(
                        request, 'password didnt matched the listed criteria')
                    return HttpResponseRedirect("/adduser/")

                repassword = request.POST.get("repassword")
                if not repassword:
                    messages.error(request, 'please provide the re-password')
                    return HttpResponseRedirect("/adduser/")
                if not validate_password(repassword):
                    messages.error(
                        request, 're-password didnt matched the listed criteria')
                    return HttpResponseRedirect("/adduser/")
                if repassword != password:
                    messages.error(
                        request, 'password and re-typed password didnt matched')
                    return HttpResponseRedirect("/adduser/")

                current_position = request.POST.get("currentposition")
                if not current_position:
                    messages.error(
                        request, 'please provide current position of the user')
                    return HttpResponseRedirect("/adduser/")

                access = request.POST.get("access")
                if not access:
                    messages.error(
                        request, 'please provide access for the user')
                    return HttpResponseRedirect("/adduser/")

                verifyUser = User.objects.filter(
                    username=username, password=password)
                verifyUser2 = User.objects.filter(
                    username=username)
                if verifyUser or verifyUser2:
                    messages.error(
                        request, 'account with this username already exists')
                    return HttpResponseRedirect("/adduser/")

                try:
                    useradded = User()
                    useradded.fullname = full_name
                    useradded.username = user_name
                    useradded.access = access
                    useradded.password = password
                    useradded.current_position = current_position
                    useradded.save()
                    messages.success(request, 'user added sucessfully')
                except:
                    messages.error(request, 'user failed to add sucessfully')

                return HttpResponseRedirect("/adduser/")
            else:
                messages.error(request, 'user already exists')
                return HttpResponseRedirect("/adduser/")
        else:
            return render(request, "createuser.html")
    else:
        return HttpResponseRedirect("../")
# ----------------------------- user add end -----------------------------------

# ----------------staff add ----------------------------------------------------


@csrf_exempt
def staffregister(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            print("here")
            fullname = request.POST.get("fullname")
            is_user_exists = User.objects.filter(fullname=fullname)
            if not is_user_exists:
                full_name = request.POST.get("fullname")
                if not full_name:
                    messages.error(
                        request, 'please provide fullname of the staff')
                    return HttpResponseRedirect("/addstaff/")

                current_position = request.POST.get("currentposition")
                if not current_position:
                    messages.error(
                        request, 'please provide current position of the staff')
                    return HttpResponseRedirect("/addstaff/")

                access = request.POST.get("access")
                print(access, "access")
                username = f'{full_name[:3]}{random.randint(1,999999)}'
                if not access:
                    messages.error(
                        request, 'please provide access for the staff')
                    return HttpResponseRedirect("/addstaff/")

                try:
                    useradded = User()
                    useradded.fullname = full_name
                    useradded.access = access
                    useradded.current_position = current_position
                    useradded.username = username
                    useradded.save()
                    messages.success(request, 'staff added sucessfully')
                except:
                    messages.error(request, 'staff failed to add sucessfully')

                return HttpResponseRedirect("/addstaff/")
            else:
                messages.error(request, 'user already exists')
                return HttpResponseRedirect("/addstaff/")
        else:
            return render(request, "createstaff.html")
    else:
        return HttpResponseRedirect("../")
# --------------------------------------------------------------------------------


@csrf_exempt
def readuser(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            id = request.POST.get("id")
            user = User.objects.get(
                id=id)
            if user.access == 'staff':
                context = {
                    'user': user,
                }
                return render(request, "editstaff.html", context)
            else:
                context = {
                    'user': user,
                }
                return render(request, "edituser.html", context)
        else:
            try:
                user = User.objects.filter(status="true")
                paginator = Paginator(user, 8)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
            except:
                user = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "readuser.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def deleteduser(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            try:
                user = User.objects.filter(status="false")
                paginator = Paginator(user, 8)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
            except:
                user = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "deletedusers.html", context)
        else:
            if (request.POST.get("id")):
                id = request.POST.get("id")
                fullname = request.POST.get("fullname")
                User.objects.filter(
                    id=id).delete()
                messages.success(request, fullname+' deleted permanently')
                return HttpResponseRedirect('/deleteduser/')
            elif (request.POST.get("id-restore")):
                id = request.POST.get("id-restore")
                fullname = request.POST.get("fullname")
                user = User.objects.get(
                    id=id)
                user.status = 'true'
                user.save()
                messages.success(request, fullname+' restored')
                return HttpResponseRedirect('/deleteduser/')
            else:
                return HttpResponseRedirect('/deleteduser/')
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def showupdateuser(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            id = request.GET.get('id')
            user = User.objects.get(
                id=id)
            context = {
                'user': user,
            }
            return render(request, "edituser.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def updateuser(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            user_name = request.POST.get("username")
            id = request.POST.get("id")

            base_url = reverse('showupdateuser')  # 1 /products/
            query_string = urlencode(
                {'username': user_name, 'id': id})  # 2 category=42
            # 3 /products/?category=42
            url = '{}?{}'.format(base_url, query_string)
            # return redirect(url)  # 4

            full_name = request.POST.get("fullname")
            if not full_name:
                messages.error(request, 'please provide fullname of the user')
                return redirect(url)

            if not user_name:
                messages.error(
                    request, 'please provide the username for the user')
                return redirect(url)

            password = request.POST.get("password")
            if not password:
                messages.error(request, 'please provide the password')
                return redirect(url)

            if not validate_password(password):
                messages.error(
                    request, 'password didnt matched the listed criteria')
                return redirect(url)

            repassword = request.POST.get("repassword")
            if not repassword:
                messages.error(request, 'please provide the re-password')
                return redirect(url)
            if not validate_password(repassword):
                messages.error(
                    request, 're-password didnt matched the listed criteria')
                return redirect(url)
            if repassword != password:
                messages.error(
                    request, 'password and re-typed password didnt matched')
                return redirect(url)

            current_position = request.POST.get("currentposition")
            if not current_position:
                messages.error(
                    request, 'please provide current position of the user')
                return redirect(url)

            access = request.POST.get("access")
            if not access:
                messages.error(request, 'please provide access for the user')
                return redirect(url)

            # -------------- user verification --------------------
            print(user_name)
            verifyUser = User.objects.filter(
                username=user_name)
            # print('filteredid', verifyUser.first().id)
            print("getid", id)
            if verifyUser.first() != None:
                if verifyUser.first().id != int(id):
                    messages.error(
                        request, 'this credentials already exists, please choose different username and password')
                    return redirect(url)
            # ----------------------------------------------------

            user = User.objects.get(id=id)
            user.username = user_name
            user.access = access
            user.fullname = full_name
            user.current_position = current_position
            user.password = password
            user.save(update_fields=[
                'username', 'access', 'fullname', 'current_position', 'password'])

            if user.username == request.session["user"]:
                del request.session["user"]
                del request.session["access"]
                del request.session["fullname"]
                logout(request)
                return HttpResponseRedirect("../")

            messages.success(request, full_name+' updated sucessfully')
            return HttpResponseRedirect('/readuser/')
    else:
        return HttpResponseRedirect("../")

# ---------------------- update staff starts -------------------------------------


@csrf_exempt
def updatestaff(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            full_name = request.POST.get("fullname")
            id = request.POST.get("id")

            base_url = reverse('showupdateuser')  # 1 /products/
            query_string = urlencode({'username': full_name})  # 2 category=42
            # 3 /products/?category=42
            url = '{}?{}'.format(base_url, query_string)

            if not full_name:
                messages.error(request, 'please provide fullname of the user')
                return redirect(url)

            current_position = request.POST.get("currentposition")
            if not current_position:
                messages.error(
                    request, 'please provide current position of the user')
                return redirect(url)

            access = request.POST.get("access")
            if not access:
                messages.error(request, 'please provide access for the user')
                return redirect(url)

            user = User.objects.get(id=id)
            user.access = access
            user.fullname = full_name
            user.current_position = current_position
            user.save(update_fields=[
                'access', 'fullname', 'current_position'])

            messages.success(request, full_name+' updated sucessfully')
            return HttpResponseRedirect('/readuser/')
    else:
        return HttpResponseRedirect("../")
# --------------- update staff end -------------------------------------

# ------------------ remove user ---------------------------------------


@csrf_exempt
def removeuser(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            id = request.POST.get("id")
            fullname = request.POST.get("fullname")
            user = User.objects.get(id=id)
            is_asset_assigned = Product.objects.filter(
                user__id=id)

            if (is_asset_assigned):
                messages.error(request, fullname +
                               ' is assigned to '+is_asset_assigned.first().name_of_asset+', we cannot perform delete operation')
                return HttpResponseRedirect('/readuser/')
            else:
                user.status = 'false'
                user.save(update_fields=['status'])
                if user.username == request.session["user"]:
                    del request.session["user"]
                    del request.session["access"]
                    del request.session["fullname"]
                    logout(request)
                    return HttpResponseRedirect("../")
                messages.success(request, fullname +
                                 ' removed sucessfully')
                return HttpResponseRedirect('/readuser/')
    else:
        return HttpResponseRedirect("../")
# ------------- remove user end -----------------------------------------

# ------------------ vendor add starts ---------------------------------


@csrf_exempt
def vendoradd(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            name_of_vendor = request.POST.get("nameofvendor")
            address = request.POST.get("address")
            contact_person = request.POST.get("contactperson")
            contact_no = request.POST.get("contactno")
            pan_no = request.POST.get("panno")

            vendor = Vendor()
            # vendor.vendor_no = 'initial'
            vendor.name_of_vendor = name_of_vendor
            vendor.address = address
            vendor.contact_person = contact_person
            vendor.contact_no = contact_no
            vendor.pan_no = pan_no
            vendor.save()

            messages.success(request, vendor.name_of_vendor +
                             ' added sucessfully')
            return HttpResponseRedirect('/addvendor/')
        else:

            return render(request, "create-vendor.html")
    else:
        return HttpResponseRedirect("../")
# -------------- vendor add ends -------------------------------

# ----------------- read vendor starts ------------------


@csrf_exempt
def readvendor(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            vendor_no = request.POST.get("vendor_no")
            vendor = Vendor.objects.get(
                vendor_no=vendor_no)
            context = {
                'vendor': vendor,
            }
            return render(request, "editvendor.html", context)
        else:
            try:
                vendor = Vendor.objects.filter(status="true")
                paginator = Paginator(vendor, 8)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
            except:
                vendor = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "readvendor.html", context)
    else:
        return HttpResponseRedirect("../")
# ------------ read vendor ends -------------------------------


@csrf_exempt
def updatevendor(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            vendor_no = request.POST.get("vendor_no")
            name_of_vendor = request.POST.get("name_of_vendor")
            address = request.POST.get("address")
            contact_person = request.POST.get("contact_person")
            contact_no = request.POST.get("contact_no")
            pan_no = request.POST.get("pan_no")

            vendor = Vendor.objects.get(vendor_no=vendor_no)
            # vendor.vendor_no = 'initial'
            vendor.name_of_vendor = name_of_vendor
            vendor.address = address
            vendor.contact_person = contact_person
            vendor.contact_no = contact_no
            vendor.pan_no = pan_no
            vendor.save(update_fields=[
                        'name_of_vendor', 'address', 'contact_person', 'contact_no', 'pan_no'])

            messages.success(request, name_of_vendor+' updated sucessfully')
            return HttpResponseRedirect('/readvendor/')
        else:
            return render(request, "create-vendor.html")
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def deletevendor(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            vendor_no = request.POST.get("vendor_no")
            vendor = Vendor.objects.get(vendor_no=vendor_no)
            is_asset_assigned = Product.objects.filter(
                vendor__vendor_no=vendor_no)

            if (is_asset_assigned):
                messages.error(request, vendor.name_of_vendor +
                               ' is assigned to '+is_asset_assigned.first().name_of_asset+', we cannot perform delete operation')
                return HttpResponseRedirect('/readvendor/')
            else:
                vendor.status = 'false'
                vendor.save(update_fields=['status'])

            messages.success(request, vendor.name_of_vendor +
                             ' deleted sucessfully')
            return HttpResponseRedirect('/readvendor/')
        else:
            return render(request, "create-vendor.html")


@csrf_exempt
def deletedvendor(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            try:
                vendor = Vendor.objects.filter(status="false")
                paginator = Paginator(vendor, 8)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
            except:
                vendor = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "deletedvendors.html", context)
        else:
            if (request.POST.get("code")):
                vendor_no = request.POST.get("code")
                Vendor.objects.filter(
                    vendor_no=vendor_no).delete()
                messages.success(request, vendor_no+' deleted permanently')
                return HttpResponseRedirect('/deletedvendor/')
            elif (request.POST.get("code-restore")):
                vendor_no = request.POST.get("code-restore")
                vendor = Vendor.objects.get(
                    vendor_no=vendor_no)
                vendor.status = 'true'
                vendor.save()
                messages.success(request, vendor_no+' restored')
                return HttpResponseRedirect('/deletedvendor/')
            else:
                return HttpResponseRedirect('/deletedvendor/')
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def AssignUser(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            nameofstaff = request.POST.get("nameofstaff")
            purpose = request.POST.get("purpose")
            date_of_issue = request.POST.get("date_of_issue")
            estimated_date_of_return = request.POST.get(
                "estimated_date_of_return")
            asset_info = request.POST.get("asset_info")
            asset_verified_by = request.POST.get("asset_verified_by")
            position_of_verified_authority = request.POST.get(
                "position_of_verified_authority")

            assetassign = AssestAssign()
            assetassign.nameofstaff = nameofstaff
            assetassign.purpose = purpose
            assetassign.date_of_issue = date_of_issue
            assetassign.estimated_date_of_return = estimated_date_of_return
            assetassign.asset_info = asset_info
            assetassign.asset_verified_by = asset_verified_by
            assetassign.position_of_verified_authority = position_of_verified_authority
            assetassign.save()

            data = {"success": "assetassigned",
                    }
            return JsonResponse(data)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def releaseasset(request, token):
    if request.session.has_key("user"):
        if request.method == "GET":
            token = request.GET.get("token")
            assigned_value = AssestAssign.objects.filter(token=token)
            assigned_date = assigned_value.first().date_of_issue
            asigned_by = assigned_value.first().asset_verified_by.fullname
            purpose = assigned_value.first().purpose
            assigned_to = assigned_value.first().nameofstaff
            expected_date_of_return = assigned_value.first().estimated_date_of_return

            context = {
                "assigned": assigned_value,
                "assigned_date": assigned_date,
                "asigned_by": asigned_by,
                "purpose": purpose,
                "assigned_to": assigned_to,
                "expected_date_of_return": expected_date_of_return,
            }

            return render(request, "release-asset.html", context)

    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def releaseassetone(request):
    if request.session.has_key("user"):
        if request.method == "POST":

            checkreleaseassets = request.POST.get("dictval")
            token = request.POST.get("token")
            date_of_return = datetime.strptime(
                request.POST.get("dateofreturn"), '%Y-%m-%d')
            striped_token = token.strip()
            print(striped_token)
            asset_released_by = User.objects.get(
                username=request.session['user'], status='true')

            print(json.loads(checkreleaseassets))
            assets_to_be_released = json.loads(checkreleaseassets)
            token_for_release_asset = f'{asset_released_by.fullname[:3]}{random.randint(1,9999999)}'
            try:
                for key, value in assets_to_be_released.items():
                    print(key)
                    print(value)

                    asset = Product.objects.get(asset_code=key)
                    remove_asset = AssestAssign.objects.filter(
                        asset_info__pk=asset.pk).filter(token=striped_token)

                    print(remove_asset)
                    # --- release info ------------------------------------------------
                    nameofstaffreturningasset = remove_asset.first().nameofstaff
                    asset_verified_by = remove_asset.first().asset_verified_by
                    asset_issued_in = remove_asset.first().date_of_issue
                    expected_date_of_return_of_such_asset = remove_asset.first().estimated_date_of_return
                    # -------------------

                    # release asset info------------------------------------------------
                    user = User.objects.get(
                        fullname=remove_asset.first().nameofstaff, status='true')

                    asset.user.remove(user)
                    if value == 'Sold':
                        asset.availale_status = 'false'
                        asset.status = 'false'
                    else:
                        asset.availale_status = 'true'
                    asset.condition_of_asset = value
                    asset.save()
                    print(asset.user)
                    # -------------------------------------------------------------------

                    # removing assigned asset from AssignAsset --------------------------
                    AssestAssign.objects.filter(
                        asset_info__pk=asset.pk).filter(token=striped_token).delete()
                    # ------------------------------------------------------------------

                    # asset returned object will be added ------------------------------
                    returnasset = AssestReturn()
                    returnasset.nameofstaffreturningasset = nameofstaffreturningasset
                    returnasset.asset_verified_by = asset_verified_by.fullname
                    returnasset.asset_release_by = asset_released_by.fullname
                    returnasset.asset_issued_in = asset_issued_in
                    returnasset.expected_date_of_return_of_such_asset = expected_date_of_return_of_such_asset
                    returnasset.date_of_return = date_of_return
                    returnasset.asset_code = asset.asset_code
                    returnasset.asset_name = asset.name_of_asset
                    returnasset.token = token_for_release_asset
                    returnasset.save()
                    # -----------------------------------------------------------------------
            except:
                data = {"error": "assets not released successfully"}
                return JsonResponse(data)

            data = {"success": "assets released successfully"}
            return JsonResponse(data)

    else:
        return HttpResponseRedirect("../")
