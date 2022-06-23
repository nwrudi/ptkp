from odoo import api, fields, models, _
import time

class request(models.Model):
    _name = 'ptkp.request'

    

    reference = fields.Char(string='No PTKP', required=True, copy=False, readonly=True, size=150, 
                            default=lambda self: _('New'))
    user_id = fields.Many2one(comodel_name="res.users")
    kepada  = fields.Many2one(comodel_name="res.users",readonly=True,
            states={'draft' : [('readonly',False)]})
    #name = fields.Char("Nomor PTKP", required=True, size=60,
    #        readonly=True,
    #        states={'draft' : [('readonly',False)]})
    jenis_ptkp = fields.Selection([('tind_perbaikan','Tindakan Perbaikan'),
        ('tind_pencegahan','Tindakan Pencegahan'),
        ('tind_keduanya','Tindakan Perbaikan & Pencegahan')], string="Jenis PTKP", help="Silakan pilih salah satu")
    uraian = fields.Text("Uraian", required=False,
            readonly=True,
            states={'draft' : [('readonly',False)]})
    sumber = fields.Selection([('audit_internal','Audit Intenal'),
        ('tinjauan_mgn','Tinjauan Managemen'),
        ('keluhan_pelanggan','Keluhan Pelanggan'),
        ('trend_proses','Tren Proses/Layanan Tidak Sesuai'),
        ('program_imp','Program Improvement/Peningkatan'),
        ('lain','Lain-lain')], string="Sumber", help="Silakan pilih salah satu")
    
    lokasi = fields.Text("Lokasi", required=False,
            readonly=True,
            states={'draft' : [('readonly',False)]})
    bukti = fields.Text("Bukti", required=False,
            readonly=True,
            states={'draft' : [('readonly',False)]})
    referensi = fields.Text("Referensi", required=False,
            readonly=True,
            states={'draft' : [('readonly',False)]})
    
        #states={'draft' : [('readonly',False)],'confirmed0' : [('readonly',True)],'confirmed0' : [('readonly',True)]})
        #date_scheduled = fields.Datetime('Scheduled Date', required=True, readonly=True, states={'draft':[('readonly',False)],'released':[('readonly',False)],'ready':[('readonly',False)]}, default=time.strftime('%Y-%m-%d %H:%M:%S'))


    tindakan_awal = fields.Text("Tindakan Awal", required=False)
    akar_penyebab = fields.Text("Akar Penyebab", required=False)
    tindakan_koreksi = fields.Text("Tindakan Koreksi", required=False)
    send_date  = fields.Date("Tanggal dikirim", required=False,
                              default=lambda self:time.strftime("%Y-%m-%d"),
                              readonly=True,
                                states={'draft' : [('readonly',False)]})
    receipt_date  = fields.Date(string="Tanggal diterima")
    finish_date  = fields.Date(string="Tanggal Penyelesaian",readonly=['ptkp.group_ptkp_auditor'])
    verifikasi_date  = fields.Date(string="Tanggal Verifikasi", required=False,
                readonly=True,
            states={'close' : [('readonly',False)]})
    tindakan_pencegahan = fields.Text("Tindakan Pencegahan", readonly=['ptkp.group_ptkp_auditor'])
    komentar = fields.Text("Komentar", required=False,
                        readonly=True,
            states={'close' : [('readonly',False)]})
    catatan_tambahan = fields.Text("Catatan Tambahan", required=False,
                        readonly=True,
            states={'close' : [('readonly',False)]})
    
    state = fields.Selection(
        string="Status",
        selection=[
            ('draft','Draft'),
            ('request','Send Request'),
            ('confirmed0','Accept by Auditan'),
            ('confirmed1','Confirmed Finish'),
            ('confirmed2','Confirmed by Auditor'),
            ('close','Close')],
        readonly=True,
        required=True,
        default='draft'
        )
    

    @api.multi
    def action_request(self):
        self.state='request'
    
    @api.multi
    def action_confirm(self):
        self.state='confirmed0'

    @api.multi
    def action_confirm1(self):
        self.state='confirmed1'

    @api.multi
    def action_confirm2(self):
        self.state='confirmed2'

    @api.multi
    def action_close(self):
        self.state='close'
    
    @api.multi
    def action_draft(self):
        self.state='draft'

    @api.multi
    def action_reopen(self):
        self.state='reeopen'
    

    @api.model
    def create(self, vals):
        if vals.get('No PTKP', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('ptkp.request') or _('New')
            res = super(request, self).create(vals)
            return res
   

    def action_confirm(self):
            order = self.env['ptkp.order']
            order_id = False
            for request in self:
                order_id = order.create({
                    
                    'reference_od': request.reference,
                    'state': 'draft',
                    
                    'bukti_od': request.bukti,
                    'lokasi_od': request.lokasi,
                })
            self.write({'state': 'confirmed0'})
            return order_id.id