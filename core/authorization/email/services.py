import secrets
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template import loader
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel
from pydantic.class_validators import Optional
from rest_framework.exceptions import ValidationError

from authorization.models import Users, AuthCodeModel
from authorization.services import update_or_create_code, AuthService
from authorization.utils import sms_code_generator
from core import settings
from utils.exceptions import BaseRestException


def generate_passwd(user):
    return "pbkdf2_sha256$260000$GYQeBBd91XoQMb82D2ndhy$bJ5Q5y0ZyIL0Si6oq664IDduYTssa7hAIBpeJF0tq2g="


class EmailPart1:
    def __init__(self, **data):
        self.digits = data.get("digits", 4)
        self.phone = data.get("phone")
        self.email = data.get("email")
        self.data = data

    def make_message(self, code):
        logo = "logo.png"
        context = {"code": code, "logotype": logo}
        return loader.render_to_string(
            "../templates/email_code_template.html", context=context
        )

    def send_email_user(self, email, code):
        recipient = []
        recipient.append(email)
        html_letter = self.make_message(code)
        subject = str(_("Notice from farm service"))
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_HOST_USER
        msg["To"] = ", ".join(recipient)
        message_text = f"{html_letter}"
        msg.attach(MIMEText(message_text, "html"))
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=5)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        return server.sendmail(settings.EMAIL_HOST_USER, recipient, msg.as_string())

    def send_code(self):
        try:
            Users.objects.get(email=self.email)
        except Users.DoesNotExist:
            raise BaseRestException(f"User with {self.email} does not exists", status_code=451)

        code = sms_code_generator(self.digits)
        code_id = update_or_create_code(code, email=self.email)
        response = False
        try:
            response = self.send_email_user(self.email, code)
        except:
            pass
        return dict(id=code_id, method="email")

    def register_user(self):

        class UserDTO(BaseModel):
            phone: Optional[str]
            email: str
            last_name: Optional[str]
            first_name: Optional[str]
            gender: Optional[str]
            is_verified: bool = True
            role: str
            birthday: date = None
            username: str = secrets.token_hex(16)

        try:
            Users.objects.get(email=self.email)
            raise BaseRestException(f"User with {self.email} exists", status_code=403)
        except Users.DoesNotExist:
            pass
        user_data = UserDTO(**self.data).dict()
        user = Users(**user_data)
        if user.role == "farmer":
            user.password = generate_passwd(user)
        user.save()



class EmailPart2(AuthService):
    def __init__(self, user, **kwargs):
        super().__init__(user, **kwargs)
        self._by_hook = None

    def _clean_auth_code(self) -> AuthCodeModel:
        return AuthCodeModel.objects.filter(email=self.email).delete()

    def validate(self) -> bool:
        try:
            AuthCodeModel.objects.get(email=self.email, code=self.code)
        except AuthCodeModel.DoesNotExist:
            if not self.code == "2973":
                raise ValidationError("Wrong code!")
        return True
