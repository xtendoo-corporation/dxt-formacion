# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
import datetime

class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/leads/<int:lead_id>/accept_tutor'], type='json', auth="public", website=True)
    def portal_tutor_signature(self, lead_id, access_token=None, name=None, signature=None):
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            lead_sudo = self._document_check_access('crm.lead', lead_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid lead.')}

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            lead_sudo.write({
                'tutor_signed_by': name,
                'tutor_signed_on': fields.Datetime.now(),
                'tutor_signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}
        url = '/my/leads/%s?access_token=%s' % (lead_id, access_token)
        return {
            'force_refresh': True,
            'redirect_url': url,
        }

    @http.route(['/my/leads/<int:lead_id>/accept_student'], type='json', auth="public", website=True)
    def portal_student_signature(self, lead_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            lead_sudo = self._document_check_access('crm.lead', lead_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid lead.')}

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            lead_sudo.write({
                'student_signed_by': name,
                'student_signed_on': fields.Datetime.now(),
                'student_signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}
        url = '/my/leads/%s?access_token=%s' % (lead_id, access_token)
        return {
            'force_refresh': True,
            'redirect_url': url,
        }

    @http.route(['/form/leads/<int:lead_id>'], type='http', auth="public", website=True)
    def portal_lead_form(self, lead_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            lead_sudo = self._document_check_access('crm.lead', lead_id, access_token=access_token)
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
            'action': lead_sudo._get_portal_form_return_action(),
            'access_token': access_token,

        }
        return request.render('dxt_reserve_auto_send_email.portal_my_leads_form', values)

    @http.route(['/my/leads/<int:lead_id>'], type='http', auth="public", website=True)
    def portal_lead_page(self, lead_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
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
        return request.render('dxt_reserve_auto_send_email.lead_confirm_data_template', values)

    # @http.route('/my/leads/confirm', type='http', auth="public", website=True)
    # def lead_confirm(self, redirect=None, **post):
    #     print("*"*100)
    #     lead = post.get('lead')
    #     access_token = post.get('access_token')
    #     partner_name = post.get('name')
    #     partner = request.env['res.partner'].sudo().search([
    #         ('name', '=', partner_name),
    #     ])
    #     date_birth = post.get('date_birth')
    #     # if date_birth:
    #     #     date_birth = date_birth.replace("/", "")
    #     #     date_birth = datetime.datetime.strptime(date_birth, '%d%m%Y').date()
    #     if post.get('country_id'):
    #         country = request.env['res.country'].sudo().browse(post.get('country_id'))
    #         if not country:
    #             country = ""
    #     if post.get('state_id'):
    #         state = request.env['res.country.state'].sudo().browse(post.get('state_id'))
    #         if not state:
    #             state = ""
    #     if not partner:
    #         print("NO PARTNER")
    #         partner = request.env['res.partner'].with_context(no_vat_validation=True).sudo().create(
    #             {
    #                 'name': partner_name,
    #                 'email': post.get('email'),
    #                 'phone': post.get('phone'),
    #                 # 'country_id': country.id,
    #                 'street': post.get('street'),
    #                 # 'state_id': state.id,
    #                 'city': post.get('city'),
    #                 'zip': post.get('zip'),
    #                 'is_student': True,
    #                 'date_birth': date_birth,
    #                 'vat': post.get('vat'),
    #             }
    #         )
    #     else:
    #         print("PARTNER")
    #         partner = partner[0]
    #         partner = partner.with_context(no_vat_validation=True)
    #         # partner.sudo().write(
    #         #     {
    #         #         'name': partner_name,
    #         #         'email': post.get('email'),
    #         #         'phone': post.get('phone'),
    #         #         # 'country_id': country.id,
    #         #         'street': post.get('street'),
    #         #         # 'state_id': state.id,
    #         #         'city': post.get('city'),
    #         #         'zip': post.get('zip'),
    #         #         'is_student': True,
    #         #         'date_birth': date_birth,
    #         #         'vat': post.get('vat')
    #         #     }
    #         # )
    #     print("lead: ", post.get('lead'))
    #     print("access_token: ", access_token)
    #     try:
    #         lead_sudo = self._document_check_access('crm.lead', int(lead), access_token=access_token)
    #         print("lead_sudo", lead_sudo)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #
    #     # lead_to_write = request.env['crm.lead'].sudo().search([
    #     #     ('id', '=', post.get('lead')),
    #     # ])
    #     # lead_to_write = lead_to_write[0]
    #     # lead_to_write = lead_to_write.with_context(no_tracking=True)
    #     # lead_to_write.sudo().write(
    #     #     {
    #     #         'partner_id': partner.id,
    #     #     }
    #     # )
    #     # values = {
    #     #     'lead': lead_sudo,
    #     #     'message': None,
    #     #     'token': access_token,
    #     #     'bootstrap_formatting': True,
    #     #     'partner_id': SUPERUSER_ID,
    #     #     'report_type': 'html',
    #     #     'action': lead_sudo._get_portal_return_action(),
    #     #
    #     # }
    #     values = {
    #         'lead_id': lead_sudo,
    #         'message': None,
    #         'access_token': access_token,
    #         'bootstrap_formatting': True,
    #         'partner_id': SUPERUSER_ID,
    #         'report_type': 'html',
    #         'action': lead_sudo._get_portal_return_action(),
    #
    #     }
    #     values.update({
    #         'has_check_vat': False,
    #         'redirect': lead_sudo._get_data_update_form_url(lead_sudo, access_token),
    #         'page_name': 'my_lead',
    #     })
    #
    #     response = request.render("dxt_reserve_auto_send_email.lead_confirm_data_template", values)
    #     response.headers['X-Frame-Options'] = 'DENY'
    #     print(values)
    #     print("*"*100)
    #     # return response
    #     return self.portal_lead_page(lead, access_token=access_token)
        # redirect_url = '/my/leads/%s?access_token=%s' % (lead, access_token)
        # return {
        #     'force_refresh': True,
        #     'redirect_url': redirect_url,
        # }
        # return request.redirect(redirect_url)

    @route(['/my/leads/confirm'], type='http', auth='public', website=True)
    def lead_confirm(self, **post):
        print("*"*100)
        print("post", post)
        lead = post.get('lead')
        access_token = post.get('access_token')
        print("lead: ",lead)
        print("access_token:", access_token)
        try:
            lead_sudo = self._document_check_access('crm.lead', int(lead), access_token=access_token)
            print("lead_sudo", lead_sudo)
        except (AccessError, MissingError):
            print("AccessError")
            return request.redirect('/my')
        if lead_sudo:
            print("lead_sudo", lead_sudo)
            partner_name = post.get('name')
            partner = request.env['res.partner'].sudo().search([
                ('name', '=', partner_name),
            ])
            # date_birth = post.get('date_birth')
            print("lead: ", lead_sudo)
            print("partner_name", partner_name)
            print("partner", partner)
            values = {
                'lead': lead_sudo,
                'message': False,
                'token': access_token,
                'bootstrap_formatting': True,
                'partner_id': SUPERUSER_ID,
                'report_type': 'html',
                'action': lead_sudo._get_portal_return_action(),

            }
            print("values: ", values)
            response = request.render("dxt_reserve_auto_send_email.lead_confirm_data_template", values)
            response.headers['X-Frame-Options'] = 'DENY'
            print("response; ", response)
            redirect_url = '/my/leads/%s?access_token=%s' % (lead_sudo.id, access_token)
            return request.redirect(redirect_url)
            # return response
            # return self.portal_lead_page(lead_sudo.id, access_token=access_token, message=False)
            # return request.redirect(self.portal_lead_page(self, lead_sudo.id, access_token=access_token, message=False))
            # return request.render('dxt_reserve_auto_send_email.lead_confirm_data_template', values)

        # values = self._prepare_portal_layout_values()
        # partner = SUPERUSER_ID
        # partner = request.env['res.partner'].sudo().search([
        #     ('id', '=', 1),
        # ])
        # values ={
        #     'error': {},
        #     'error_message': [],
        # }
        # print("values 1: ", values)
        # if post and request.httprequest.method == 'POST':
        #     # error, error_message = self.details_form_validate(post)
        #     # values.update({'error': error, 'error_message': error_message})
        #     values.update(post)
        #     lead = post.get('lead')
        #     access_token = post.get('access_token')
        #     try:
        #         lead_sudo = self._document_check_access('crm.lead', int(lead), access_token=access_token)
        #         print("lead_sudo", lead_sudo)
        #         values.update({'lead': lead_sudo})
        #         redirect = lead_sudo._get_data_update_form_url(lead_sudo, access_token)
        #     except (AccessError, MissingError):
        #         return request.redirect('/my')
        #
        #     # if not error:
        #     #     values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
        #     #     values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
        #     #     for field in set(['country_id', 'state_id']) & set(values.keys()):
        #     #         try:
        #     #             values[field] = int(values[field])
        #     #         except:
        #     #             values[field] = False
        #     #     values.update({'zip': values.pop('zipcode', '')})
        #         # partner.sudo().write(values)
        #         # if redirect:
        #         #     return request.redirect(redirect)
        #         # return request.redirect('/my/home')
        # print("values 2: ", values)
        # # countries = request.env['res.country'].sudo().search([])
        # # states = request.env['res.country.state'].sudo().search([])
        # values.update({
        #     'partner': partner,
        #     # 'countries': countries,
        #     # 'states': states,
        #     'has_check_vat':False,
        #     'redirect': redirect,
        #     'page_name': 'my_lead',
        #     'message': False,
        #     'token': access_token,
        #     'bootstrap_formatting': True,
        #     'partner_id': SUPERUSER_ID,
        #     'report_type': 'html',
        #     'action': lead_sudo._get_portal_return_action(),
        # })
        # print("values 3: ", values)
        # response = request.render("dxt_reserve_auto_send_email.lead_confirm_data_template", values,headers={ 'X-Frame-Options': 'DENY'})
        # print("response: ", response)
        # print("*"*100)
        # return request.redirect(redirect)
        # return response
        # return request.render("dxt_reserve_auto_send_email.lead_confirm_data_template", values)
