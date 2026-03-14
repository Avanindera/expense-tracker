from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction, MerchantCategoryMap


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request):

    user = request.user

    amount = request.data.get('amount')
    receiver_name = request.data.get('receiver_name')
    category = request.data.get('category')
    date = request.data.get('date')
    time = request.data.get('time')

    Transaction.objects.create(
        user=user,
        amount=amount,
        receiver_name=receiver_name,
        category=category,
        date=date,
        time=time
    )

    # mapping save / update
    MerchantCategoryMap.objects.update_or_create(
        user=user,
        receiver_name=receiver_name,
        defaults={'category': category}
    )

    return Response({"message": "Transaction added"})