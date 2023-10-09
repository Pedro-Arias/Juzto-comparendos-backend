from .models import *
import pandas as pd
from multiprocessing.pool import ThreadPool
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .profiles import BasicProfile
from utils.tools import IUtility
from .controllers import InfractionController
import threading


class Multas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        csv_file = request.FILES.get('file')
        
     
        hilo = threading.Thread(target=inicio(csv_file))
        hilo.start()
        object_response = {
            'status': 'Corriendo consulta',
            'error': None,
        }
        return Response(status=status.HTTP_200_OK, data=object_response)



def inicio(csv_file):
    print('entro')
    try:
        csv_file.content_type
    except Exception as err:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid parameters.'})  
    
    if 'text/csv' in csv_file.content_type:

        # df_multas = pd.DataFrame(columns=cols)
        #df_placas = pd.read_csv(csv_file, usecols=['Tipo_documento','Documento','Nombres','Apellidos','Email','Mobile','Origin'])
        df_placas = pd.read_csv(csv_file, usecols=['Tipo_documento','Documento','Origin'])
        df_placas['Numero_de_fila'] = df_placas.index + 1
        list_placas = df_placas.values.tolist()  
        log_data =  {
            'origen': 'CONSULTA MASIVA',
            'destino': 'scraper',
            'resultado': 2,
            'fecha': IUtility.datetime_utc_now(),
            'detalle': 'CONSULTA MASIVA INICIADA'
        }
        Logs.objects.create(**log_data)
    
        with ThreadPool(30) as pool:
            pool.starmap(multihilos, list_placas)
        
    else:
        return Response(status=status.HTTP_200_OK, data={'error': 'Invalid type file.'})
    
    log_data = {
        'origen': 'CONSULTA MASIVA',
        'destino': 'scraper',
        'resultado': 2,
        'fecha': IUtility.datetime_utc_now(),
        'detalle': 'CONSULTA MASIVA TERMINADA'
    }
    Logs.objects.create(**log_data)


    
def multihilos(Tipo_documento,Documento,Origin,Numero_de_fila):

    customer = BasicProfile(origin=Origin, doc_number=Documento, doc_type=Tipo_documento)
    person = customer.save(customer.__dict__)
    print(Numero_de_fila)

    infractions = InfractionController(customer)
     
    # Fetching to the external API 
    data_infractions, err = infractions._fetch_data_infractions()
    _, _, err = infractions._save_infractions(person)
    person.fecha_consulta_comp = IUtility().datetime_utc_now()
    person.save()
    

    
    return Response(status=status.HTTP_200_OK)
    