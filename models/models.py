from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, AccessError


class DomainToRestrict(models.Model):
    _name = 'domain.to.restrict'

    name = fields.Char('Domain name', required=True)


class DomainRestriction(models.Model):
    _name = 'domain.restriction'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    domains_ids = fields.Many2many('domain.to.restrict', string='Domains')


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        mail = super(MailMail, self).create(values)
        domain_restriction_obj = self.env['domain.restriction']
        enc = False

        if mail.email_to:
            for domain_restriction in domain_restriction_obj.search([('active', '=', True)]):
                for domain in domain_restriction.domains_ids:
                    if domain.name in mail.email_to:
                        enc = True
                        break

        if mail.recipients_ids:
            print('Send Mail!')

        if enc:
            raise Warning(
                _('The domain of the destination email %s is not included in the list of allowed emails') % mail.email_to)

        return mail
