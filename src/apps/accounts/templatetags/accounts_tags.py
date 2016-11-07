from django import template
from apps.accounts.forms import LoginForm

register = template.Library()


def login_form(request_path):
    return {"form": LoginForm(), "current_url": request_path}


register.inclusion_tag("units/forms/form_signin.html")(login_form)
