from odoo import api, fields, models, _
import time

class order(models.Model):
    _name = 'ptkp.order'

   
    #request_id = fields.Many2one('ptkp.request')
    #reference = fields.Char(related='request_id.reference')
    #reference = fields.Char(string='reference', related='ptkp.request.reference', tracking=True)
    reference_od = fields.Char('No PTKP')
    lokasi_od = fields.Char(string='Lokasi')
    bukti_od = fields.Char(string='Bukti')