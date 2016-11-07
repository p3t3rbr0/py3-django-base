import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, HttpResponseNotAllowed
from .models import CustomUser
from .forms import ProfileForm


@csrf_exempt
def save_profile(request):
    '''
    _(Обновление профиля пользователя)
    '''
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"error": "Not authenticated"}))

    if request.is_ajax() and request.method == 'POST':
        user = request.user
        errors = {}
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            info = form.cleaned_data['info']

            if user.email != email:
                try:
                    CustomUser.objects.get(email=email)
                    errors['email'] = 'Данный e-mail уже используется другим пользователем'
                except CustomUser.DoesNotExist:
                    user.email = email
                    user.key = user._gen_hash()
                    user.is_approved = False
                except KeyError:
                    pass

            if user.username != username:
                try:
                    CustomUser.objects.get(username=username)
                    errors['username'] = 'Данное имя пользователя уже используется'
                except CustomUser.DoesNotExist:
                    user.username = username
                    user.key = user._gen_hash()
                    user.is_approved = False
                except KeyError:
                    pass

            user.avatar = form.cleaned_data['avatar']
            user.fname = fname
            user.lname = lname
            user.info = info

            user.save()

            res = {'status': 'ok'}
            if errors:
                res = {'status': 'fail', 'errors': errors}

            return HttpResponse(json.dumps(res))

        else:
            return HttpResponse(json.dumps({"erros": "Form is not valid"}))
    else:
        return HttpResponseNotAllowed()
