from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import  Room
from .serializers import Roomserializers

@api_view(['GET'])
def getroutes(request):
    routes = [
        'hello',
        'GET / api '
        'GET / api/rooms'
    ]
    return Response(routes)

@api_view(['GET'])
def getrooms(request):
    rooms = Room.objects.all()
    serializers = Roomserializers(rooms,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getroom(request,pk):
    rooms = Room.objects.get(id=pk)
    serializers = Roomserializers(rooms,many=False)
    return Response(serializers.data)