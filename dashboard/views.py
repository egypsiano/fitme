from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import UserHealthData # Assuming UserHealthData is in users.models
import json # For passing data to Chart.js

@login_required
def dashboard_view(request):
    user = request.user

    # Get latest health metrics
    latest_health_data = UserHealthData.objects.filter(user=user).order_by('-date').first()

    # Get all health data for graphs, ensuring consistent ordering
    historical_health_data = UserHealthData.objects.filter(user=user).order_by('date')

    # Prepare data for Chart.js
    # We need labels (dates) and data points (e.g., weight)
    chart_labels = []
    chart_weight_data = []
    # Potentially other metrics like BMI, calorie target if we want more graphs
    # chart_bmi_data = []

    for entry in historical_health_data:
        chart_labels.append(entry.date.strftime('%Y-%m-%d')) # Format date as string
        chart_weight_data.append(float(entry.weight_kg) if entry.weight_kg is not None else None) # Handle potential None
        # chart_bmi_data.append(float(entry.bmi) if entry.bmi is not None else None)

    context = {
        'user': user,
        'latest_health_data': latest_health_data,
        'historical_health_data_count': historical_health_data.count(), # For conditional display
        'chart_labels': json.dumps(chart_labels),
        'chart_weight_data': json.dumps(chart_weight_data),
        # 'chart_bmi_data': json.dumps(chart_bmi_data),
    }
    return render(request, 'dashboard/dashboard.html', context)
