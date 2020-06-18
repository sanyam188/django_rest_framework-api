from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ItemSerializer, ItemRatingSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Rating
from rest_framework import permissions
# Create your views here.


class UserApiView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        # print(serializer)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemApiView(APIView):
    # permission_classes =  [permissions.IsAuthenticated]
    def get(self, request):
        item = Item.objects.all()
        serialize = ItemSerializer(item, many=True)
        return Response(serialize.data)

    def post(self, request):
        permission_classes =  [permissions.IsAuthenticated]
        serializer = ItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingApiView(APIView):
    permission_classes =  [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Rating.objects.filter(r_item = pk, r_user = self.request.user.pk)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)

    def set_user_item(self, request, obj, **kwargs):
        obj['r_item'] = kwargs.get('pk')
        obj['r_user'] = self.request.user.pk
        return obj

    def check_no_rating(self,**kwargs):
        try:
            if Rating.objects.get(r_item = kwargs.get('pk'), r_user = self.request.user.pk):
                return False
        except :
            return True


    def get(self, request, **kwargs):
        # print("jfjfj")
        item = self.get_object(kwargs.get('pk'))
        serialize = RatingSerializer(item, many=True)
        # print(serialize.data)
        return Response(serialize.data)



    def post(self, request,**kwargs):
        data = request.data
        data = self.set_user_item(request, data, **kwargs)
        serialize = RatingSerializer(data=data)
        print(serialize.initial_data)
        if serialize.is_valid() and self.check_no_rating(**kwargs):
            print("in")
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)



