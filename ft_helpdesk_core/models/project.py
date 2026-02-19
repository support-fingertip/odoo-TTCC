from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        related='partner_id',
        store=True,
    )
