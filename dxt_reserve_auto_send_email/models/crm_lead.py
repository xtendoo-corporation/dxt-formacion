from odoo import fields, models, api
from jinja2 import Template
import uuid

class Lead(models.Model):
    _inherit = "crm.lead"

    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()),
                               groups='base.group_system', required=True, readonly=True, copy=False)

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id:
            if self.stage_id.name == 'Reservado':
                print("*"*200)
                print("_onchange_stage_id",self.stage_id.name)
                print("access_token",self.access_token)
                self.send_email()
                print("*"*200)

    def send_email(self):
        template = self.env.ref('dxt_reserve_auto_send_email.email_template_crm_lead')
        self_id = str(self.id)
        partes = self_id.split("_")
        self_id = partes[-1]
        self_id = int(self_id)
        template_values = {
            'object': self,
            'object_name': self.name,
            'object_id': self_id,
            'access_token': self.access_token,
        }
        print("*"*200)
        print("template_values", template_values)
        print("*"*200)
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

    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('dxt_reserve_auto_send_email.portal_my_leads')



