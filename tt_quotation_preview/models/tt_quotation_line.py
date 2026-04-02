from odoo import api, fields, models


class TTQuotationLine(models.Model):
    _name = 'tt.quotation.line'
    _description = 'Quotation Line Item'
    _order = 'sequence, id'

    category_id = fields.Many2one(
        'tt.quotation.category', string='Category',
        required=True, ondelete='cascade',
    )
    order_id = fields.Many2one(
        related='category_id.order_id',
        string='Sale Order',
        store=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)
    category_name = fields.Char(string='Category')
    subcategory = fields.Char(string='Subcategory')
    service_item = fields.Text(string='Service Item')
    item_name = fields.Char(string='Item Name')
    quantity = fields.Float(string='Qty', default=1.0)
    unit = fields.Char(string='Unit', default='Nos')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(
        string='Amount',
        compute='_compute_amount',
        store=True,
    )

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price
