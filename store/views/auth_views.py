from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..serializers import RegisterSerializer, UserSerializer
from rest_framework import status

# 5. USER AUTH
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user': UserSerializer(user).data, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Try to get 'email' first, then fall back to 'username'
        email = request.data.get('email')
        username = request.data.get('username')
        
        # If they sent email, try to find the username associated with it
        if email and not username:
            from django.contrib.auth.models import User
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=request.data.get('password'))
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data, 
                'refresh': str(refresh), 
                'access': str(refresh.access_token)
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): return Response(UserSerializer(request.user).data)
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(): serializer.save(); return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request): request.user.delete(); return Response(status=status.HTTP_204_NO_CONTENT)