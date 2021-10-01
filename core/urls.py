from core.view import CustomTokenObtainPairView, OrderDelivered
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from core.views.Department_view import DepartmentView
from core.views.DeptUser_view import DeptUserView
from core.views.Document_view import DocumentView
from core.views.Offer_view import OfferView
from core.views.Order_view import OrderView
from core.views.OrderProcess_view import OrderProcessView
from core.views.Organization_view import OrganizationView
from core.views.Pipeline_view import PipelineView
from core.views.PipelineNode_view import PipelineNodeView
from core.views.User_view import UserView

urlpatterns = [

    path('Department/', DepartmentView.as_view()),
    path('Department/<str:pk>', DepartmentView.as_view()),


    path('DeptUser/', DeptUserView.as_view()),
    path('DeptUser/<str:pk>', DeptUserView.as_view()),


    path('Document/', DocumentView.as_view()),
    path('Document/<str:pk>', DocumentView.as_view()),


    path('Offer/', OfferView.as_view()),
    path('Offer/<str:pk>', OfferView.as_view()),


    path('Order/', OrderView.as_view()),
    path('Order/<str:pk>', OrderView.as_view()),


    path('OrderProcess/', OrderProcessView.as_view()),
    path('OrderProcess/<str:pk>', OrderProcessView.as_view()),


    path('Organization/', OrganizationView.as_view()),
    path('Organization/<str:pk>', OrganizationView.as_view()),


    path('Pipeline/', PipelineView.as_view()),
    path('Pipeline/<str:pk>', PipelineView.as_view()),


    path('PipelineNode/', PipelineNodeView.as_view()),
    path('PipelineNode/<str:pk>', PipelineNodeView.as_view()),


    path('User/', UserView.as_view()),
    path('User/<str:pk>', UserView.as_view()),


    path('auth/jwt/create', CustomTokenObtainPairView.as_view()),
    path("order_delivered/<str:pk>", OrderDelivered.as_view()),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
