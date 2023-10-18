from django.shortcuts import render

class RegisterView(generics.CreateAPIView):
    queryset = SiteUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def SiteUser(request):
    # Request the information about the user making the request
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SiteUserSerializer(user, context={'request': request})
        return Response(serializer.data)