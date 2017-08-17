
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from assembly_auth.forms import AssemblyUserCreationForm
from .models import Profile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, parsers, renderers
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


def registration_complete(request):
    '''renders registration complete page'''
    return render(request, 'registration/registration_form_complete.html')


def register(request, extra_context=None):
    '''register a new user'''
    form = AssemblyUserCreationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            new_user = authenticate(username=form.cleaned_data['username'].lower(),
                                    password=form.cleaned_data['password1']
                                    )

            if new_user and new_user.is_authenticated:
                '''We have to login once so the last login date is set'''
                login(request, new_user)

                # has_send = send_email_confirmation(request, new_user) #ToDO
                has_send = True

                request_context = RequestContext(request)

                if has_send:
                    return render(request, 'registration/registration_form_complete.html',
                                  {"success_registration": True, "user": new_user})
                else:
                    return render(request, 'registration/registration_form_complete.html',
                                  {"success_registration": False})
            else:
                print('new_user is not authenticated')
        else:
            '''not a valid form'''
            print(form.error_messages)

    return render(request, 'registration/registration_form.html', {'form': form})

    if request.user.is_authenticated():
        '''if user is authenticated, it means he is already a registered user'''
        request_context.push({"has_account": True})
        return render(request, 'registration/registration_form_complete.html', request_context)

    user_profile = get_object_or_404(Profile)

    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()

    request_context.push({"success_activation": True})
    request_context.push({"user": user_account})
    return render(request, 'registration/registration_form_complete.html', request_context)


@login_required(login_url='/api-auth/login/')
def fetch_auth_token(request):
    token, created = Token.objects.get_or_create(user=request.user)  # @UnusedVariable
    json_data = {'token': token.key}
    return JsonResponse(json_data)


class CustomObtainAuthToken(generics.CreateAPIView):
    """
    post:
    Retrieve authtoken.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)  # @UnusedVariable
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()
