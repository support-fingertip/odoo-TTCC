import json

from odoo import api, fields, models


class FtHelpdeskTicket(models.Model):
    _name = 'ft.helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Subject',
        required=True,
        tracking=True,
    )
    ticket_no = fields.Char(
        string='Ticket #',
        readonly=True,
        copy=False,
        default='New',
    )
    description = fields.Html(string='Description')

    # ── Project linkage ────────────────────────────────────────────────────────
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        tracking=True,
        ondelete='set null',
        help='Link this ticket to one of your projects.',
    )

    # Computed domain so only the current user's own projects appear
    user_project_domain = fields.Char(
        compute='_compute_user_project_domain',
        store=False,
    )

    # ── Basic fields ───────────────────────────────────────────────────────────
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        tracking=True,
    )
    assigned_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned To',
        tracking=True,
        default=lambda self: self.env.user,
    )
    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Urgent'),
        ],
        string='Priority',
        default='1',
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('open', 'In Progress'),
            ('pending_customer', 'Pending Customer'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='new',
        tracking=True,
    )

    # ── Sequence ───────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ticket_no', 'New') == 'New':
                vals['ticket_no'] = self.env['ir.sequence'].next_by_code(
                    'ft.helpdesk.ticket'
                ) or 'New'
        return super().create(vals_list)

    # ── Project domain computation ─────────────────────────────────────────────
    @api.depends_context('uid')
    def _compute_user_project_domain(self):
        """
        Returns a domain that restricts the project_id many2one to projects
        where the current user is the project manager (user_id).
        Evaluated per-record but effectively constant within a single user session.
        """
        domain = [('user_id', '=', self.env.uid)]
        serialised = json.dumps(domain)
        for record in self:
            record.user_project_domain = serialised
