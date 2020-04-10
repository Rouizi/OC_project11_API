from django.urls import path
from users.views import SaveProduct, ListSavedProduct, ProfileUser, EditProfile


urlpatterns = [
    path('save-product/<id_substitute>', SaveProduct.as_view(), name='save-product'),
    path('list-saved-product/', ListSavedProduct.as_view(), name='list-saved-product'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
]
