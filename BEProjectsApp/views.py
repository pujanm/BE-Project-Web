from BEProjectsApp.models import Project, TeacherProfile, Contributor
from BEProjectsApp.serializers import (
    ProjectSerializer,
    TeacherSerializer,
    ContributorSerializer,
    UserSerializer,
    LoginSerializer,
)
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import serializers
from django.contrib.auth.models import User
<<<<<<< HEAD
from rest_framework.response import Response

# from drf_multiple_model.viewsets import FlatMultipleModelAPIViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
=======
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsUserOrReadOnly
>>>>>>> 3b025ab4e6821ce603a7e27138a2fcbff070b1fc


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = (
        "company",
        "supervisor",
        "domain",
        "is_inhouse",
        "approved",
        "year_created",
        "title",
        "teacher",
    )


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = ("subject",)
    permission_classes = (IsUserOrReadOnly, IsAuthenticatedOrReadOnly)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    filterset_fields = ("name", "last_name", "email")


class SearchProjectView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        count = []
        SearchResult = []

        search = request.query_params["generic"]

        # Get the required projects  based on search
        projects = Project.objects.filter(title__startswith=search)
        contributors = Contributor.objects.filter(name__startswith=search)

        context = {"request": request}

        # Count the total number of search results
        count.append({"ProjectCount": projects.count()})
        # count.append({"ContributorCount": contributors.count()})

        projects = (ProjectSerializer(projects, many=True, context=context)).data

        contributors = (
            ContributorSerializer(contributors, many=True, context=context)
        ).data

        # Sort in ascending order of project titles
        projects = sorted(projects, key=lambda k: k["title"])

        labels = ["count", "projects", "contributors"]

        Result = [count, projects, contributors]

        for indx, label in enumerate(labels):
            SearchResult.append({label: Result[indx]})

<<<<<<< HEAD
# class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer


# class AllProjectsView(FlatMultipleModelAPIViewSet):
#     sorting_fields = ['title','name']
#     querylist = [
#         {
#             'queryset' : Project.objects.all(),
#             'serializer_class' : ProjectSerializer,
#             'label' : 'Projects',
#         },
#         {
#             'queryset' : Contributor.objects.all(),
#             'serializer_class' : ContributorSerializer,
#             'label' : 'Contributors',
#         },

#     ]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('^title','^name')

# import pdb; pdb.set_trace()

# class SearchProjectView(FlatMultipleModelAPIViewSet):
#     def get_querylist(self):
#         c = 0

#         title = self.request.query_params['title']
#         querylist = [
#             {
#                 'queryset' : Inhouse_Project.objects.filter(title__startswith = title),
#                 'serializer_class' : InhouseProjectSerializer,
#                 'label' : 'InhouseProject',
#             },
#             {
#                 'queryset' : Outhouse_Project.objects.filter(title__startswith = title),
#                 'serializer_class' : OuthouseProjectSerializer,
#                 'label' : 'OuthouseProject',
#             },

#         ]

#         for _ in querylist:

#             c = c +1
#         c = c-1
#         print(c)


#         return querylist


class SearchProjectView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        count = []
        # contributors = []
        search = request.query_params["name"]

        # Get the required projects  based on search
        projects = Project.objects.filter(title__startswith=search)
        contributors = Contributor.objects.filter(name__startswith=search)

        context = {"request": request}

        # Count the total number of search results
        count.append({"count": projects.count()})

        projects = (ProjectSerializer(projects, many=True, context=context)).data

        contributors = (
            ContributorSerializer(contributors, many=True, context=context)
        ).data

        # Add type to each project i.e. inhouse and outhouse
        for project in projects:
            if project["is_inhouse"] == True:
                project.update({"type": "Inhouse_Project"})
            else:
                project.update({"type": "Outhouse_Project"})

        # Sort in ascending order of project titles
        projects = sorted(projects, key=lambda k: k["title"])

        # combine inhouse, outhouse and count
        projects = projects + count + contributors
        return Response(projects)
=======
        return Response(SearchResult)
>>>>>>> 3b025ab4e6821ce603a7e27138a2fcbff070b1fc
