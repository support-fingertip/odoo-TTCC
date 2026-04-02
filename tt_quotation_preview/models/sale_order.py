from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --- Custom Quotation Fields ---
    tt_category_ids = fields.One2many(
        'tt.quotation.category', 'order_id',
        string='Quotation Categories',
    )
    tt_payment_schedule_ids = fields.One2many(
        'tt.payment.schedule.line', 'order_id',
        string='Payment Schedule',
    )
    tt_material_spec_ids = fields.One2many(
        'tt.material.specification', 'order_id',
        string='Material Specifications',
    )

    # --- Charges ---
    tt_floor_protection = fields.Float(
        string='Floor Protection (per sqft)',
        default=0.0,
    )

    # --- Computed Totals ---
    tt_categories_total = fields.Float(
        string='Categories Total',
        compute='_compute_tt_totals',
        store=True,
    )
    tt_platform_fee = fields.Float(
        string='Platform Fee (7%)',
        compute='_compute_tt_totals',
        store=True,
    )
    tt_grand_total = fields.Float(
        string='Grand Total',
        compute='_compute_tt_totals',
        store=True,
    )

    @api.depends(
        'tt_category_ids.grand_total',
        'tt_floor_protection',
    )
    def _compute_tt_totals(self):
        for order in self:
            categories_total = sum(order.tt_category_ids.mapped('grand_total'))
            subtotal_before_fee = categories_total + order.tt_floor_protection
            platform_fee = subtotal_before_fee * 0.07
            order.tt_categories_total = categories_total
            order.tt_platform_fee = platform_fee
            order.tt_grand_total = subtotal_before_fee + platform_fee

    def action_generate_payment_schedule(self):
        """Generate fixed payment schedule lines (10%, 25%, 25%, 40%)."""
        schedule_data = [
            (10, 'Booking advance'),
            (25, 'After material finalisation and 3D design finalisation (before masking)'),
            (25, 'After masking and the final quotation is shared (During Design Sign-Off)'),
            (40, 'During carcass delivery (Before Installation of Modular Works)'),
        ]
        for order in self:
            order.tt_payment_schedule_ids.unlink()
            for percentage, description in schedule_data:
                amount = order.tt_grand_total * (percentage / 100.0)
                self.env['tt.payment.schedule.line'].create({
                    'order_id': order.id,
                    'name': f"{percentage}% - {description}",
                    'percentage': percentage,
                    'amount': amount,
                })
