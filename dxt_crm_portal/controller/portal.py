# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class PortalCRM(CustomerPortal):

    def _prepare_my_leads_values(self, page, domain=None, url="/my/leads"):
        values = self._prepare_portal_layout_values()
        CRMLeads = request.env['crm.lead']

        domain = expression.AND([
            domain or [],
            self._get_leads_domain(),
        ])

        print("****domain: ", domain)
        for lead in CRMLeads.search(domain):
            print("****lead: ", lead)

        values.update({
            'leads': lambda pager_offset: (
                CRMLeads.search(domain, limit=self._items_per_page, offset=pager_offset)
                if CRMLeads.check_access_rights('read', raise_exception=False) else CRMLeads
            ),
            'page_name': 'lead',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {},
                "total": CRMLeads.search_count(domain) if CRMLeads.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
        })

        print("****values: ", values)

        return values

    @http.route(['/my/leads', '/my/leads/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_crm(self, page=1, **kw):
        values = self._prepare_my_leads_values(page)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        leads = values['leads'](pager['offset'])

        values.update({
            'leads': leads,
            'pager': pager,
        })
        return request.render("dxt_crm_portal.portal_my_leads", values)

    def _get_leads_domain(self):
        return [('active', '=', True)]


    # @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    # def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
    #     try:
    #         invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #
    #     if report_type in ('html', 'pdf', 'text'):
    #         return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)
    #
    #     values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
    #     return request.render("account.portal_invoice_page", values)

    # ------------------------------------------------------------
    # My Home
    # ------------------------------------------------------------

    # def details_form_validate(self, data, partner_creation=False):
    #     error, error_message = super(PortalAccount, self).details_form_validate(data)
    #     # prevent VAT/name change if invoices exist
    #     partner = request.env['res.users'].browse(request.uid).partner_id
    #     # Skip this test if we're creating a new partner as we won't ever block him from filling values.
    #     if not partner_creation and not partner.can_edit_vat():
    #         if 'vat' in data and (data['vat'] or False) != (partner.vat or False):
    #             error['vat'] = 'error'
    #             error_message.append(_('Changing VAT number is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #         if 'name' in data and (data['name'] or False) != (partner.name or False):
    #             error['name'] = 'error'
    #             error_message.append(_('Changing your name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #         if 'company_name' in data and (data['company_name'] or False) != (partner.company_name or False):
    #             error['company_name'] = 'error'
    #             error_message.append(_('Changing your company name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #     return error, error_message
    #
    # def extra_details_form_validate(self, data, additional_required_fields, error, error_message):
    #     """ Ensure that all additional required fields have a value in the data """
    #     for field in additional_required_fields:
    #         if field.name not in data or not data[field.name]:
    #             error[field.name] = 'error'
    #             error_message.append(_('The field %s must be filled.', field.field_description.lower()))
    #     return error, error_message
