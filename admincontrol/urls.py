from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginpage, name="loginpage"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("home/", views.home, name="home"),

    # -----------------------------------------------------------------
    path("selectusertype/", views.selectusertype, name="selectusertype"),
    path("adduser/", views.userregister, name="adduser"),
    path("addstaff/", views.staffregister, name="addstaff"),
    path("readuser/", views.readuser, name="readuser"),
    path("updateuser/", views.updateuser, name="updateuser"),
    path("updatestaff/", views.updatestaff, name="updatestaff"),
    path("removeuser/", views.removeuser, name="removeuser"),
    # ------------------------------------------------------------------

    # -------------- if you want to delete the user permanenlty
    path("deleteduser/", views.deleteduser, name="deleteduser"),
    # ---------------------------------------------------------

    path("addvendor/", views.vendoradd, name="addvendor"),
    path("readvendor/", views.readvendor,
         name="readvendor"),
    path("updatevendor/", views.updatevendor,
         name="updatevendor"),
    path("deletevendor/", views.deletevendor,
         name="deletevendor"),
    path("deletedvendor/", views.deletedvendor, name="deletedvendor"),

    path("search/", views.search, name="search"),
    path("assignasset/<str:values>", views.assignasset, name="assignasset"),
    path("assignassettemplate/", views.assignassettemplate,
         name="assignassettemplate"),
    path("addassignasset/", views.addassignasset,
         name="addassignasset"),


    path("showupdateuser/", views.showupdateuser,
         name="showupdateuser"),

    # release related
    path("releaseasset/<str:token>", views.releaseasset, name="releaseasset"),
    path("releaseassetone/", views.releaseassetone, name="releaseassetone"),
]
