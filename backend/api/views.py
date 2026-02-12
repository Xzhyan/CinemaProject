from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, FilmCard
from .serializer import FilmCardSerializer

@api_view(['GET'])
def films(request):
    films = FilmCard.objects.all()
    serializer = FilmCardSerializer(films, many=True)

    return Response({'films': serializer.data})
