from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .comparendos import ComparendosDB
from .profiles import BasicProfile
from utils.tools import IUtility
from .controllers import InfractionController
from django.core.files.storage import default_storage
from core_system.serializers.profiles import BasicProfileSerializer
from core_system.models import *
import threading


# Create your views here.

class Fotomultas(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        API function to fetch comparendos data from Verifik API and RPA projects.
        This API works as core system to collect all the data from different sources.

        Args:
            request (POST): Json request has 

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        _data = request.data
        
        object_response = {
            'data': list(),
            'status': None,
            'error': None,
        }
        err = None
        
        try:
            # A basic profile not demand all the data structure to fetch comparendos data
            profile_serializer = BasicProfileSerializer(data=_data)
            
            # Validating if the imput data is correct
            if profile_serializer.is_valid():
                
                customer = BasicProfile(_data['origin'], _data['doc_number'], _data['doc_type'])
                
                if _data['person_type']: customer._person_type = _data['person_type']
                if _data['first_name']: customer._first_name = _data['first_name']
                if _data['last_name']: customer._last_name = _data['last_name']
                if _data['email']: customer._email = _data['email']
                if _data['mobile']: customer._mobile = _data['mobile']
                if _data['recurrent_query']: customer._recurring_query = _data['recurrent_query']
                if _data['update']: customer._update = _data['update']
                
                person = Personas.objects.filter(documento=_data['doc_number'], tipo_documento=_data['doc_type']).first()
                
                infractions = InfractionController(customer)
                
                # Validating the cuote to renew comparendos data from the last datetime query 

                data_infractions, err = infractions.get_infractions_from_db(person, _data['origin'])
                    
                object_response['data'] = data_infractions
                object_response['status'] = 'success'
            else:
                raise Exception (profile_serializer.errors)
        
        except Exception as _except:

            object_response['status'] = 'error'
            object_response['error'] = err if err else _except.args
            # log con la excepción presentada
            print(_except)
            log_data =  {
                'origen': _data['origin'],
                'destino': 'Verifik',
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now(),
                'detalle': err if err else _except.args
            }

            Logs.objects.create(**log_data)
            
            object_response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(status=status.HTTP_200_OK, data=object_response)


class FotomultasConsulta(APIView):
    
    permission_classes = [IsAuthenticated]

    
    def post(self, request):
        """
        API function to fetch comparendos data from Verifik API and RPA projects.
        This API works as core system to collect all the data from different sources.

        Args:
            request (POST): Json request has 

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        def consulta():
            # Hacer algo que toma mucho tiempo aquí
            _data = request.data
            object_response = {
                'data': list(),
                'status': None,
                'error': None,
            }
            err = None
            
            try:
                # A basic profile not demand all the data structure to fetch comparendos data
                profile_serializer = BasicProfileSerializer(data=_data)
                
                # Validating if the imput data is correct
                if profile_serializer.is_valid():
                    
                    customer = BasicProfile(_data['origin'], _data['doc_number'], _data['doc_type'])
                    
                    if _data['person_type']: customer._person_type = _data['person_type']
                    if _data['first_name']: customer._first_name = _data['first_name']
                    if _data['last_name']: customer._last_name = _data['last_name']
                    if _data['email']: customer._email = _data['email']
                    if _data['mobile']: customer._mobile = _data['mobile']
                    if _data['recurrent_query']: customer._recurring_query = _data['recurrent_query']
                    if _data['update']: customer._update = _data['update']
                    
                    person = customer.save(customer.__dict__)
                    
                    infractions = InfractionController(customer)
                    
                    # Validating the cuote to renew comparendos data from the las datetime query 
                    refresh_query = infractions._is_allowed_by_date(person)
                     
                    if refresh_query:
                        # Fetching to the external API 
                        data_infractions, err = infractions._fetch_data_infractions()
                        _, _, err = infractions._save_infractions(person)
                        person.fecha_consulta_comp = IUtility().datetime_utc_now()
                        person.save()
                        if err:
                            raise Exception(err)
                    else:
                        # Fetching to the own data base
                        data_infractions, err = infractions.get_infractions_from_db(person, _data['origin'])
                        
                    object_response['data'] = data_infractions
                    object_response['status'] = 'success'
                else:
                    raise Exception (profile_serializer.errors)
            
            except Exception as _except:
    
                object_response['status'] = 'error'
                object_response['error'] = err if err else _except.args
                # log con la excepción presentada
                print(_except)
                log_data =  {
                    'origen': _data['origin'],
                    'destino': 'Verifik',
                    'resultado': 1,
                    'fecha': IUtility.datetime_utc_now(),
                    'detalle': err if err else _except.args
                }
    
                Logs.objects.create(**log_data)
                
                object_response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        
        hilo = threading.Thread(target=consulta)
        hilo.start()
        object_response = {
            'status': 'Corriendo consulta',
            'error': None,
        }
        return Response(status=status.HTTP_200_OK, data=object_response)
    


class ComparendosCrm(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        API function to fetch comparendos data from Verifik API and RPA projects.
        This API works as core system to collect all the data from different sources.

        Args:
            request (POST): Json request has 

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        _data = request.data
        
        object_response = {
            'data': list(),
            'status': None,
            'error': None,
        }
        err = None
        
        try:
            # A basic profile not demand all the data structure to fetch comparendos data
            profile_serializer = BasicProfileSerializer(data=_data)
            
            # Validating if the imput data is correct
            if profile_serializer.is_valid():
                
                customer = BasicProfile(_data['origin'], _data['doc_number'], _data['doc_type'])
                
                if _data['person_type']: customer._person_type = _data['person_type']
                if _data['first_name']: customer._first_name = _data['first_name']
                if _data['last_name']: customer._last_name = _data['last_name']
                if _data['email']: customer._email = _data['email']
                if _data['mobile']: customer._mobile = _data['mobile']
                if _data['recurrent_query']: customer._recurring_query = _data['recurrent_query']
                if _data['update']: customer._update = _data['update']
                
                person = customer.save(customer.__dict__)
                
                infractions = InfractionController(customer)
                
                # Validating the cuote to renew comparendos data from the las datetime query 
                refresh_query = infractions._is_allowed_by_date(person)
                 
                if refresh_query or _data['origin']=='CRM':
                    # Fetching to the external API 
                    data_infractions, err = infractions._fetch_data_infractions()
                    _, _, err = infractions._save_infractions(person)
                    person.fecha_consulta_comp = IUtility().datetime_utc_now()
                    person.save()
                    if err:
                        raise Exception(err)
                else:
                    # Fetching to the own database
                    data_infractions, err = infractions.get_infractions_from_db(person, _data['origin'])
                    
                object_response['data'] = data_infractions
                object_response['status'] = 'success'
            else:
                raise Exception (profile_serializer.errors)
        
        except Exception as _except:

            object_response['status'] = 'error'
            object_response['error'] = err if err else _except.args
            # log con la excepción presentada
            print(_except)
            log_data =  {
                'origen': _data['origin'],
                'destino': 'Verifik',
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now(),
                'detalle': err if err else _except.args
            }

            Logs.objects.create(**log_data)
            
            object_response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(status=status.HTTP_200_OK, data=object_response)


class SaveInDB(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        API function to fetch comparendos data from Verifik API and RPA projects.
        This API works as core system to collect all the data from different sources.

        Args:
            request (POST): Json request has

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        _data = request.data

        object_response = {
            'data': list(),
            'status': None,
            'error': None,
        }
        err = None
        customer_data = None
        try:
            # Validating if the imput data is correct
            if "multas" in _data:
                for multa in _data["multas"]:
                    if customer_data is None \
                        or (customer_data is not None
                            and customer_data.documento == multa["infractor"]["numeroDocumento"]
                            and customer_data.tipo_documento == multa["infractor"]["tipoDocumento"]):
                        customer_data = BasicProfile("Add_comp_endpoint", multa["infractor"]["numeroDocumento"], multa["infractor"]["tipoDocumento"])
                        customer_data = customer_data.get()

               # Validating the cuote to renew comparendos data from the las datetime query
                    comparendos_controller = ComparendosDB(customer=customer_data)
                    comparendos_controller.save(multa)

            object_response['status'] = 'success'

        except Exception as _except:

            object_response['status'] = 'error'
            object_response['error'] = err if err else _except.args
            # log con la excepción presentada
            print(_except)
            log_data = {
                'origen': _data['origin'],
                'destino': 'Verifik',
                'resultado': 1,
                'fecha': IUtility.datetime_utc_now(),
                'detalle': err if err else _except.args
            }

            Logs.objects.create(**log_data)

            object_response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(status=status.HTTP_200_OK, data=object_response)
