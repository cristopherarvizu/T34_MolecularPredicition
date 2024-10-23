from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_csv, name="upload_csv"),
    path("predictions/", views.prediction_list, name="prediction_list"),
    path("chart_data/<str:plot_type>/", views.get_chart_data, name="get_chart_data"),
    path("plot/", views.plot_data, name="plot_data"),
]
