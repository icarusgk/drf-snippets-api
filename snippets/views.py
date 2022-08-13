# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
# from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
# from rest_framework import status
# from django.http import Http404
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers




@api_view(['GET'])
def api_root(request, format=None):
  # we're using REST framework's reverse function in order to 
  # return fully-qualified URLs
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
  })


class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = [renderers.StaticHTMLRenderer]

  def get(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)
    

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

# Listing all the existing snippets or creating a new snippet
class SnippetList(generics.ListCreateAPIView):
  """
  List all code snippets, or create a new snippet
  """

  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  # .perform_create() method on our snippet views, that allows us to modify 
  # how the instance save is managed, and handle any information that 
  # is implicit in the incoming request or requested URL.

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

  # The create() method of our serializer will now be passed an additional 
  # 'owner' field, along with the validated data from the request.

  # The base class (GenericAPIView) provides the core functionality, 
  # and the mixin classes provide the .list() and .create() actions. 
  # We're then explicitly binding the get and post methods to
  # the appropriate actions.

  # def get(self, request, *args, **kwargs):
  #   return self.list(request, *args, **kwargs)

  # def post(self, request, *args, **kwargs):
  #   return self.create(request, *args, **kwargs)

  # Part 3 Class Based Views
  # def get(self, request, format=None):
  #   snippets = Snippet.objects.all()
  #   serializer = SnippetSerializer(snippets, many=True)
  #   return Response(serializer.data)

  # def post(self, request, format=None):
  #   serializer = SnippetSerializer(data=request.data)
  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.data, status=status.HTTP_201_CREATED)
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # if request.method == 'GET':
  #   snippets = Snippet.objects.all()
  #   serializer = SnippetSerializer(snippets, many=True)
  #   return Response(serializer.data)

  # elif request.method == 'POST':
  #   # Instead of parsing the binary data form the resquest
  #   # data = JSONParser().parse(request)

  #   # The @api_view nourishes the request and does that for us
  #   serializer = SnippetSerializer(data=request.data)
  #   if serializer.is_valid():
  #     serializer.save()
  #     # With rest_framework status we get access to more detailed
  #     # status codes
  #     return Response(serializer.data, status=status.HTTP_201_CREATED)
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  Retrieve, update or delete a code snippet
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  # def get(self, request, *args, **kwargs):
  #   return self.retrieve(request, *args, **kwargs)

  # def put(self, request, *args, **kwargs):
  #   return self.update(request, *args, **kwargs)

  # def delete(self, request, *args, **kwargs):
  #   return self.delete(request, *args, **kwargs)

  # def get_object(self, pk):
  #   try:
  #     # Get the snippet
  #     return Snippet.objects.get(pk=pk)
  #   except Snippet.DoesNotExist:
  #     raise Http404

  # def get(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   serializer = SnippetSerializer(snippet)
  #   # Return the data as JSON
  #   return Response(serializer.data)

  # def put(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   serializer = SnippetSerializer(snippet, data=request.data)
  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.data)
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # def delete(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   snippet.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)

  # if request.method == 'GET':
  #   serializer = SnippetSerializer(snippet)
  #   return Response(serializer.data)

  # elif request.method == 'PUT':
  #   # Part 1. Parse the binary data from the request
  #   # As a native python datatypes 
  #   # data = JSONParser().parse(request)

  #   # Replace the data from the snipped with the new received data
  #   serializer = SnippetSerializer(snippet, data=request.data)
  #   # If the parsed data received my the serializer is valid
  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.data)
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # elif request.method == 'DELETE':
  #   snippet.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)
    
    
