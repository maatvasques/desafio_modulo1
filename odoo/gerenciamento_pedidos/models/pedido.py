# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class Pedido(models.Model):
    _name = 'gerenciamento_pedidos.pedido'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gerenciamento de Pedidos'

    name = fields.Char(string='Referência', required=False, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('gerenciamento_pedidos.pedido.sequence'))
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    # NOVO CAMPO: Adicionado para testes rápidos
    data_pedido = fields.Date(string='Data do Pedido', default=fields.Date.today())
    pedido_item_ids = fields.One2many('gerenciamento_pedidos.pedido.item', 'pedido_id', string='Itens do Pedido')
    total = fields.Float(string='Total do Pedido', compute='_compute_total', store=True)

    @api.depends('pedido_item_ids.subtotal')
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(item.subtotal for item in pedido.pedido_item_ids)

    # Em odoo/gerenciamento_pedidos/models/pedido.py

def action_enviar_whatsapp(self):
    self.ensure_one()

    whatsapp_api_url = 'http://waha:3000/api/default/sendText'
    
    # LÓGICA ATUALIZADA: Busca o celular e depois o telefone do cliente
    numero_destino = self.cliente_id.mobile or self.cliente_id.phone
    
    if not numero_destino:
        message = "Nenhum número de Celular (Mobile) ou Telefone (Phone) encontrado no cadastro do cliente."
        self.message_post(body=message, subtype_xmlid='mail.mt_note')
        return

    # O resto do código continua igual...
    numero_limpo = ''.join(filter(str.isdigit, numero_destino))

    api_payload = {
        'chatId': f'{numero_limpo}@c.us',
        'text': f'Olá! Este é um teste de envio de mensagem de texto. Pedido {self.name}.'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        _logger.info(f"Enviando pedido {self.name} para {api_payload['chatId']}")
        response = requests.post(whatsapp_api_url, json=api_payload, headers=headers, timeout=30)
        response.raise_for_status()

        message = "Mensagem de teste enviada com sucesso via WhatsApp."
        self.message_post(body=message, subtype_xmlid='mail.mt_note')
        _logger.info("Mensagem enviada com sucesso!")

    except requests.exceptions.RequestException as e:
        message = f"Falha ao enviar a mensagem via WhatsApp. Erro: {e}"
        self.message_post(body=message, subtype_xmlid='mail.mt_note')
        _logger.error(f"Erro ao enviar pedido: {e}")

class PedidoItem(models.Model):
    _name = 'gerenciamento_pedidos.pedido.item'
    _description = 'Item do Pedido'

    pedido_id = fields.Many2one('gerenciamento_pedidos.pedido', string='Pedido')
    produto_id = fields.Many2one('product.product', string='Produto', required=True)
    quantidade = fields.Integer(string='Quantidade', default=1, required=True)
    preco_unitario = fields.Float(string='Preço Unitário', required=True, related='produto_id.list_price', readonly=False)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantidade', 'preco_unitario')
    def _compute_subtotal(self):
        for item in self:
            item.subtotal = item.quantidade * item.preco_unitario