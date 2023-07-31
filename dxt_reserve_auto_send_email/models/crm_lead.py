from odoo import fields, models, api
from jinja2 import Template

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id:
            if self.stage_id.name == 'Reservado':
                print("*"*200)
                print("_onchange_stage_id",self.stage_id.name)
                self.send_email()
                print("*"*200)

    def send_email(self):
        template = self.env.ref('dxt_reserve_auto_send_email.email_template_crm_lead')
        template_values = {
            'object': self,
            'object_name': self.name,
        }
        template_body = template.body_html
        rendered_template_body = Template(template_body).render(template_values)

        mail_obj = self.env['mail.mail']
        email_to = self.partner_id.email
        subject = f"{self.partner_id.name}, finaliza tu inscripción"

        mail_id = mail_obj.create({
            'email_from': self.user_id.email_formatted,
            'email_to': email_to,
            'subject': subject,
            'body_html': rendered_template_body,
        })
        mail_obj.send(mail_id)
        return True

