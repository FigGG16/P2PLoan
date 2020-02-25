from django import forms
from captcha.fields import CaptchaField


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile, Borrower, EmploymentDetail, UsersFamilyAuthentication


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"invalid": u"邮箱填写错误"})
    # captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    userName = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    trueName = forms.CharField(required=True, min_length=2)
    bornDate = forms.DateField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})
    borrowerCheckbox = forms.CharField(required=False)


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class UploadFamilyAuthenticationImageForm(forms.ModelForm):
    class Meta:
        model = UsersFamilyAuthentication
        fields = ['file']

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']



class UserEmploymentDetail(forms.ModelForm):
    class Meta:
        model = EmploymentDetail
        fields = ['employment_state', 'receive_wage', 'company_type', 'working_life', 'working_department',
                  'company_mobile', 'company_name']


class UserFamilyCondition(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['marriage_state', 'dwelling_condition', 'dwelling_mobile', 'dwelling_time', 'is_buy_car']



class UserBasicProfile(forms.ModelForm):
    class Meta:
        model = Borrower
        # fields = ['contact_number', 'qq']
        fields = ['highest_qualification', 'university_name', 'pass_out_year']

