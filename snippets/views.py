# from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Listing all the existing snippets or creating a new snippet
@csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
  """
  List all code snippets, or create a new snippet
  """
  if request.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    # Instead of parsing the binary data form the resquest
    # data = JSONParser().parse(request)

    # The @api_view nourishes the request and does that for us
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      # With rest_framework status we get access to more detailed
      # status codes
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
  """
  Retrieve, update or delete a code snippet
  """
  try:
    # Get the snippet
    snippet = Snippet.objects.get(pk=pk)
  except Snippet.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  elif request.method == 'PUT':
    # Part 1. Parse the binary data from the request
    # As a native python datatypes 
    # data = JSONParser().parse(request)

    # Replace the data from the snipped with the new received data
    serializer = SnippetSerializer(snippet, data=request.data)
    # If the parsed data received my the serializer is valid
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
    
