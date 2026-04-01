from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Session, FilmCard, Promotion
from .serializer import FilmCardSerializer, SessionSerializer, PromotionSerializer


@api_view(['GET'])
def promotions(request):
    promotions = Promotion.objects.all()
    serializer = PromotionSerializer(promotions, many=True)

    return Response({'promotions': serializer.data})


@api_view(['GET'])
def films(request):
    films = FilmCard.objects.all()
    serializer = FilmCardSerializer(films, many=True)

    return Response({'films': serializer.data})


@api_view(['GET'])
def sessions(request):
    sessions = Session.objects.all()
    serializer = SessionSerializer(sessions, many=True)

    return Response({'sessions': serializer.data})
