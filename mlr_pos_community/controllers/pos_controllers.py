# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import http
from odoo.http import request
import json
import logging
import requests

_logger = logging.getLogger(__name__)

class BTCPayController(http.Controller):
    
    @http.route('/btcpay/submitlightningorder', type='json', auth='user', csrf=False, methods=['POST']) #creates a lightning invoice based on current order
    def btcpay_lightning_payment_link(self, **kw):
        try:
            btcpay_invoice = request.env['btcpay.server.instance'].search([('state', '=', 'active')], limit=1).action_create_invoice_lightning(kw) #calls function to create invoice and passes kw
            btcpay_invoice_id = btcpay_invoice['id'] #retrieves invoice id
            btcpay_payment_link = btcpay_invoice['BOLT11'] #retrieves invoice itself
            invoiced_sat_amount = btcpay_invoice['invoiced_sat_amount'] #retrieves invoiced satoshi amount
            conversion_rate = btcpay_invoice['conversion_rate'] #retrieves conversion rate of transaction
            return json.dumps({ #returns information that will be placed on bill receipt and stored in database if ultimately paid
                'error':False,
                'btcpay_payment_link_qr_code': "lightning:"+btcpay_payment_link, #adds lightning prefix for QR code
                'btcpay_payment_link': btcpay_payment_link, #the invoice itself
                'btcpay_invoice_id': btcpay_invoice_id,
                'invoiced_sat_amount': invoiced_sat_amount,
                'conversion_rate': conversion_rate
            })
        except Exception as e: #error if invoice cannot be created
             return json.dumps({
                 'error':True,
                 'error_message': "Internal Server Error!!"
            })
    @http.route('/btcpay/lightninginvoice', type='json', auth='user', csrf=False, methods=['POST']) #checks status of the lightning transaction
    #three possible statuses: Paid, Unpaid, and Expired. Status of an existing invoice will be displayed if unpaid or expired
    def btcpay_check_lightning_invoice(self, **kw):
        try:
            btcpay_invoice = request.env['btcpay.server.instance'].search([('state', '=', 'active')], limit=1).action_check_lightning_invoice(kw.get('invoice_id')) #calls function to get invoice status, should also check that invoice id is not blank
            if btcpay_invoice['status'] == 'Paid':
                return json.dumps({
                    'error': False,
                    'invoice_status': btcpay_invoice['status']

                })
            elif btcpay_invoice['status'] == 'Unpaid':
                return json.dumps({
                    'error': True,
                    'error_message': "Lightning: payment not made, check again in a minute. Invoice status is: " + btcpay_invoice['status']
                })
            else:
                return json.dumps({
                    'error': True,
                    'error_message': "Lightning: unknown error with invoice. Invoice status is: " + btcpay_invoice['status']
                })
        except Exception as e: #if an invoice status cannot be obtained, currently assumed to be due to no invoice having been created
             return json.dumps({
                 'error': True,
                 'error_message': "Lightning: invoice likely not created. Create invoice through invoice button or split screen."
            })