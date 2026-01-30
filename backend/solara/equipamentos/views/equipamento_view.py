from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from equipamentos.serializers import (
    EquipamentoRequest,
    EquipamentoResponse
)
from equipamentos.services import EquipamentoService

from core.error import Erro

class EquipamentoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Cadastra um equipamento",
        request_body = EquipamentoRequest,
        responses={
            201: EquipamentoResponse,
            400: openapi.Response("Erro de validação"),
            401: openapi.Response("Não autenticado"),
            403: openapi.Response("Sem permissão"),
            409: openapi.Response("Conflito"),
        },
        tags=["Equipamento"]
    )
    
    def post(self, request):
        serializer = EquipamentoRequest(data = request.data)
        serializer.is_valid(raise_exception = True)

        resultado = EquipamentoService.criar(
            usuario_logado = request.user,
            data = serializer.validated_data
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status = resultado.status_code
            )

        response_serializer = EquipamentoResponse(resultado)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    

    @swagger_auto_schema(
        operation_summary="Listar equipamentos",
        manual_parameters=[
            openapi.Parameter(
                "fabricante",
                openapi.IN_QUERY,
                description="Filtrar por fabricante",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "tipo_equipamento",
                openapi.IN_QUERY,
                description="Tipo do equipamento",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "potencia_min",
                openapi.IN_QUERY,
                description="Potência mínima (W)",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "potencia_max",
                openapi.IN_QUERY,
                description="Potência máxima (W)",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "tensao",
                openapi.IN_QUERY,
                description="Tensão do equipamento",
                type=openapi.TYPE_NUMBER,
            ),
        ],
        responses={
            200: EquipamentoResponse(many=True),
            403: openapi.Response("Sem permissão"),
        },
        tags=["Equipamentos"],
    )
    def get(self, request):
        filtros = {
            "fabricante": request.query_params.get("fabricante"),
            "tipo_equipamento": request.query_params.get("tipo_equipamento"),
            "potencia_min": request.query_params.get("potencia_min"),
            "potencia_max": request.query_params.get("potencia_max"),
            "tensao": request.query_params.get("tensao"),
        }

        resultado = EquipamentoService.listar(
            usuario_logado=request.user,
            filtros=filtros,
        )

        if isinstance(resultado, Erro):
            return Response(
                resultado.to_response(),
                status=resultado.status_code,
            )

        return Response(
            EquipamentoResponse(resultado, many=True).data,
            status=status.HTTP_200_OK,
        )