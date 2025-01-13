from fastapi_mail import FastMail, MessageSchema
from jinja2 import Template
from fastapi import BackgroundTasks
from core.config import getEmailConfig

class EmailService:
    def __init__(self):
        self.mail = FastMail(getEmailConfig())

    def sendEmailVerification(self, addressee: str, subject: str, url_code: str, background_tasks: BackgroundTasks):
        try:
            # Leer y renderizar la plantilla Jinja2
            with open('./crosscutting/templates/EmailVerificationTemplate.html', 'r', encoding='utf-8') as file:
                template_content = file.read()
            
            template = Template(template_content)
            rendered_html = template.render(UrlCode=url_code)
            
            message = MessageSchema(
                subject=subject,
                recipients=[addressee],
                body=rendered_html,
                subtype="html"
            )
            
            background_tasks.add_task(self.mail.send_message, message)
            print(f"✅ Email de verificación de email enviado a: {addressee}")
        except Exception as e:
            print(f"❌ Error al enviar el correo a {addressee}: {e}")
            raise Exception(f"Error al enviar el correo: {e}")
        
    def sendPasswordReset(self, addressee: str, subject: str, url_code: str, background_tasks: BackgroundTasks):
        try:
            # Leer y renderizar la plantilla Jinja2
            with open('./crosscutting/templates/PasswordResetCodeTemplate.html', 'r', encoding='utf-8') as file:
                template_content = file.read()
            
            template = Template(template_content)
            rendered_html = template.render(UrlCode=url_code)
            
            message = MessageSchema(
                subject=subject,
                recipients=[addressee],
                body=rendered_html,
                subtype="html"
            )
            
            background_tasks.add_task(self.mail.send_message, message)
            print(f"✅ Email de restablecimiento de contraseña enviado a: {addressee}")
        except Exception as e:
            print(f"❌ Error al enviar el correo a {addressee}: {e}")
            raise Exception(f"Error al enviar el correo: {e}")
