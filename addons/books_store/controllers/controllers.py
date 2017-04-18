# -*- coding: utf-8 -*-
from openerp import http

# class BooksStore(http.Controller):
#     @http.route('/books_store/books_store/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/books_store/books_store/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('books_store.listing', {
#             'root': '/books_store/books_store',
#             'objects': http.request.env['books_store.books_store'].search([]),
#         })

#     @http.route('/books_store/books_store/objects/<model("books_store.books_store"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('books_store.object', {
#             'object': obj
#         })