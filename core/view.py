from rest_framework.views import APIView
from core.models import Order, User
from django.db.models.query_utils import Q
from prototype.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status, permissions
# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        {
        "email": "user9@user.com",
        }
        {
        "email": "user9@user.com",
        "password": "00000",
        }
        """

        user = User.objects.filter(
            Q(email=request.data['email']) | Q(
                username=request.data['email'])
        )
        if not user.exists():
            raise InvalidToken("user does not exist")
        try:
            request.data['email'] = user[0].email
        except:
            pass

        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class OrderDelivered(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.completion = Order.delivered
        order.save()
        return Response("Order Delivered Successfully", status=status.HTTP_200_OK)
