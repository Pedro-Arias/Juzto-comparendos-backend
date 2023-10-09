from .models import *
from utils.tools import IUtility


class ComparendosDB:
    """
    Class base of different request profiles. The minimun profile have
    a origin, doc number, doc type a person type. This attributes are
    neccesary to make any type of request to obtain infractions.

    Args:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.

    Attributes:
        origin (str):       Request source system or client.
        doc_number (str):   Customer doc number.
        doc_type (str):     Customer doc type. Official doc types.
        person_type (str):  Customer person type (Natural, Jurídica).
        update (boolean):   Default False if update the Profile -> Persona
                            is not necessary.
        data_map (dict):    Data structure to transform a Profile in Persona
                            object.

    """
    def __init__(self, customer):
        self.__customer = customer


    def save(self, validated_data: dict) -> Comparendos:
        """
        Function to save the Profile data to Persona
        object in database.

        Args:
            validated_data (dict): a Profile dictionary with all data neccessary.

        Returns:
            Personas: A Personas object saved (created or updated).
        """
        comparendos = None
        try:
            # validated_data.pop('origin')
            map_object = self.__map_object(validated_data)

            if validated_data.get('_update'):
                comparendos = self.__update(map_object)

            else:
                comparendos = self.__create(map_object)

            return comparendos

        except Exception as err:
            result = err
        return comparendos

    def __create(self, c_data: dict):
        """
        Function to get or create a persona in database.
        Args:
            c_data (dict): A profile maped in Persona data structure.

        Returns:
            Persona: A Persona object obtained or created.
        """
        comparendos, _ = Comparendos.objects.get_or_create(**c_data)
        comparendos.save()

        return comparendos

    def __update(self, u_data: dict):
        """
        Function to update or create a persona in database.
        Args:
            u_data (dict): A profile maped in Persona data structure.

        Returns:
            Persona: A Persona object updated or created.
        """
        comparendos, _ = Comparendos.objects.update_or_create(
            id_comparendo=u_data.get('id_comparendo'),
            defaults=u_data)
        return comparendos

    def __map_object(self, validated_data: dict):
        """
        Function to map the profile data structure into a Persona object
        model structure.

        Args:
            validated_data (dict):  Profile dictionary with all
                                    data neccessary.

        Raises:
            Exception:              When de input data does not
                                    a dicctionary.

        Returns:
            dict:                   With the profile data maped into a
                                    Persona structure.
        """

        try:

            if isinstance(validated_data, dict):
                print(validated_data["infracciones"][0]["codigoInfraccion"])
                infraction = Infracciones.objects.filter(codigo=validated_data["infracciones"][0]["codigoInfraccion"])[0]
                data_map = {
                    'id_comparendo': validated_data['numeroComparendo'],
                    'infraccion': infraction,
                    'id_persona': self.__customer,
                    'fotodeteccion':validated_data['comparendoElectronico'],
                    'estado': 'Comparendo',
                    'fecha_imposicion': IUtility().format_date_verifik(validated_data['fechaComparendo']),
                    'fecha_resolucion': IUtility().format_date_verifik(validated_data['fechaResolucion']),
                    'fecha_cobro_coactivo': IUtility().format_date_verifik(validated_data['fechaCoactivo']),
                    'numero_resolucion': validated_data['fechaCoactivo'],
                    'numero_cobro_coactivo': validated_data['fechaCoactivo'],
                    'placa': validated_data['placa'],
                    'servicio_vehiculo': None,
                    'tipo_vehiculo': None,
                    'secretaria': validated_data['organismoTransito'],
                    'direccion': None,
                    'valor_neto': None,
                    'valor_pago': validated_data['valor'],
                    'scraper': "Juzto-simit",
                    'fecha_notificacion': IUtility().format_date_verifik(validated_data['fechaNotificacion']),
                    'origen': "Add_comp_endpoint"
                }
                return data_map

            raise Exception('Validated data does not a dict')

        except Exception as err:
            return err

