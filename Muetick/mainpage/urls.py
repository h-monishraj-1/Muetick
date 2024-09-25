from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.dashboard, name="dashboard"),
    path("adminpage/",views.adminpage,name="adminpage"),
    path("catpage/<str:mname>",views.catpage,name="catpage"),
    path("dev/",views.dev,name="dev"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("profile/",views.profile,name="profile"),
    path("signin/",views.signin,name="signin"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.logout,name="logout"),
    path("scan/",views.scan,name="scan"),
    path("transactions/",views.transactions,name="transactions"),
    path("lostitems/",views.lostitems,name="lostitems"),
    path("feedback/",views.feedback_page,name="feedback_page"),
    path("quicksetupadmin/",views.quicksetup,name="quicksetup"),
    path("",views.landingpage,name="landingpage"),
]