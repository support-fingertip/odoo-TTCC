from odoo import api, fields, models


class TTQuotationCategory(models.Model):
    _name = 'tt.quotation.category'
    _description = 'Quotation Category'
    _order = 'sequence, id'

    order_id = fields.Many2one(
        'sale.order', string='Sale Order',
        required=True, ondelete='cascade',
    )
    name = fields.Char(string='Category Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    line_ids = fields.One2many(
        'tt.quotation.line', 'category_id',
        string='Quotation Lines',
    )

    # --- Computed Totals ---
    subtotal = fields.Float(
        string='Total',
        compute='_compute_totals',
        store=True,
    )
    gst_amount = fields.Float(
        string='GST (18%)',
        compute='_compute_totals',
        store=True,
    )
    grand_total = fields.Float(
        string='Grand Total',
        compute='_compute_totals',
        store=True,
    )

    @api.depends('line_ids.amount')
    def _compute_totals(self):
        for category in self:
            subtotal = sum(category.line_ids.mapped('amount'))
            gst = subtotal * 0.18
            category.subtotal = subtotal
            category.gst_amount = gst
            category.grand_total = subtotal + gst
