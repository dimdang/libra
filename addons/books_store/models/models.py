# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import timedelta as td
from openerp import models, fields, api
# class books_store(models.Model):
#     _name = 'books_store.books_store'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

# version 1
# class books_store(models.Model):
# 	_name = 'books_store.book_store'
# 	_description = 'Library Book'
# 	_order = 'date_release desc, name'
# 	name = fields.Char('Title', required=True)
# 	short_name = fields.Char('Release Title')
# 	date_release = fields.Date('Release Date')
# 	author_ids = fields.Many2many('res.partner', String='Authors')

# 	def name_get(self):
# 		result = []
# 		for record in self:
# 			result.append(
# 				(record.id,
# 					u"%s (%s)" % (record.name, record.date_release)
# 				)
# 			)
# 		returun result	

class books_store(models.Model):
	short_name = fields.Char(
		string='Short Title',
		size=100, # for char only
		translate=False, # also for Text field
		)
	notes = fields.Text('Internal Notes')
	state = fields.Selection(
		[ ('draft', 'Not Available'),
  		  ('available', 'Available'),
  		  ('lost', 'Lost')
		],
		'State'
		)

	description = fields.Html(
		string='Description',
		# optional:
		sanitize=True,
		strip_style=False,
		translate=False,
		)
	cover = fields fields.Binary('Book Cover')
	out_of_print = fields.Boolean('Out of Print?')
	date_release = fields.Date('Release Date')
	page = fields.Integer(
		string = 'Number of Page',
		default =0,
		help='Total book page count',
		groups='base.group_user',
		state={'cancel': [('readonly', True)]},
		copy=True,
		index=False,
		readonly=False,
		required=False,
		company_dependent=False,
	)
	reader_rating = fields.Float(
		'Reader Average Rating',
		(14, 4), # Optional precision (total, decimal),
	)
	cost_price = fields.Float(
		'Book Cost', dp.get_precision('Book Price')
	)

	currency_id = fields.Many2one(
		'res.currency', string='Currency'
	)

	retail_price = fields.Monetary(
	'Retail Price',
	# optional: currency_field='currency_id',
	)

	publisher_id = fields.Many2one(
	'res.partner', string='Publisher')

	author_ids = fields.Many2many(
	'res.partner', string='Authors'
	)

	age_days = fields.Float(
		string='Days Since Release',
		compute='_compute_age',
		inverse='_inverse_age',
		search='_search_age',
		store=False,
		compute_sudo=False,
		)

	publisher_city = fields.Char(
		'Publisher City',
		related='publisher_id.city')


	_sql_constraints = [
		('name_uniq',
		'UNIQUE (name)',
		'Book title must be unique.')
		]

def _inverse_age(self): today =
	fDate.from_string(fDate.today())
	for book in self.filtered('date_release'):
	d = td(days=book.age_days) - today
	book.date_release = fDate.to_string(d)

def _search_age(self, operator, value):
	today = fDate.from_string(fDate.today())
	value_days = td(days=value)
	value_date = fDate.to_string(today - value_days)
	return [('date_release', operator, value_date)]


@api.model
	def _referencable_models(self):
	models = self.env['res.request.link'].search([])
	return [(x.object, x.name) for x in models]

	ref_doc_id = fields.Reference(
	selection='_referencable_models',
	string='Reference Document')


# ResPartner For models

class ResPartner(models.Model):
	# _inherit = 'res.partner'
	# book_ids = fields.One2many(
	# 'library.book', 'publisher_id',
	# string='Published Books')

	_inherit = 'res.partner'
	_order = 'name'
	authored_book_ids = fields.Many2many(
	'library.book', string='Authored Books')
	count_books = fields.Integer(
	'Number of Authored Books',
	compute='_compute_count_books'
	)


	book_ids = fields.Many2many(
	'library.book',
	string='Authored Books',
	# relation='library_book_res_partner_rel'
	)

	@api.depends('authored_book_ids')
	def _compute_count_books(self):
	for r in self:
	r.count_books = len(r.authored_book_ids)



@api.constrains('date_release')
	def _check_release_date(self):
	for r in self:
	if r.date_release > fields.Date.today():
	raise models.ValidationError(
	'Release date must be in the past'
	)

@api.depends('date_release')
	def _compute_age(self):
	today = fDate.from_string(fDate.today())
	for book in self.filtered('date_release'):
	delta = (fDate.from_string(book.date_release - today)
	book.age_days = delta.days

