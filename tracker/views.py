import json

from tracker.models import LogTrace, PackageContainer
from django.http.response import HttpResponse, HttpResponseNotAllowed
from helpers import restfy
from .serializers import (
    LegalPersonSerializer,
    LogTraceSerializer,
    PackageContainerSerializer,
    PersonSerializer,
    StateSerializer, 
    CitySerializer, 
    NaturalPersonSerializer
)


log_trace_index, log_trace_by_id = restfy.make_rest(LogTraceSerializer)
(
    package_container_index, 
    package_container_by_id
) = restfy.make_rest(PackageContainerSerializer)
person_index, person_by_id = restfy.make_rest(
    PersonSerializer,
    allow_create=False, 
    allow_update=False, 
    allow_delete=False
)
legal_person_index, legal_person_by_id = restfy.make_rest(LegalPersonSerializer)
natual_person_index, natual_person_by_id = restfy.make_rest(NaturalPersonSerializer)
state_index, state_by_id = restfy.make_rest(StateSerializer)
city_index, city_by_id = restfy.make_rest(CitySerializer)


def package_container_log_trace_register(request, unique_identify):
    status = 501
    content = None
    
    try:
        payload = json.loads(request.body)
        package = PackageContainer.objects.get(unique_identify=unique_identify)
        log_trace = LogTraceSerializer.decode(payload)
        package.logs.add(log_trace, bulk=False)

        status = 201
        content = json.dumps({
            'package': PackageContainerSerializer.encode(package),
            'log_trace': LogTraceSerializer.encode(log_trace)
        })
    except PackageContainer.DoesNotExist:
        status = 404
        content = json.dumps({
            "message": "Pacote não encontrado"
        })
    except Exception as e:
        status = 400
        content = json.dumps({
            "message": str(e)
        })

    return HttpResponse(
        status=status,
        content=content,
        content_type='application/json'
    )


def package_container_log_trace_list(request, unique_identify):
    status = 501
    content = None

    try:
        package = PackageContainer.objects.get(unique_identify=unique_identify)
        
        status = 200
        content = json.dumps({
            'package': PackageContainerSerializer.encode(package),
            'log_traces': [LogTraceSerializer.encode(log) for log in package.logs.all()]
        })
    except PackageContainer.DoesNotExist:
        status = 404
        content = json.dumps({
            "message": "Pacote não encontrado"
        })
    except Exception as e:
        status = 400
        content = json.dumps({
            "message": str(e)
        })

    return HttpResponse(
        status=status,
        content=content,
        content_type='application/json'
    )


def package_container_log_trace(request, unique_identify):
    if request.method == 'GET':
        return package_container_log_trace_list(request, unique_identify)
    elif request.method == 'POST':
        return package_container_log_trace_register(request, unique_identify)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    
