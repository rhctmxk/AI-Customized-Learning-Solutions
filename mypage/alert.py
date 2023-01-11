from django.apps import apps

def message_processor(request):
    if request.user.is_authenticated:
        user = request.user
        Alert = apps.get_model('mypage', 'Alert')
        alerts = Alert.objects.filter(user=user, activate=1)
        alert_count = len(alerts)
    else:
        alert_count = None
        alerts = None
    params = {'alert_count': alert_count,
              'alerts': alerts}
    return params