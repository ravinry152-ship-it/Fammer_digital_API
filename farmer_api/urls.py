from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('saleproducts/', views.SaleProductView.as_view()),
    path('product-detail/<int:pk>/', views.SaleProductDetail.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('rice-price/', views.RicePriceView.as_view()),
    path('rice-price/<int:pk>/', views.DetailRicePrice.as_view()),
    path('learning/' , views.LearningViews.as_view()),
    path("histrory/<int:pk>/", views.LearningHistrory.as_view()),
    path('ricevarietie/', views.Ricevarietie.as_view()),
    path('ricevarietiedetail/<int:pk>/', views.RicevarietieDetail.as_view()),
    path('predict_yield/', views.predict_yield, name= 'predict_yield')
]
