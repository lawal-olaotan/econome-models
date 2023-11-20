from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import UserTrials
from .translator.conversation import Chatbot

from .serializers import UserTrialSerializer

# Create your views here.
class ChatAppView(APIView):

    def get(self, request, *args, **kwargs ):
        chat = Chatbot()
        postedBy = request.query_params.get('postedBy')
        message = request.query_params.get('message')
        chat_response = chat.get_response(message,postedBy)
        # take data from request and reterieve all data 
        list= UserTrials.objects.filter( )
        serializer=UserTrialSerializer(list,many=True)

        return Response( chat_response , status=status.HTTP_200_OK)

    