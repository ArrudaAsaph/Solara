from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.error import Erro
from contas.serializers import PessoaResponse, PessoaSimpleResponse, PessoaUpdatePrivateRequest
from contas.services import PessoaService

class PessoaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retorna lista de pessoas da empresa",
        manual_parameters=[
            openapi.Parameter(
                "nome",
                openapi.IN_QUERY,
                description="Filtrar por nome",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "tipo_perfil",
                openapi.IN_QUERY,
                description="Filtrar por tipo de perfil",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Status do usuário",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: PessoaSimpleResponse(many=True),
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
        },
        tags=["Pessoas"],
    )
    def get(self, request):
        filtros = {
            "nome": request.query_params.get("nome"),
            "tipo_perfil": request.query_params.get("tipo_perfil"),
            "status": request.query_params.get("status"),
        }

        pessoas = PessoaService.listar(
            usuario_logado=request.user,
            filtros=filtros
        )

        if isinstance(pessoas, Erro):
            return Response(
                pessoas.to_response(),
                status=pessoas.status_code
            )

        return Response(
            PessoaSimpleResponse(pessoas, many=True).data,
            status=status.HTTP_200_OK
        )

    
class PessoaPrivateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = "Buscar pessoa por ID",
        responses={
            200: PessoaResponse,
            403: openapi.Response("Sem permissão"),
            404: openapi.Response("Pessoa não encontrada"),
        },
        tags=["Pessoas"],
    )
    
    def get(self, request, id):
        resultado = PessoaService.buscar_por_id(
            usuario_logado=request.user,
            id=id,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status=resultado.status_code,
            )

        return Response(
            PessoaResponse(resultado).data,
            status=status.HTTP_200_OK,
        )
    
    @swagger_auto_schema(
        operation_summary="Atualizar pessoa apartir de um ID",
        request_body=PessoaUpdatePrivateRequest,
        responses={
            200: PessoaResponse,
            401: openapi.Response("Senha inválida"),
            403: openapi.Response("Sem permissão"),
            404: openapi.Response("Pessoa não encontrada"),
            422: openapi.Response("Dados inválidos"),
        },
        tags=["Pessoas"]
    )

    def put(self, request, id):
        serializer = PessoaUpdatePrivateRequest(
            data = request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        resultado = PessoaService.atualizar(
            usuario_logado=request.user,
            id = id,
            data = serializer.validated_data
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code,
            )

        return Response(
            PessoaResponse(resultado).data,
            status=status.HTTP_200_OK,
        )
    