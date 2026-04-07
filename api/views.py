from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import Device, BirdDetection, ActivityLog
from .serializers import (
    RegisterSerializer, UserSerializer, DeviceSerializer,
    BirdDetectionSerializer, ActivityLogSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(UserSerializer(request.user).data)


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BirdDetectionViewSet(viewsets.ModelViewSet):
    serializer_class = BirdDetectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = BirdDetection.objects.filter(device__owner=self.request.user)
        device_id = self.request.query_params.get('device')
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        detections = self.get_queryset().filter(detected_at__date=today)
        serializer = self.get_serializer(detections, many=True)
        return Response(serializer.data)


class ActivityLogViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ActivityLog.objects.filter(device__owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent = self.get_queryset()[:10]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
