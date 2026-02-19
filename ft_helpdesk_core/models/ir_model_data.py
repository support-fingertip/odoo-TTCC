import logging

from odoo import models

_logger = logging.getLogger(__name__)


class IrModelData(models.Model):
    _inherit = 'ir.model.data'

    def _process_end_unlink_record(self, record):
        """Handle FK constraint when orphaned res.groups records are cleaned up.

        During module updates, Odoo's _process_end tries to delete res.groups
        records that are no longer declared in any module's data files.  If
        ir_model_access rows still reference such a group (e.g. from a
        previous module version), psycopg2 raises a ForeignKeyViolation and
        the entire registry load fails.

        We resolve this by unlinking the dangling ir.model.access records
        *before* the group itself is deleted.
        """
        if record._name == 'res.groups':
            access_records = self.env['ir.model.access'].search(
                [('group_id', 'in', record.ids)]
            )
            if access_records:
                _logger.warning(
                    "ft_helpdesk_core: removing %d ir.model.access record(s) "
                    "referencing group id(s) %s before unlinking the group(s). "
                    "These records were left over from a previous module version.",
                    len(access_records),
                    record.ids,
                )
                access_records.unlink()
        return super()._process_end_unlink_record(record)
