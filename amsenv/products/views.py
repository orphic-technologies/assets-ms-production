from django.shortcuts import render
from .models import Product, AssestAssign, AssestReturn, Location
from django.http import HttpResponseRedirect
from django.contrib import messages
from admincontrol.models import User as users
from products.models import Vendor, Specifications, Image, AssetPool
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import ImageForm
from django.db.models import Q
from django import template
from datetime import datetime
from admincontrol.utils import render_to_pdf
from django.http import HttpResponse
import csv


register = template.Library()
# Create your views here.


@csrf_exempt
def productadd(request):
    imageform = ImageForm()
    if request.session.has_key("user"):
        if request.method == "POST":
            files = request.FILES.getlist('images')
            name_of_asset = request.POST.get("name")
            supporting_gear = request.POST.get("gears")
            quantity = request.POST.get("quantity")
            rate_per_unit = request.POST.get("rate")
            condition_of_asset = request.POST.get("condition")
            assets_pool = request.POST.get("pool")
            asset_location = request.POST.get("location")
            purpose_of_asset = request.POST.get("purpose")
            date_of_update = request.POST.get("dateofupdate")
            date_of_purchase = request.POST.get("dateofp")
            product_category = request.POST.get("categoryvalue")
            vendor = request.POST.get("vendor")
            user = request.POST.get("currentpossesion")
            vendor_to_be_added = Vendor.objects.get(vendor_no=vendor)

            if user != "":
                user_to_be_added = users.objects.get(username=user)
            else:
                user_to_be_added = None

            brand = request.POST.get("brand")
            model = request.POST.get("model")
            manufacture = request.POST.get("manufacture")
            color = request.POST.get("color")
            size = request.POST.get("size")
            warranty = request.POST.get("warranty")
            additionalspecs = request.POST.get("additionalspecs")

            # if brand or model or manufacture or color or size or warranty or additionalspecs != "":
            specification = Specifications(
                brand=brand,
                Model_no=model,
                year_of_manufacture=manufacture,
                color=color,
                size=size,
                warranty_period=warranty,
                other_specs=additionalspecs,
            )
            specification.save()
            # else:
            #     specification = None
            product = Product(
                name_of_asset=name_of_asset,
                supporting_gear=supporting_gear,
                quantity=quantity,
                rate_per_unit=rate_per_unit,
                condition_of_asset=condition_of_asset,
                assets_pool=assets_pool,
                asset_location=asset_location,
                purpose_of_asset=purpose_of_asset,
                date_of_update=date_of_update,
                product_category=product_category,
                vendor=vendor_to_be_added,
                date_of_purchase=date_of_purchase,
                specifications=specification,
            )
            product.save()
            product.user.add(user_to_be_added)
            product.save()
            for file in files:
                Image.objects.create(product=product, images=file)
            messages.success(request, product.name_of_asset +
                             ' added sucessfully')
            return HttpResponseRedirect('/product/addproduct/')
        else:

            alluser = users.objects.all()
            allvendor = Vendor.objects.all()
            assetpool = AssetPool.choices
            locations = Location.objects.all()

            context = {

                "totalusers": alluser,
                "totalvendors": allvendor,
                "i_form": imageform,
                "assetpool": assetpool,
                "locations": locations,
            }
            return render(request, "record-assets.html", context)
    else:
        return HttpResponseRedirect("../../login/")


@csrf_exempt
def locationadd(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            location_name = request.POST.get("locationname")

            location = Location(
                location_name=location_name,
            )
            location.save()
            messages.success(request, location.location_name +
                             ' added sucessfully')
            return HttpResponseRedirect('/product/locationadd/')
        else:
            return render(request, "location.html")
    else:
        return HttpResponseRedirect("../../login/")


@csrf_exempt
def locationread(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            if request.POST.get("location_id"):
                location_id = request.POST.get("location_id")
                location = Location.objects.get(
                    id=location_id)
                context = {
                    "locations": location,
                }
                return render(request, "locationedit.html", context)
        else:
            try:
                locations = Location.objects.filter(status='true')
                paginator = Paginator(locations, 5)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

            except:
                assets = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "locationread.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def locationupdate(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            location_id = request.POST.get("location_id")
            name_of_location = request.POST.get("name_of_location")

            location = Location.objects.get(id=location_id)
            # vendor.vendor_no = 'initial'
            location.location_name = name_of_location
            location.save(update_fields=[
                'location_name'])

            messages.success(request, name_of_location+' updated sucessfully')
            return HttpResponseRedirect('../../product/locationread/')
        else:
            return render(request, "location.html")
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def locationdelete(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            try:
                locations = Location.objects.filter(status='false')
                paginator = Paginator(locations, 5)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

            except:
                locations = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "locationdelete.html", context)
        else:
            # for putting the location to the trash ------------
            if (request.POST.get("temporary_delete_location_id")):
                try:
                    location_id = request.POST.get(
                        "temporary_delete_location_id")

                    location = Location.objects.get(
                        id=location_id)
                    location.status = 'false'

                    location.save(update_fields=['status'])

                    messages.success(request, location.location_name +
                                     ' is added to the trash')
                except:
                    assets = None
                return HttpResponseRedirect('../../product/locationread/')
            # ---------------------------------------------------------

            elif (request.POST.get("code")):
                locationid = request.POST.get("locationid")
                locaionname = request.POST.get("code")
                Location.objects.filter(
                    id=locationid).delete()
                messages.success(request, locaionname+' deleted permanently')
                return HttpResponseRedirect('../../product/locationdelete/')

            # -- for restore -------------
            elif (request.POST.get("code-restore")):
                print('here at restore')
                locaionname = request.POST.get("code-restore")
                locationid = request.POST.get("locationid")
                location = Location.objects.get(
                    id=locationid)
                location.status = 'true'
                location.save()
                messages.success(request, locaionname+' is restored')
                return HttpResponseRedirect('../../product/locationdelete/')
            else:
                return HttpResponseRedirect('../../product/locationdelete/')
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def readasset(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            if request.POST.get("asset_code"):
                imageform = ImageForm()
                asset_code = request.POST.get("asset_code")
                asset = Product.objects.get(
                    asset_code=asset_code)
                totalusers = users.objects.all()
                totalvendors = Vendor.objects.all()
                locations = Location.objects.all()
                assetpool = AssetPool.choices
                context = {
                    'asset': asset,
                    'totalusers': totalusers,
                    'totalvendors': totalvendors,
                    "i_form": imageform,
                    "assetpool": assetpool,
                    "locations": locations,

                }
                return render(request, "edit-asset.html", context)
            else:
                # for goback button
                try:
                    assets = Product.objects.all()
                    paginator = Paginator(assets, 5)
                    page_number = request.GET.get("page")
                    page_obj = paginator.get_page(page_number)

                except:
                    assets = None
                context = {
                    "page_obj": page_obj,
                }
                return render(request, "readasset.html", context)

        else:
            # when you search
            try:
                query = request.GET.get("query", "")
                assets = Product.objects.filter(
                    Q(name_of_asset__icontains=query) | Q(asset_code=query)).filter(status='true')
                paginator = Paginator(assets, 5)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

            except:
                assets = None
            context = {
                "page_obj": page_obj,
                "queryvalue": query,
            }
            return render(request, "readasset.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def deletedassets(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            try:
                query = request.GET.get("query", "")
                assets = Product.objects.filter(
                    Q(name_of_asset__icontains=query) | Q(asset_code=query)).filter(status='false')
                paginator = Paginator(assets, 5)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

            except:
                assets = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "deletedassets.html", context)
        else:
            if (request.POST.get("all")):
                try:
                    query = request.GET.get("query", "")
                    assets = Product.objects.filter(
                        Q(name_of_asset__icontains=query) | Q(asset_code=query)).filter(status='false')
                    paginator = Paginator(assets, 5)
                    page_number = request.GET.get("page")
                    page_obj = paginator.get_page(page_number)

                except:
                    assets = None
                context = {
                    "page_obj": page_obj,
                }
                return render(request, "deletedassets.html", context)
            elif (request.POST.get("code")):
                asset_code = request.POST.get("code")
                Product.objects.filter(
                    asset_code=asset_code).delete()
                messages.success(request, asset_code+' deleted permanently')
                return HttpResponseRedirect('/product/deletedassets/')

            # -- for restore -------------
            elif (request.POST.get("code-restore")):
                asset_code = request.POST.get("code-restore")
                asset = Product.objects.get(
                    asset_code=asset_code)
                asset.status = 'true'
                asset.availale_status = 'true'
                asset.save()
                messages.success(request, asset_code+' is restored')
                return HttpResponseRedirect('/product/deletedassets/')
            else:
                return HttpResponseRedirect('/product/deletedassets/')
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def updateasset(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            files = request.FILES.getlist('images')
            spec_model_no = request.POST.get("hidden_model_no")
            id = request.POST.get('id')
            if spec_model_no != "":
                specs = Specifications.objects.get(id=int(id))
                specs.brand = request.POST.get("brand")
                specs.Model_no = request.POST.get("model")
                specs.year_of_manufacture = request.POST.get("manufacture")
                specs.color = request.POST.get("color")
                specs.size = request.POST.get("size")
                specs.warranty_period = request.POST.get("warranty")
                specs.other_specs = request.POST.get("additionalspecs")

                specs.save(update_fields=[
                    'brand', 'Model_no', 'year_of_manufacture', 'color', 'size', 'warranty_period', 'other_specs'])

                asset_code = request.POST.get("asset_code")
                vendor = request.POST.get("vendor")
                print(vendor)
                asset = Product.objects.get(asset_code=asset_code)

                asset.name_of_asset = request.POST.get("name")
                asset.supporting_gear = request.POST.get("gears")
                asset.quantity = request.POST.get("quantity")
                asset.rate_per_unit = request.POST.get("rate")
                asset.condition_of_asset = request.POST.get("condition")
                asset.assets_pool = request.POST.get("pool")
                asset.date_of_purchase = request.POST.get("dateofp")
                asset.date_of_update = request.POST.get("dateofupdate")
                asset.asset_location = request.POST.get("location")
                asset.purpose_of_asset = request.POST.get("purpose")
                asset.product_category = request.POST.get("categoryvalue")
                asset.vendor = Vendor.objects.get(vendor_no=vendor)

                asset.save(update_fields=[
                    'name_of_asset', 'supporting_gear', 'quantity', 'rate_per_unit', 'condition_of_asset',
                    'assets_pool', 'asset_location', 'purpose_of_asset', 'date_of_purchase', 'date_of_update', 'product_category', 'vendor'])
            else:
                print('here')
                specs = Specifications()
                specs.brand = request.POST.get("brand")
                specs.Model_no = request.POST.get("model")
                specs.year_of_manufacture = request.POST.get("manufacture")
                specs.color = request.POST.get("color")
                specs.size = request.POST.get("size")
                specs.warranty_period = request.POST.get("warranty")
                specs.other_specs = request.POST.get("additionalspecs")
                specs.save()

                asset_code = request.POST.get("asset_code")
                vendor = request.POST.get("vendor")
                print(vendor)
                asset = Product.objects.get(asset_code=asset_code)

                asset.name_of_asset = request.POST.get("name")
                asset.supporting_gear = request.POST.get("gears")
                asset.quantity = request.POST.get("quantity")
                asset.rate_per_unit = request.POST.get("rate")
                asset.condition_of_asset = request.POST.get("condition")
                asset.assets_pool = request.POST.get("pool")
                asset.date_of_purchase = request.POST.get("dateofp")
                asset.date_of_update = request.POST.get("dateofupdate")
                asset.asset_location = request.POST.get("location")
                asset.purpose_of_asset = request.POST.get("purpose")
                asset.product_category = request.POST.get("categoryvalue")
                asset.vendor = Vendor.objects.get(vendor_no=vendor)
                asset.specifications = specs

                asset.save(update_fields=[
                    'name_of_asset', 'supporting_gear', 'quantity', 'rate_per_unit', 'condition_of_asset',
                    'assets_pool', 'asset_location', 'purpose_of_asset', 'date_of_purchase', 'date_of_update',
                    'product_category', 'vendor', 'specifications'])
            for file in files:
                Image.objects.create(product=asset, images=file)
            messages.success(request, asset.asset_code +
                             ' updated sucessfully')
            return HttpResponseRedirect('/product/readasset/')
        else:
            return render(request, "readasset.html")


@csrf_exempt
def usedassets(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            query = request.GET.get("query", "")

            token_list = AssestAssign.objects.filter(Q(asset_info__name_of_asset__icontains=query) |
                                                     Q(asset_info__asset_code__icontains=query) | Q(nameofstaff__icontains=query) |
                                                     Q(asset_verified_by__fullname__icontains=query)).values_list(
                'token',  flat=True
            ).distinct()
            group_by_token = {}
            for token in token_list:
                group_by_token[token] = AssestAssign.objects.filter(
                    token=token)

            grouped_acc_to_token = tuple(group_by_token.items())

            paginator = Paginator(grouped_acc_to_token, 8)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {
                "page_obj": page_obj,
            }

            return render(request, "used-assets.html", context)

        else:
            token_list = AssestAssign.objects.values_list(
                'token',  flat=True
            ).distinct()
            group_by_token = {}
            for token in token_list:
                group_by_token[token] = AssestAssign.objects.filter(
                    token=token)

            grouped_acc_to_token = tuple(group_by_token.items())

            paginator = Paginator(grouped_acc_to_token, 8)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {
                "page_obj": page_obj,
            }

            return render(request, "used-assets.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def archives(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            query = request.GET.get("query", "")

            token_list = AssestReturn.objects.filter(Q(asset_name__icontains=query) |
                                                     Q(asset_code__icontains=query) | Q(nameofstaffreturningasset__icontains=query) |
                                                     Q(asset_verified_by__icontains=query)).values_list(
                'token',  flat=True
            ).distinct()
            group_by_token = {}
            for token in token_list:
                group_by_token[token] = AssestReturn.objects.filter(
                    token=token)

            grouped_acc_to_token = tuple(group_by_token.items())[::-1]

            paginator = Paginator(grouped_acc_to_token, 8)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {
                "page_obj": page_obj,
                "queryvalue": query,
            }

            return render(request, "archives.html", context)

        else:
            token_list = AssestReturn.objects.values_list(
                'token',  flat=True
            ).distinct()
            group_by_token = {}
            for token in token_list:
                group_by_token[token] = AssestReturn.objects.filter(
                    token=token)

            grouped_acc_to_token = tuple(group_by_token.items())

            paginator = Paginator(grouped_acc_to_token, 8)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {
                "page_obj": page_obj,
            }

            return render(request, "archives.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
@register.simple_tag(takes_context=True)
def availableassets(request):
    if request.session.has_key("user"):
        if request.method == "GET":
            query = request.GET.get("query", "")

            availableassets = Product.objects.filter(availale_status='true').filter(
                Q(name_of_asset__icontains=query) | Q(asset_code=query))

            paginator = Paginator(availableassets, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context = {
                "page_obj": page_obj,
            }
            return render(request, "available-assets.html", context)
        else:
            availableassets = Product.objects.filter(availale_status='true')
            paginator = Paginator(availableassets, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context = {
                "page_obj": page_obj,
            }
            return render(request, "available-assets.html", context)

    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def repairmantain(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            if request.POST.get("asset_code"):

                datenow = datetime.today().strftime('%Y-%m-%d')
                asset_code = request.POST.get("asset_code")
                asset = Product.objects.get(asset_code=asset_code)
                asset.condition_of_asset = 'Good'
                asset.date_of_update = datenow
                asset.updated_by = request.session['user']

                asset.save(update_fields=[
                    'condition_of_asset',
                    'date_of_update', 'updated_by'])
                messages.success(request,
                                 'condition of '+asset.asset_code + " is updated as good")
                return HttpResponseRedirect('../../product/repairmantain/')
            else:
                try:
                    assets = Product.objects.filter(
                        condition_of_asset='Requires Repair').filter(status='true')
                    paginator = Paginator(assets, 5)
                    page_number = request.GET.get("page")
                    page_obj = paginator.get_page(page_number)

                except:
                    assets = None
                context = {
                    "page_obj": page_obj,
                }
                return render(request, "repairmantain.html", context)

        else:
            try:
                query = request.GET.get("query", "")
                assets = Product.objects.filter(
                    Q(name_of_asset__icontains=query) | Q(asset_code=query)).filter(status='true', condition_of_asset='Requires Repair')
                paginator = Paginator(assets, 5)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

            except:
                assets = None
            context = {
                "page_obj": page_obj,
            }
            return render(request, "repairmantain.html", context)
    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def deleteasset(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            asset_code = request.POST.get("asset_code_c")
            print(asset_code)
            asset = Product.objects.get(asset_code=asset_code)
            try:
                is_asset_assigned = AssestAssign.objects.get(asset_info=asset)
                messages.error(request, asset.asset_code +
                               ' is assigned, we cannot perform delete operation')
                return HttpResponseRedirect('../../product/readasset/')
            except:
                asset.availale_status = 'false'
                asset.status = 'false'
                asset.save(update_fields=['status', 'availale_status'])

            messages.success(request, asset.asset_code +
                             ' deleted sucessfully')
            return HttpResponseRedirect('../../product/readasset/')
        else:
            return render(request, "create-vendor.html")


@csrf_exempt
def assuremessage(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            if (request.POST.get("fromdeleteasset")):
                assetinfo = request.POST.get("asset_code")

                context = {
                    "assetinfo": assetinfo,
                }
                return render(request, "assuremessage.html", context)
            elif (request.POST.get("fromdeleteuser")):
                id = request.POST.get("id")
                fullname = request.POST.get("fullname")

                context = {
                    "fullname": fullname,
                    "id": id,
                }
                return render(request, "assuremessage.html", context)

            elif (request.POST.get("fromdeletelocation")):
                id = request.POST.get("location_id")
                location = Location.objects.get(id=id)

                context = {
                    "locationname": location.location_name,
                    "locationid": location.id,
                }
                return render(request, "assuremessage.html", context)
            else:
                vendorinfo = request.POST.get("vendor_no")

                context = {
                    "vendorinfo": vendorinfo,
                }
                return render(request, "assuremessage.html", context)
        else:
            return HttpResponseRedirect("../product/")

    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def assuremessagerestore(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            if (request.POST.get("fromdeleteasset")):
                assetinfo = request.POST.get("asset_code")

                context = {
                    "assetinfo": assetinfo,
                    "restore": "restore",
                }
                return render(request, "assuremessage.html", context)
            elif (request.POST.get("fromdeleteuser")):
                id = request.POST.get("id")
                fullname = request.POST.get("fullname")

                context = {
                    "fullname": fullname,
                    "id": id,
                    "restore": "'restore",
                }
                return render(request, "assuremessage.html", context)

            elif (request.POST.get("fromdeletelocation")):
                id = request.POST.get("location_id")
                location = Location.objects.get(id=id)

                context = {
                    "locationname": location.location_name,
                    "locationid": location.id,
                    "restore": "restore",
                }
                return render(request, "assuremessage.html", context)

            else:
                vendorinfo = request.POST.get("vendor_no")

                context = {
                    "vendorinfo": vendorinfo,
                    "restore": "'restore",
                }
                return render(request, "assuremessage.html", context)
        else:
            return HttpResponseRedirect("../product/")

    else:
        return HttpResponseRedirect("../")


@csrf_exempt
def assuremessagerepair(request):
    if request.session.has_key("user"):
        assetinfo = request.POST.get("asset_code")

        context = {
            "assetinfo": assetinfo,
        }
        return render(request, "assure/assuremessagerepair.html", context)

    else:
        return HttpResponseRedirect("../")


# @csrf_exempt
# def generatePDF(request):
#     if request.method == "GET":
#         query = request.GET.get("query", "")
#         print(query)

#         token_list = AssestReturn.objects.filter(Q(asset_name__icontains=query) |
#                                                  Q(asset_code__icontains=query) | Q(nameofstaffreturningasset__icontains=query) |
#                                                  Q(asset_verified_by__icontains=query)).values_list(
#             'token',  flat=True
#         ).distinct()
#         group_by_token = {}
#         for token in token_list:
#             group_by_token[token] = AssestReturn.objects.filter(
#                 token=token)

#         grouped_acc_to_token = tuple(group_by_token.items())[::-1]
#         context = {
#             "page_obj": grouped_acc_to_token,
#         }
#         pdf = render_to_pdf("export/archives.html", context)
#         if pdf:
#             response = HttpResponse(pdf, content_type="application/pdf")
#             filename = "archives.pdf"
#             content = "inline; filename=%s" % (filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" % (filename)
#             response["Content-Disposition"] = content
#             return response

#         return HttpResponseRedirect("archives/")


@csrf_exempt
def generatecsv(request):
    if request.session.has_key("user"):
        # get for archives
        if request.method == "GET":
            query = request.GET.get("query", "")

            datatobeconverted = AssestReturn.objects.filter(Q(asset_name__icontains=query) |
                                                            Q(asset_code__icontains=query) | Q(nameofstaffreturningasset__icontains=query) |
                                                            Q(asset_verified_by__icontains=query))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=archives.csv'
            writer = csv.writer(response)
            writer.writerow(['Assigned to', 'Assigned by', 'Released by',
                            'Asset Code', 'Asset Name', 'Assigned Date', 'Due Date', 'Returned Date'])
            datatobeconverted = datatobeconverted.values_list('nameofstaffreturningasset', 'asset_verified_by', 'asset_release_by',
                                                              'asset_code', 'asset_name', 'asset_issued_in', 'expected_date_of_return_of_such_asset', 'date_of_return')
            for data in datatobeconverted:
                writer.writerow(data)
            return response
        else:
            # get for assets
            query = request.GET.get("query", "")

            datatobeconverted = Product.objects.filter(Q(name_of_asset__icontains=query) |
                                                       Q(asset_code__icontains=query))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=assets.csv'
            writer = csv.writer(response)
            writer.writerow(['Asset Name', 'Supporting Gear',
                            'Rate per unit', 'Condition', 'Pool', 'Category', 'Location', 'Purpose', 'Update Date', 'Vendor',
                             'Purchase Date', 'Brand', 'Model No', 'Manufacture Year', 'Color', 'Size', 'Warranty', 'Others'])
            datatobeconverted = datatobeconverted.values_list('name_of_asset', 'supporting_gear',
                                                              'rate_per_unit', 'condition_of_asset', 'assets_pool',
                                                              'product_category', 'asset_location', 'purpose_of_asset', 'date_of_update', 'vendor__name_of_vendor',
                                                              'date_of_purchase', 'specifications__brand', 'specifications__Model_no', 'specifications__year_of_manufacture',
                                                              'specifications__color', 'specifications__size', 'specifications__warranty_period', 'specifications__other_specs')
            for data in datatobeconverted:
                writer.writerow(data)
            return response
    else:
        return HttpResponseRedirect("../")
