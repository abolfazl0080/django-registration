# **About Django Registration**
## *Django Registration is a tool for the user registration operation in View*
# **How to use Django Registration**
## *Django Registration has three base classes for register operations*

* **RegistrationView that is base class**

* **RegisterView that is a instance from class RegistrationView for user register**

* **LoginView that is a instance from class RegistrationView for user login**

## **login View**

```python
class Login(LoginView):
    model = User
    form = LoginForm
    template_name = 'your template'
    fields = '__all__'
    success_url = 'redirect after login'
    context = {}
```
### **model** = your user model
### **form** = your form login
### **template_name** = your template name
### **fields** = Required form fields to enter as a list default on '__all__'
### **success_url** = url redirect after login
### **context** = Required fields to send as dict default on {}
