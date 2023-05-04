from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .auth import authenticate_and_get_user, create_user_account
from eventsapi.models import Client

User = get_user_model()


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.LoginSerializer,
        'register': serializers.RegistrationSerializer,
        'password-change': serializers.PasswordChangeSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate_and_get_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        client_code = serializer.data.get('client_code')
        client = None
        if client_code:
            client = Client.objects.filter(code=client_code).first()
            if not client:
                return Response(data={'message': 'Invalid client code'}, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        validated_data.pop('client_code', None)
        user = create_user_account(**validated_data, client=client, client_rep=bool(client))
        registration_success_serializer = serializers.RegistrationSuccessSerializer(user)
        return Response(data=registration_success_serializer.data, status=status.HTTP_201_CREATED)

    # @action(methods=['POST', ], name='verify-email', url_path='verify-email', detail=False)
    # def verify_registration_email(self, request):
    #     email = request.data["email"]
    #     code = request.data["code"]
    #     try:
    #         verification = EmailVerification.objects.get(verification_code=code, user__email=email,
    #                                                      user_action='REGISTRATION', is_verified=False)
    #         if verification.is_verified:
    #             return Response(
    #                 data={'success': 0, 'message': 'This verification code has been used. Request a new code'},
    #                 status=status.HTTP_400_BAD_REQUEST)
    #         verification.is_verified = True
    #         verification.save()
    #         # try:
    #         User.objects.filter(email=verification.user.email).update(is_active=True)
    #         token, created = Token.objects.get_or_create(user=verification.user)
    #         data = {
    #             "user_id": verification.user.user_id,
    #             "email": verification.user.email,
    #             "first_name": verification.user.first_name,
    #             "last_name": verification.user.last_name,
    #             "phone_number": verification.user.phone_number,
    #             "system": verification.user.system.system_id,
    #             "staff": verification.user.is_staff,
    #             "auth_token": token.key
    #         }
    #         return Response(data=data, status=status.HTTP_200_OK)
    #     except User.DoesNotExist as e:
    #         return Response(data={'message': 'This account does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #         # return Response(data={'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
    #     except ObjectDoesNotExist as e:
    #         return Response(data={'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET', ], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except ObjectDoesNotExist:
            logout(request)
        data = {'message': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], name='change-password', url_path='change-password', detail=False,
            permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['POST'], name='reset-password', url_path='reset-password', detail=False,
    #         permission_classes=[AllowAny, ])
    # def reset_password(self, request):
    #     email = request.data['email']
    #     code = request.data['code']
    #     password = request.data['password']
    #
    #     try:
    #         verification = EmailVerification.objects.get(verification_code=code, user__email=email,
    #                                                      user_action='FORGOT_PASSWORD', is_verified=False)
    #         if verification.is_verified:
    #             return Response(
    #                 data={'success': 0, 'message': 'This verification code has been used. Request a new code'},
    #                 status=status.HTTP_400_BAD_REQUEST)
    #         verification.is_verified = True
    #         verification.save()
    #         user = User.objects.get(email=email)
    #         user.set_password(password)
    #         user.save()
    #         return Response(data={'success': 1, 'message': 'Password reset successful'})
    #     except User.DoesNotExist:
    #         return Response(data={'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     except ObjectDoesNotExist:
    #         return Response(data={'message': 'Invalid verification code'}, status=status.HTTP_404_NOT_FOUND)

    # @action(methods=['POST'], name='forgot-password', url_path='forgot-password', detail=False,
    #         permission_classes=[AllowAny, ])
    # def forgot_password_email(self, request):
    #     email = request.data.get('email')
    #     if not email:
    #         return Response({'status': 'error', 'message': 'Email is required'})
    #     try:
    #         user = User.objects.get(email=email)
    #         verification_code = hashlib.sha256((user.email + str(user.pk)).encode()).hexdigest()
    #         EmailVerification.objects.get_or_create(user=user, verification_code=verification_code,
    #                                                 user_action='FORGOT_PASSWORD', is_verified=False)
    #         email = user.email
    #         subject = 'Password reset link'
    #         message = 'Hello, below is the password reset link.\n' \
    #                   'Please click on the link to complete the process.\n' \
    #                   f'https://voting.kenyatheatreawards.com/new-credentials?em={email}&vc={verification_code}'
    #         from_email = settings.EMAIL_HOST_USER
    #         recipient_list = [email]
    #         send_mail(subject, message, from_email, recipient_list)
    #         return Response({'status': 'success', 'message': 'Password reset link sent to your email'})
    #     except User.DoesNotExist:
    #         return Response({'status': 'error', 'message': 'Email address not found in the database'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     except smtplib.SMTPException as e:
    #         print(e)
    #         return Response(data={'message': 'We could not send an email.', 'exception': f'{e}'},
    #                         status=status.HTTP_408_REQUEST_TIMEOUT)

    # @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated, ])
    # def profile(self, request):
    #     from votingapi.models import Vote
    #     votes = Vote.objects.filter(voter=request.user.user_id)
    #     voter = request.user
    #     votes_array = []
    #     for vote in votes:
    #         single_vote = {
    #             "nominee": f'{vote.nominee.first_name} {vote.nominee.last_name}',
    #             "category": vote.category.name
    #         }
    #         votes_array.append(single_vote)
    #     response = {"name": f'{voter.first_name} {voter.last_name}', "email": voter.email, 'votes': votes_array}
    #     return Response(data=response, status=status.HTTP_200_OK)
