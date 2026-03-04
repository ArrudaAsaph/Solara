from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.error import Erro
from contas.serializers import (
    VendedorCreateRequest,
    VendedorUpdateRequest,
    VendedorResponse,
    VendedorSimpleResponse,
)
from contas.services import VendedorService


class VendedorView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Cadastrar vendedor",
        request_body = VendedorCreateRequest,
        responses = {
            201: VendedorResponse,
            400: openapi.Response("Erro de validação"),
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
            409: openapi.Response("Conflito"),
        },
        tags = ["Vendedores"],
    )
    def post(self, request):
        serializer = VendedorCreateRequest(data = request.data)
        serializer.is_valid(raise_exception = True)

        resultado = VendedorService.criar(
            usuario_logado = request.user,
            data = serializer.validated_data,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code,
            )

        return Response(
            VendedorResponse(resultado).data,
            status = status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        operation_summary = "Listar vendedores",
        manual_parameters = [
            openapi.Parameter("nome", openapi.IN_QUERY, description = "Filtrar por nome", type = openapi.TYPE_STRING),
            openapi.Parameter("status", openapi.IN_QUERY, description = "Filtrar por status", type = openapi.TYPE_STRING),
            openapi.Parameter("data_inicio", openapi.IN_QUERY, description = "Data inicial de cadastro (YYYY-MM-DD)", type = openapi.TYPE_STRING),
            openapi.Parameter("data_fim", openapi.IN_QUERY, description = "Data final de cadastro (YYYY-MM-DD)", type = openapi.TYPE_STRING),
        ],
        responses = {
            200: VendedorSimpleResponse(many = True),
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
        },
        tags = ["Vendedores"],
    )
    def get(self, request):
        filtros = {
            "nome": request.query_params.get("nome"),
            "status": request.query_params.get("status"),
            "data_inicio": request.query_params.get("data_inicio"),
            "data_fim": request.query_params.get("data_fim"),
        }

        resultado = VendedorService.listar(
            usuario_logado = request.user,
            filtros = filtros,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code,
            )

        return Response(
            VendedorSimpleResponse(resultado, many = True).data,
            status = status.HTTP_200_OK,
        )


class VendedorPrivateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Atualizar vendedor",
        request_body = VendedorUpdateRequest,
        responses = {
            200: VendedorResponse,
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
            404: openapi.Response("Vendedor não encontrado"),
            409: openapi.Response("Conflito"),
            422: openapi.Response("Dados inválidos"),
        },
        tags = ["Vendedores"],
    )
    def put(self, request, id):
        serializer = VendedorUpdateRequest(data = request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        resultado = VendedorService.atualizar(
            usuario_logado = request.user,
            id = id,
            data = serializer.validated_data,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code,
            )

        return Response(
            VendedorResponse(resultado).data,
            status = status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary = "Remover vendedor",
        responses = {
            204: openapi.Response("Vendedor removido"),
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
            404: openapi.Response("Vendedor não encontrado"),
            409: openapi.Response("Vínculo financeiro/comercial impede remoção"),
        },
        tags = ["Vendedores"],
    )
    def delete(self, request, id):
        resultado = VendedorService.remover(
            usuario_logado = request.user,
            id = id,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code,
            )

        return Response(status = status.HTTP_204_NO_CONTENT)
