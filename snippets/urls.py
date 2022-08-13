from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
  path('snippets/', views.SnippetList.as_view()),
  path('snippets/<int:pk>', views.SnippetDetail.as_view())
]

# For suffixes such as .html | .json | .api
urlpatterns = format_suffix_patterns(urlpatterns)