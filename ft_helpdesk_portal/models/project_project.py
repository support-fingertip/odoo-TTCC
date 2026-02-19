from odoo import models, fields


class ProjectProject(models.Model):
    """Adds customer_id as an alias for partner_id on project.project.

    Odoo 18 renamed the customer field from customer_id to partner_id on
    project.project.  Any IR record rules that were written against the old
    field name will raise a ValueError in the new _anyfy_leaves / expression
    optimisation layer when portal users trigger a project.task search_count.

    Exposing customer_id as a stored related field makes those rules resolve
    correctly without requiring a database-level migration of the rules
    themselves.
    """

    _inherit = 'project.project'

    customer_id = fields.Many2one(
        'res.partner',
        related='partner_id',
        string='Customer',
        store=True,
    )
