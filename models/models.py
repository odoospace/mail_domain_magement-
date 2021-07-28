from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, AccessError


class DomainToRestrict(models.Model):
    _name = 'domain.to.restrict'

    name = fields.Char('Domain name', required=True)
    active = fields.Boolean('Active', default=True)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        domain_to_restrict_obj = self.env['domain.to.restrict']
        domain_restriction_list = [domain_restriction.name for domain_restriction in
                                   domain_to_restrict_obj.search([('active', '=', True)])]

        if 'email_to' in values and values['email_to']:
            enc = False
            for domain_restriction in domain_restriction_list:
                if domain_restriction in values['email_to']:
                    enc = True
                    break
            if not enc:
                values['email_to'] = ''

        if 'recipient_ids' in values and values['recipient_ids']:
            if isinstance(values['recipient_ids'][0], tuple):
                recipients_list = []
                for recipient_id in values['recipient_ids']:
                    recipient = self.env['res.partner'].browse(recipient_id[1])
                    if recipient.email:
                        for domain_restriction in domain_restriction_list:
                            if domain_restriction in recipient.email:
                                recipients_list.append((4, recipient.id))
                values['recipient_ids'] = recipients_list
            elif isinstance(values['recipient_ids'][0], list):
                recipients_list = []
                for recipient_id in values['recipient_ids'][0][2]:
                    recipient = self.env['res.partner'].browse(recipient_id)
                    if recipient.email:
                        for domain_restriction in domain_restriction_list:
                            if domain_restriction in recipient.email:
                                recipients_list.append(recipient.id)
                values['recipient_ids'] = [[6, 0, recipients_list]]


        return super(MailMail, self).create(values)
