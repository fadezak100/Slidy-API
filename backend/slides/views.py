from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

import cloudinary.uploader

from .serializers import SlideSerializer
from .models import Slide

class SlideViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Slide.objects.all()
    serializer_class =  SlideSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        slide_file = request.data.get('slide')
        upload_data = cloudinary.uploader.upload(slide_file, resource_type="auto")
        serializer.validated_data['url'] = upload_data.get('url')
        serializer.validated_data['user'] = request.user

        self.perform_create(serializer=serializer)
        return Response({
            "state": 200,
            "message": "success",
            "data": serializer.data
        })
        
view_slide_set = SlideViewSet.as_view
