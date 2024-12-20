from django.urls import path
from . import views
urlpatterns = [
    # path('map/', views.ListFoodView.as_view(), name='list-food'),
    path('map/', views.index, name='first-page'),
    path('map/list/', views.ListFoodView.as_view(), name='list-food'),
    path('map/<int:pk>/detail/', views.DetailFoodView.as_view(), name='detail-food'),
    path('map/create/', views.CreateFoodView.as_view(), name='create-food'),
    path('map/<int:pk>/delete/', views.DeleteFoodView.as_view(), name='delete-food'),
    path('map/<int:pk>/update/', views.UpdateFoodView.as_view(), name='update-food'),
    path('map/meat/', views.meat_view, name='meat-list'),
    path('map/vegetable/', views.vegetable_view, name='vegetable-list'),
    path('map/fruit/', views.fruit_view, name='fruit-list'),
    path('map/drink/', views.drink_view, name='drink-list'),
    path('map/frozen_food/', views.frozen_food_view, name='frozen_food-list'),
    path('map/noodle/', views.noodle_view, name='noodle-list'),
    path('map/seasoning/', views.seasoning_view, name='seasoning-list'),
    path('map/other/', views.other_view, name='other-list'),
    #path('map/update_voice/', views.VoiceUpdateFoodView.as_view(), name='update-food-voice'),
    path('map/process_voice_input/', views.process_voice_input, name='process_voice_input'),
    path('map/process_receipt_input/', views.process_receipt_input, name='process_receipt_input'),
    path('map/register-food/', views.register_food, name='register_food'),
    # path('map/receipt_result/', views.register_food, name='register_food'),
    path('send-notify/',views.my_view),
]
