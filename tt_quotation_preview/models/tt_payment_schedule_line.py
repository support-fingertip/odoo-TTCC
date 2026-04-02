from odoo import fields, models


class TTPaymentScheduleLine(models.Model):
    _name = 'tt.payment.schedule.line'
    _description = 'Payment Schedule Line'
    _order = 'sequence, id'

    order_id = fields.Many2one(
        'sale.order', string='Sale Order',
        required=True, ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Description', required=True)
    percentage = fields.Float(string='Percentage (%)')
    amount = fields.Float(string='Amount (INR)')
