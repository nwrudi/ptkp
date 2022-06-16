from odoo import api, fields, models, _
import time

class ptkp(models.Model):
    _name = 'ptkp.ptkp'



    

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
        
    kepada = fields.Char("Kepada", required=True, size=100)
    lokasi = fields.Char("Lokasi Temuan", size=100)
    uraian = fields.Char("Uraian", size=100)
    bukti = fields.Char("Bukti", size=100)


    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('ptkp.ptkp') or _('New')
            res = super(ptkp, self).create(vals)
            return res


    