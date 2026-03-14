""""
class RegisterAPI(APIView):
    permission_classes = [AllowAny,] 
    authentication_classes = []
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            # 1. Validation check(អត់Email and password and username is error)
            if not email or not password or not username:
                return Response(
                    {'error': "Username, email, and password are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username).exists():
                return Response({'error': "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Account created successfully",
                "email": user.email,
                "user_id": user.id,
                "access": str(refresh.access_token), 
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#======================================Login-API=======================================
class login_api(APIView) :
    permission_classes = [AllowAny,]
    def post(self , request , format=None) :
         email = request.data.get('email')
         password = request.data.get('password')
         if not email or not password :
             return Response({
                 "error": "សូមបញ្ចូល Email និងលេខសម្ងាត់"
             } , status=status.HTTP_400_BAD_REQUEST)
         try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
         except User.DoesNotExist:
            return Response({
                "error": "មិនមានគណនីប្រើប្រាស់អ៊ីមែលនេះទេ"
            }, status=status.HTTP_401_UNAUTHORIZED)
         user = authenticate(request, username=username, password=password)
    #========================================================================
         if user is not None:
          login(request, user) 
          refresh = RefreshToken.for_user(user)
          access_token = str(refresh.access_token)
          role = "admin" if user.is_staff else "user"
          return Response({
            "message": "Login successful",
             "access": access_token,   
            "refresh": str(refresh),
            "email": user.email,
            "user_id": user.id,
            "is_staff": user.is_staff,
            "role": role
        }, status=status.HTTP_200_OK)
         else:
           return Response({
            "error": "Invalid credentials.",
        }, status=status.HTTP_401_UNAUTHORIZED)
"""
