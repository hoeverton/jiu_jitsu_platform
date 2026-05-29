import mercadopago
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from agendamentos.models import Agendamento
from .models import Pagamento

class CriarPixView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        agendamento_id = request.data.get('agendamento_id')

        agendamento = Agendamento.objects.get(
            id=agendamento_id
        )

        sdk = mercadopago.SDK(
            settings.MP_ACCESS_TOKEN
        )

        payment_data = {
            "transaction_amount": 50.00,
            "description": f"Aula #{agendamento.id}",
            "payment_method_id": "pix",
            "payer": {
                "email": request.user.email
            }
        }

        payment_response = sdk.payment().create(
            payment_data
        )
        print(payment_response)

        """payment = payment_response["response"]

        return Response({
            "pix_id": payment["id"],
            "status": payment["status"],
            "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        })"""

        