from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from core.error import Erro
from contas.serializers import (
    UsuarioUpdateRequest, UsuarioUpdateMeRequest,
    UsuarioResponse, UsuarioSimpleResponse
)
from contas.services import UsuarioService

class UsuarioViewMe(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Retorna o usuário logado",
        responses = {
            200: UsuarioSimpleResponse,
            401: openapi.Response("Não autenticado"),
            },
        
        tags = ["Usuário"],
    )

    def get(self, request):
        usuario = UsuarioService.UsuarioMeService.listar(usuario_logado = request.user)

        if isinstance(usuario, Erro):
            return Response(
                usuario.to_response(),
                status = usuario.status_code
            )

        return Response(
            UsuarioSimpleResponse(usuario).data,
            status = status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Atualizar dados do usuário",
        request_body=UsuarioUpdateMeRequest,
        responses = {
            200: UsuarioResponse,
            400: openapi.Response("Erro de validação"),
            401: openapi.Response("Não autenticado"),
            409: openapi.Response("Conflito"),
            },
        tags=["Usuário"],
    )

    def put(self, request):
        serializer = UsuarioUpdateMeRequest(data = request.data)
        serializer.is_valid(raise_exception=True)

        resultado = UsuarioService.UsuarioMeService.atualizar(
                usuario_logado = request.user,
                data = serializer.validated_data
            )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status=resultado.status_code
            )

        return Response(
            UsuarioResponse(resultado).data,
            status=status.HTTP_200_OK
        )


class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Retorna uma lista de usuários",
        responses = {
            200: UsuarioSimpleResponse,
            401: openapi.Response("Não autenticado"),
            },
        
        tags = ["Usuários"],
    )

    def get(self, request):
        usuario = UsuarioService.listar(usuario_logado = request.user)

        if isinstance(usuario, Erro):
            return Response(
                usuario.to_response(),
                status = usuario.status_code
            )

        return Response(
            UsuarioSimpleResponse(usuario, many = True).data,
            status = status.HTTP_200_OK
        )