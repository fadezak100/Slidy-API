
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import SlideSerializer
from .models import Slide
from .view_components import SlideCommonComponents
from users.mixins import UserViewSetPermissionMixin
from users.models import User
from users.serializers import UserWithSlidesSerializer


class SlideViewSet(UserViewSetPermissionMixin, viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer

    def get_object(self):
        slide = Slide.objects.filter(id=self.kwargs['pk'])
        if not slide:
            raise Http404("Slide not found")
        return User.objects.filter(slides_info__id=self.kwargs['pk']).first()

    def list(self, request, *args, **kwargs):
        query_set = User.objects.filter(username=request.user)
        data = UserWithSlidesSerializer(query_set, many=True).data

        return Response({
            "status_code": 200,
            "message": "success",
            "data": data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        slide_object = Slide.objects.filter(id=kwargs['pk']).first()
        slide_content = SlideSerializer(slide_object).data
        slide_url = slide_content['url']

        html_form = SlideCommonComponents.get_slide_content(slide_url)

        return Response({
            "status_code": 200,
            "message": "success",
            "html_content": html_form
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slide_file = request.data.get('slide')

        if not request.data.get('title'):
            serializer.validated_data['title'] = str(slide_file)

        serializer.validated_data['url'] = SlideCommonComponents.upload_files(
            slide_file)

        serializer.validated_data['user'] = request.user

        self.perform_create(serializer=serializer)
        return Response({
            "status_code": 200,
            "message": "success",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)

        slide_instance = Slide.objects.get(pk=kwargs['pk'])
        self.perform_destroy(slide_instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        slide_instance = Slide.objects.get(pk=kwargs['pk'])

        serializer = self.get_serializer(
            slide_instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save(
                title=serializer.validated_data.get(
                    'title') or slide_instance.title,
                description=serializer.validated_data.get(
                    'description') or slide_instance.description,
                is_public=serializer.validated_data.get(
                    'is_public') if not None else slide_instance.is_public,
                is_live=serializer.validated_data.get(
                    'is_live') if not None else slide_instance.is_live
            )

            return Response({
                "status_code": 200,
                "message": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)


view_slide_set = SlideViewSet.as_view
