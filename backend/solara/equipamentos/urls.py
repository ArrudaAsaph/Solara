from django.urls import path
from equipamentos.views import *

app_name = "equipamentos"

urlpatterns = [
    path("equipamentos/", EquipamentoView.as_view(), name = "equipamentos"),
    
    

]
