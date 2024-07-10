from django.http import JsonResponse
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework import status
from django.core.validators import EmailValidator
import jwt
import datetime
validator = EmailValidator() 
def EmailHandler(email) -> bool:
    '''This will Handle Email'''
    try:
        validator(email)
        return True
    except:
        return False
def check_user_exists(email):
    """
    Checks if a user exists with the given email address.
    """
    return User.objects.filter(email=email).exists()
def generateTokens(user):
    '''This Function help to generate access and refresh Token'''
    refresh = RefreshToken.for_user(user)
    return  {
        'refresh' : refresh,
        'access' : refresh.access_token
        }
def checkToken(request = None,jwtToken = None) -> dict:
    '''Check token'''
    if not jwtToken == None:
        token = jwtToken
    else:
        token = request.COOKIES.get('jwt')
    if not token:
        return {
            'error' : True,
            'mssg' : "No cookie found"
        }
    try:
        payload = jwt.decode(token,'secret',algorithms=["HS256"])
    except :
        return {
            'error': True,
            'mssg': "Session expired or Incorrect key. Please login again."
        }
    
    try:
        return {
            'error':False,
            'userId' : payload['id']
        }
    except:
        return Response({
            'error': True,
            'mssg': "Internal Server Error"
        })
# Create your views here.
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        errorMssg ={
            'error' : False,
            'mssg' : "",
        }
        try:
            serializer = UserSerialzer(data=request.data)
            data = request.data
            if serializer.is_valid():

                #Checking Email is Valid or Not!
                if not EmailHandler(data['email']):
                    errorMssg['error'] = True
                    errorMssg['mssg'] =  "Invalid Email"
                    return Response(errorMssg)
                
                # Checking if person exist
                if check_user_exists(data['email']):
                    errorMssg['error'] = True
                    errorMssg['mssg'] =  "Email Exist!"
                    return Response(errorMssg)
                
                serializer.create(validated_data = request.data)
                return Response(errorMssg)
        except:
            errorMssg['error']  = True
            errorMssg['mssg'] = "Internal Server Error"
            return Response(errorMssg, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self,request):
        res = {
            'error': False,
            'mssg' : "",
        }
        data = request.data
        try:
            serializer = LoginSerialzer(data=data)
            if serializer.is_valid():
                user = User.objects.filter(email = data['email']).first()
                if user is None:
                    res['error'] = True
                    res['mssg'] = "Email not registered"
                    return Response(res)
                if not user.check_password(data['password']):
                    res['error'] = True
                    res['mssg'] = "Incorrect Password"
                    return Response(res)

                
                # JWT
                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
                    'iat': datetime.datetime.now(datetime.UTC)
                }
                print(datetime.datetime.now(datetime.UTC))
                token = jwt.encode(payload,'secret',algorithm="HS256")
               
                response = Response()
                response.set_cookie(key='jwt',value=token,httponly=True)
                res['jwt'] = token
                response.data = res
                print(res)
                return response
        except:
            res['error'] = True
            res['mssg'] = "Internal Server Error"
            return res
class UserView(APIView):
    def get(self,request):
        response = checkToken(request)
        print(response)
        return Response(response)
        
        


            
            
        

                    



