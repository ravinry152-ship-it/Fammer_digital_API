from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from  . models import SaleProduct , Learning , RicePrice , RiceVarieties
from . serializers import SaleProductSerializer, LearningSerializer ,RicePriceSerializer ,RiceVarietiesSerializer
#from django.conf import settings
#==================================Register_API==============================
class Register(APIView) :
    permission_classes = [AllowAny,] 
    authentication_classes = []
    def post(self , request , format =None) :
        try :
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password or not username :
                return Response({
                    'error': "Username, email, and password are required"
                }, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'error': 'គណនីនេះត្រូវបានចុះឈ្មោះរួចហេីយ'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'គណនីនេះធ្លាប់បានចុះឈ្មោះរួចហេីយ'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#====================================Login_api======================================
class Login(APIView) :
    permission_classes = [AllowAny,] 
    def post(self , request , format=None) :
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password or not username :
            return Response({
                'error': "សូមបញ្ចូល Email និងលេខសម្ងាត់ និងឈ្មោះអ្នកប្រើប្រាស់ឪ្យបានត្រឹមត្រូវ"   
            }, status=status.HTTP_400_BAD_REQUEST)
        try :
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist :
            return Response({
                'error': "មិនមានគណនីប្រើប្រាស់អុីម៉ែលនេះទេ"
            }, status=status.HTTP_404_NOT_FOUND)
        if user_obj is not None :
            if user_obj.check_password(password):
                #login(request, user_obj)
                refresh = RefreshToken.for_user(user_obj)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': username
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': "ពាក្យសម្ងាត់ឬអុឺម៉ែលមិនត្រឹមត្រូវ"
                }, status=status.HTTP_400_BAD_REQUEST)
            
#==========================================Saleproduct_API=====================================
class SaleProductView(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request , format = None) :
        product = SaleProduct.objects.all()
        serializer = SaleProductSerializer(product , many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self , request , format = None):
        serializer = SaleProductSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
class SaleProductDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return SaleProduct.objects.get(pk=pk)
        except SaleProduct.DoesNotExist:
            return None
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SaleProductSerializer(product)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = SaleProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
#===================================Rice-price===========================================
class RicePriceView(APIView)  :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request ,format=None) :
        riceprice = RicePrice.objects.all()
        serializer = RicePriceSerializer(riceprice , many=True) 
        return Response(serializer.data , status=status.HTTP_200_OK)
    def post(self ,request , formet=None) :
        serialzer = RicePriceSerializer(data = request.data)
        if serialzer.is_valid() :
            serialzer.save()
            return Response(serialzer.data , status=status.HTTP_201_CREATED)
        print(serialzer.errors)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
#======================================rice-price=========================================
class DetailRicePrice(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self , pk) :
        try :
            return RicePrice.objects.get(pk=pk)
        except RicePrice.DoesNotExist :
            return None
    def get(self , request ,pk,format=None)  :
        price = self.get_object(pk) 
        if  not  price:
            return Response({'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer= RicePriceSerializer(price)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def put(self , request , pk) :
        price = self.get_object(pk)
        if not price :
            return Response({"not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RicePriceSerializer(price, data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    def delete(self ,request , pk ) :
        price = self.get_object(pk)
        if not price:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        price.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
#===========================================Learning======================================
class LearningViews(APIView)  :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request , format=None) :
        learn = Learning.objects.all()
        serializer = LearningSerializer(learn , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def post(self , request ,format=None) :
        serialzer = LearningSerializer(data = request.data)
        if serialzer.is_valid() :
            serialzer.save()
            return Response(serialzer.data , status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
class LearningHistrory(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Learning.objects.get(pk=pk)
        except Learning.DoesNotExist:
            return None

    def get(self, request, pk):  
        learn = self.get_object(pk)
        if not learn:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LearningSerializer(learn)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        learning = self.get_object(pk)
        if not learning:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LearningSerializer(learning, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk): 
        learn = self.get_object(pk)
        if not learn:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        learn.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#======================================================Rice varieties================================    
class Ricevarietie(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self , request , Format=None) :
        rice = RiceVarieties.objects.all()
        serializer = RiceVarietiesSerializer(rice , many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    def post(self ,request ,Format=None) :
        #request.data គឺជាចំណុចពិសេសរបស់ DRF ដែលវាជួយ Parse រាល់ទិន្នន័យដែលមកពី 
        # Frontend (មិនថាជា JSON, Form Data ឬទម្រង់ផ្សេងទៀត) មកជា 
        # Python Dictionary ដោយស្វ័យប្រវត្តិ
        serializer = RiceVarietiesSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("error")
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
class RicevarietieDetail(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self , pk) :
        try :
            #ទាញរកអ្វីដែលuserបោះមករួចទៅរកក្នុងTable
            return RiceVarieties.objects.get(pk=pk)
        #បេីអ្វីដែលUserបោះមកអត់មានវាចាប់error
        except RiceVarieties.DoesNotExist :
            return None
    def put(self , request ,pk)  :
        rice = self.get_object(pk) 
        #បោះមកUserវិញថាdataនឹងអត់មាននោះទេវានឹងចេញerror 404 not found
        if not rice :
            return Response ({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND) 
        serializer = RiceVarietiesSerializer(rice, data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_200_OK)
        print("error")
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request , pk) :
        rice = self.get_object(pk)
        if not rice:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        rice.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#================================================ML==============================================
# ១. Load Model ទុកជាមុន (Global variable) ដើម្បីឱ្យលឿន
# ចំណាំ៖ ត្រូវឆែកមើល Path របស់ File ឱ្យត្រឹមត្រូវ
# MODEL_PATH = os.path.join(settings.BASE_DIR, 'farmer_api', 'rice_model.pkl')

# # ២. Load Model
# try:
#     model = joblib.load(MODEL_PATH) # ប្រើឈ្មោះឱ្យដូចខាងលើ
#     print("AI Model ត្រូវបាន Load ជោគជ័យ!")
# except Exception as e:
#     model = None
#     print(f"ការព្រមាន: មិនអាច Load Model បានទេ ដោយសារ {e}")

# @csrf_exempt
# def predict_yield(request):
#     if request.method == 'POST':
#         if model is None:
#             return JsonResponse({'status': 'error', 'message': 'Model មិនទាន់បានដំឡើងក្នុង Server ទេ'})
            
#         try:
#             # ទទួលទិន្នន័យពី Flutter
#             data = json.loads(request.body)
#             area = float(data.get('area', 0))

#             # បង្កើត DataFrame ឱ្យត្រូវតាម Format (Column: 'Area')
#             input_df = pd.DataFrame([[area]], columns=['Area'])

#             # ឱ្យ AI ទាយ
#             prediction = model.predict(input_df)
#             result = prediction[0]

#             return JsonResponse({
#                 'status': 'success',
#                 'area': area,
#                 'predicted_production_tons': round(result, 2),
#                 'message': 'AI បានទាយរួចរាល់'
#             })
            
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': f'កំហុសបច្ចេកទេស: {str(e)}'})

#     return JsonResponse({'status': 'error', 'message': 'សូមប្រើវិធី POST'})

   





  
    
    

        
