from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and Password required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(email=email, password=password)

    return Response({"message": "User created successfully"})
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def login(request):

    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })