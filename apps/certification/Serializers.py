from rest_framework import serializers
from .models import RealAuth


class RealAuthSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default = 'success', read_only=True)
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()

    class Meta:
        model = RealAuth
        fields = ('status','image1', 'image2')

        # if photo and hasattr(photo, 'url'):
        #     photo_url = car.photo.url
        #     return request.build_absolute_uri(photo_url)
        # else:
        #     return None


    def get_image1(self, realauth):
        request = self.context.get('request')
        if realauth.image1 and hasattr(realauth.image1, 'url'):
            image1 = realauth.image1.url
            return request.build_absolute_uri(image1)
        else:
            return "False"

    def get_image2(self, realauth):
        request = self.context.get('request')
        if realauth.image2 and hasattr(realauth.image2, 'url'):
            image2 = realauth.image2.url
            return request.build_absolute_uri(image2)
        else:
            return "False"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['image1']:
            data['image1'] = "False"
        if not data['image2']:
            data['image2'] = "False"
        return data
