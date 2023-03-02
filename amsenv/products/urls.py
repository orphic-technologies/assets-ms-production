from django.urls import path
from . import views

urlpatterns = [

    # ------------ crud asset related -------------------
    path("addproduct/", views.productadd, name="addproduct"),
    path("readasset/", views.readasset, name="readasset"),
    path("deletedassets/", views.deletedassets, name="deletedassets"),
    path("updateasset/", views.updateasset, name="updateasset"),
    path("usedassets/", views.usedassets, name="usedassets"),
    path("availableassets/", views.availableassets, name="availableassets"),
    # ----------------------------------------------------------------

    path("archives/", views.archives, name="archives"),


    # --------- to change the status of asset to false ----------------
    path("deleteasset/", views.deleteasset, name="deleteasset"),
    # ----------------------------------------------------------------


    path("repairmantain/", views.repairmantain, name="repairmantain"),

    # --------------- assure message related ----------------------------

    path("assuremessage/", views.assuremessage, name="assuremessage"),
    path("assuremessagerestore/", views.assuremessagerestore,
         name="assuremessagerestore"),
    path("assuremessagerepair/", views.assuremessagerepair,
         name="assuremessagerepair"),
    # --------------------------------------------------------------------


    # ---- export related ------------------------------------------
    path("download_file/", views.generatecsv, name="download_file"),
    # --------------------------------------------------------------

    # --------------- location related ---------------------------
    path("locationadd/", views.locationadd, name="locationadd"),
    path("locationread/", views.locationread, name="locationread"),
    path("locationupdate/", views.locationupdate, name="locationupdate"),
    path("locationdelete/", views.locationdelete, name="locationdelete"),

    # ------------------------------------------------------------
]
