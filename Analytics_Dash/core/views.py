from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.models import User
import uuid
from core.models import Apps, AppInstalls, UserRole
from core.serializers import AppInstallsSerializer
def index(request):
    print(request.user.username)
    print(request.headers)
    apps = Apps.objects.all()    
    return render(request, 'index.html', {'apps':apps})

def logout_request(request):
    logout(request)
    return redirect(index)

def login_request(request):

    if request.method=='POST':
        form=AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse('User Error try again')
        else:
            return HttpResponse('invalid username or password')
    
    form=AuthenticationForm()
    return render(request,"login.html",{"form":form})


def google_login_callback(request):
    state=request.GET.get('state')
    code = request.GET.get('code')
    scope = request.GET.get('scope')
    auth_user = request.GET.get('authuser')
    consent=request.GET.get('consent')
    print(state)
    print(code)
    print(scope)
    print(auth_user)
    print(consent)
    return HttpResponse('google login callback')


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        password = request.POST.get('password')
        email = request.POST.get('email')
        custom_username = email.split('@')[0] + '_' + uuid.uuid4().hex[:6]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )        
        return render(request, 'signup.html')


class AdminView(View):
    def get(self, request):
        _admin = request.user
        user = UserRole.objects.get(user=_admin)
        if user.role !='manager':
            return HttpResponse('You are not authorized to access this page')
        users=User.objects.all().select_related('userrole')
        
        return render(request, 'admin_page.html', {'users': users})
    def post(self, request):
        user_id = request.POST.get('user_id')
        user=User.objects.get(id=user_id)
        try:
            user_role = UserRole.objects.get(user=user)
            user_role.role = 'manager'
            user_role.save()
        except UserRole.DoesNotExist:
            user_role = UserRole.objects.create(user=user, role='manager')
        return redirect('/admin-page/')

    # def post(self, request):
    #     return render(request, 'admin.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 1000

    def paginate(self, object_list, page, limit, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        
        # if objects.has_next() and objects.has_previous():
        data = {
                'next_page': objects.has_next() and objects.next_page_number() or None,
                'data': list(objects)
            }
        return data

from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class GetAllInstalls(ViewPaginatorMixin, View):  
    def get(self,request):
        date1=request.GET.get("date1")
        date2=request.GET.get("date2")
        query=request.GET.get("search")
        if date1 is not None and date2 is not None:
            date1 = datetime.strptime(date1, '%Y-%m-%d')
            date2 = datetime.strptime(date2, '%Y-%m-%d')
        page_no=request.GET.get('page')
        if not query:
            if date1 and date2:
                installs = AppInstalls.objects.filter(idate__range=(date1, date2))
            else:
                installs = AppInstalls.objects.all()
        else:
            installs = AppInstalls.objects.filter(name__ilike=query)
        
        data=AppInstallsSerializer(installs,many=True)

        return JsonResponse({'data': self.paginate(data.data, page_no, 50)})

def view_installs(request):
    return render(request, 'view_installs.html')
    