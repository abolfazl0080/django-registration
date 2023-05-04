from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View


class RegistrationView(View):
    model = None
    form = None
    template_name = None
    fields = '__all__'
    success_url = None
    context = {}

    def check_query_post(self, fields):
        return []

    def after_check_post(self, fields):
        return None

    def get(self, request):
        self.context['form'] = self.form
        return render(request, self.template_name, self.context)

    def post(self, request):
        object_form = self.form(request.POST)
        if object_form.is_valid():
            fields_registration = {}
            if self.fields == '__all__':
                self.fields = []
                for field in self.form.__dict__['declared_fields'] or self.form.__dict__['base_fields']:
                    self.fields.append(field)
            for field in self.fields:
                fields_registration[field] = object_form.cleaned_data.get(field)
            try:
                query_post = self.check_query_post(fields_registration)
            except:
                raise Http404
            if query_post:
                if query_post[1] == 'Http404':
                    raise Http404
                else:
                    object_form.add_error(query_post[0], query_post[1])
                    self.context['form'] = object_form
                    return render(request, self.template_name, self.context)
            self.after_check_post(fields_registration)
            return redirect(self.success_url)
        else:
            self.context['form'] = object_form
            return render(request, self.template_name, self.context)


class RegisterView(RegistrationView):
    unique_fields = []

    def check_query_post(self, fields):
        user = self.model.objects.filter(username=fields['username']).first()
        if user is not None:
            return ['username', 'This username has already been created']
        if not fields['password'] == fields['password_confirm']:
            return ['password', 'Password is not the same as confirm password']
        for field in self.unique_fields:
            query = {field: fields[field]}
            user = self.model.objects.filter(**query).first()
            if user is not None:
                if type(self.unique_fields) is list:
                    return [field, 'A field with this name has already been registered']
                else:
                    return [field, self.unique_fields[field]]
        return []

    def after_check_post(self, fields):
        new_user = self.model()
        for field in fields:
            if field in self.model.__dict__:
                if field == 'password':
                    new_user.set_password(fields[field])
                else:
                    new_user.__dict__[field] = fields[field]
        new_user.save()


class LoginView(RegistrationView):
    def check_query_post(self, fields):
        for field in fields:
            if field in self.model.__dict__:
                if not field == 'password':
                    for user in self.model.objects.all():
                        if user.__dict__[field] == fields[field]:
                            if not user.check_password(fields['password']):
                                return [field, 'The username or password is incorrect']
                            return []
        return ['password', 'The username or password is incorrect']

    def after_check_post(self, fields):
        for field in fields:
            if field in self.model.__dict__:
                if not field == 'password':
                    for user in self.model.objects.all():
                        if user.__dict__[field] == fields[field]:
                            login(self.request, user)

