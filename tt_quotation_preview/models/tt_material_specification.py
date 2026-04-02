from odoo import fields, models


class TTMaterialSpecification(models.Model):
    _name = 'tt.material.specification'
    _description = 'Product and Material Specification'
    _order = 'sequence, id'

    order_id = fields.Many2one(
        'sale.order', string='Sale Order',
        required=True, ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Specification', required=True)
    value = fields.Text(string='Details')
