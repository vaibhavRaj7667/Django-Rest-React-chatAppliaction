from django.shortcuts import render
from app.serializer import CreateUserSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import FriendList
from django.shortcuts import get_object_or_404

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        return Response({"message": f"This is a protected route ${user}"})
    
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class UserFriendsView(APIView):
    def get(self, request, user_id):
        friend_list = get_object_or_404(FriendList, user__id=user_id)  
        friends = friend_list.friends.all()  

        serializer = UserSerializer(friends, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    

class createuser(APIView):
    def post(self, request):
        print(request.data)
        serializer = CreateUserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
