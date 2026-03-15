from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction, MerchantCategoryMap
from rest_framework.decorators import permission_classes
from django.db.models import Sum

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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):

    user = request.user

    transactions = Transaction.objects.filter(user=user).order_by('-date', '-time')

    data = []

    for t in transactions:
        data.append({
            "amount": str(t.amount),
            "receiver_name": t.receiver_name,
            "category": t.category,
            "date": t.date,
            "time": t.time
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_summary(request):

    user = request.user

    summary = (
        Transaction.objects
        .filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
    )

    data = []

    for item in summary:
        data.append({
            "category": item['category'],
            "total_amount": str(item['total'])
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filtered_transactions(request):

    user = request.user

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    transactions = Transaction.objects.filter(user=user)

    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    data = []

    for t in transactions:
        data.append({
            "amount": str(t.amount),
            "receiver_name": t.receiver_name,
            "category": t.category,
            "date": t.date,
            "time": t.time
        })

    return Response(data)