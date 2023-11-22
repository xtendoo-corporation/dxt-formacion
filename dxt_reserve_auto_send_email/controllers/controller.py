# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager

class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/leads/<int:lead_id>'], type='http', auth="public", website=True)
    def portal_lead_page(self, lead_id, report_type=None, access_token=None, message=False, download=False, **kw):
        print("/"*50)
        print("access_token", access_token)
        try:
            # lead_sudo = self._document_check_access('crm.lead', lead_id, access_token=access_token)
            lead_sudo = self._document_check_access('crm.lead', lead_id, access_token=access_token)
            print("lead_sudo", lead_sudo)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if lead_sudo:
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_lead_%s' % lead_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_lead_%s' % lead_sudo.id] = now
                body = _('Lead viewed by customer %s',
                         lead_sudo.partner_id.name if request.env.user._is_public() else request.env.user.partner_id.name)
                _message_post_helper(
                    "crm.lead",
                    lead_sudo.id,
                    body,
                    token=lead_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=lead_sudo.user_id.sudo().partner_id.ids,
                )

        values = {
            'lead': lead_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': SUPERUSER_ID,
            'report_type': 'html',
            'action': lead_sudo._get_portal_return_action(),

        }
        print("values", values)
        print("/"*50)
        return request.render('dxt_reserve_auto_send_email.portal_my_leads', values)

    # @http.route(['/my/orders/<int:order_id>/decline'], type='http', auth="public", methods=['POST'], website=True)
    # def decline(self, order_id, access_token=None, **post):
    #     try:
    #         order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #
    #     message = post.get('decline_message')
    #
    #     query_string = False
    #     if order_sudo.has_to_be_signed() and message:
    #         order_sudo.action_cancel()
    #         _message_post_helper('sale.order', order_id, message, **{'token': access_token} if access_token else {})
    #     else:
    #         query_string = "&message=cant_reject"
    #
    #     return request.redirect(order_sudo.get_portal_url(query_string=query_string))
    @http.route('/my/leads/confirm', auth='public', website=True)
    def lead_confirm(self, **post):
        print("*"*100)
        print("post", post)
        print("*"*100)
        return request.render('dxt_reserve_auto_send_email.lead_confirm_template', {})

    # @http.route('/my/leads/confirm', auth='public', website=True)
    # def lead_confirm(self, **post):
    #     print("*"*100)
    #     print("**post", **post)
    #     print("*"*100)
    #     # # get from query string if not on json param
    #     # access_token = access_token or request.httprequest.args.get('access_token')
    #     # try:
    #     #     order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
    #     # except (AccessError, MissingError):
    #     #     return {'error': _('Invalid order.')}
    #     #
    #     # if not order_sudo.has_to_be_signed():
    #     #     return {'error': _('The order is not in a state requiring customer signature.')}
    #     # if not signature:
    #     #     return {'error': _('Signature is missing.')}
    #     #
    #     # try:
    #     #     order_sudo.write({
    #     #         'signed_by': name,
    #     #         'signed_on': fields.Datetime.now(),
    #     #         'signature': signature,
    #     #     })
    #     #     request.env.cr.commit()
    #     # except (TypeError, binascii.Error) as e:
    #     #     return {'error': _('Invalid signature data.')}
    #     #
    #     # if not order_sudo.has_to_be_paid():
    #     #     order_sudo.action_confirm()
    #     #     order_sudo._send_order_confirmation_mail()
    #     #
    #     # pdf = request.env.ref('sale.action_report_saleorder').with_user(SUPERUSER_ID)._render_qweb_pdf([order_sudo.id])[
    #     #     0]
    #     #
    #     # _message_post_helper(
    #     #     'sale.order', order_sudo.id, _('Order signed by %s') % (name,),
    #     #     attachments=[('%s.pdf' % order_sudo.name, pdf)],
    #     #     **({'token': access_token} if access_token else {}))
    #     #
    #     # query_string = '&message=sign_ok'
    #     # if order_sudo.has_to_be_paid(True):
    #     #     query_string += '#allow_payment=yes'
    #     return {
    #         'force_refresh': True,
    #         'redirect_url': 'http:/localhost:15069/contactus-thank-you',
    #     }
