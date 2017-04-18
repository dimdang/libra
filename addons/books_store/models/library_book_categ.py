# -*- coding: utf-8 -*-

from openerp import models, fields, api
class BookCategory(models.Model):
_name = 'library.book.category'
name = fields.Char('Category')
parent_id = fields.Many2one(
'library.book.category',
string='Parent Category',
ondelete='restrict',
index=True)

child_ids = fields.One2many(
'library.book.category', 'parent_id',
string='Child Categories')