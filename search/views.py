from django.shortcuts import render
from .models import Technology_korea, Technology_other, License_raking
from django.apps import apps


# Create your views here.

def license_info(request):
    license_select = apps.get_model('mypage', 'license_select')
    user = request.user
    license = ''
    if request.method == 'POST':
        try:
            license = request.POST['license_name']
            print('ㅇㅁㄹㄴㅇㄹ' + license)
        except:
            license = request.POST['license_name1']
            print('sdfdsf' + license)
        license = str(license)


    license_summary = Technology_korea.objects.filter(license=license)

    if len(license_summary) == 0:
        license_summary = Technology_other.objects.filter(license=license)



    license_summary = license_summary[0]
    if license_select.objects.filter(user_id=user, license=license).exists():
        user_license = True
    else:
        user_license = False

    summary = license_summary.summary
    summary = summary.split('\n')

    params = {'license': license,
              'license_summary': license_summary,
              'user_license': user_license,
              'summary': summary}
    return render(request, 'search/license_info.html', params)
