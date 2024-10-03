import torch
from django.http import HttpResponse
# Verificar si PyTorch se ha instalado correctamente

print('verion xd xd /:', torch.__version__)

def verificacion(request):
    print('hola en la terminal')
    print(torch.__version__)
    # Verificar si tienes acceso a la GPU (esto debería devolver 'False' si no tienes una GPU NVIDIA)
    print(torch.cuda.is_available())
    return HttpResponse("¡Hola! xd xdL")
