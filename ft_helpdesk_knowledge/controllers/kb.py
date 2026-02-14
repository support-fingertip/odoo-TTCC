import json
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class KnowledgeBaseController(http.Controller):

    @http.route('/my/support/kb', type='http', auth='public', website=True)
    def kb_index(self, search='', **kw):
        """Knowledge Base index page with categories and search."""
        Article = request.env['ft.helpdesk.kb.article'].sudo()
        Category = request.env['ft.helpdesk.kb.category'].sudo()

        categories = Category.search([
            ('portal_published', '=', True),
            ('parent_id', '=', False),
        ], order='sequence')

        articles = False
        if search:
            articles = Article.search([
                ('portal_published', '=', True),
                '|', '|', '|',
                ('name', 'ilike', search),
                ('summary', 'ilike', search),
                ('keywords', 'ilike', search),
                ('body_html', 'ilike', search),
            ], limit=20, order='helpful_score desc, view_count desc')

        values = {
            'page_name': 'kb_index',
            'categories': categories,
            'articles': articles,
            'search': search,
        }
        return request.render('ft_helpdesk_knowledge.kb_portal_index', values)

    @http.route('/my/support/kb/<string:slug>', type='http',
                auth='public', website=True)
    def kb_article(self, slug, **kw):
        """Single KB article page."""
        Article = request.env['ft.helpdesk.kb.article'].sudo()
        article = Article.search([
            ('slug', '=', slug),
            ('portal_published', '=', True),
        ], limit=1)

        if not article:
            return request.redirect('/my/support/kb')

        # Increment view counter
        article._increment_view()

        # Related articles from same category
        related = Article.search([
            ('category_id', '=', article.category_id.id),
            ('portal_published', '=', True),
            ('id', '!=', article.id),
        ], limit=5, order='view_count desc')

        values = {
            'page_name': 'kb_article',
            'article': article,
            'related_articles': related,
        }
        return request.render('ft_helpdesk_knowledge.kb_portal_article', values)

    @http.route('/my/support/kb/category/<int:category_id>', type='http',
                auth='public', website=True)
    def kb_category(self, category_id, **kw):
        """KB category page with articles list."""
        Category = request.env['ft.helpdesk.kb.category'].sudo()
        Article = request.env['ft.helpdesk.kb.article'].sudo()

        category = Category.browse(category_id)
        if not category.exists() or not category.portal_published:
            return request.redirect('/my/support/kb')

        articles = Article.search([
            ('category_id', '=', category.id),
            ('portal_published', '=', True),
        ], order='sequence, helpful_score desc')

        values = {
            'page_name': 'kb_category',
            'category': category,
            'articles': articles,
        }
        return request.render('ft_helpdesk_knowledge.kb_portal_category', values)

    @http.route('/my/support/kb/suggest', type='http', auth='user',
                website=True, methods=['GET'])
    def kb_suggest(self, q='', category_id=None, **kw):
        """AJAX endpoint for KB article suggestions during ticket creation."""
        if len(q) < 3:
            return request.make_json_response([])

        Article = request.env['ft.helpdesk.kb.article'].sudo()
        domain = [
            ('portal_published', '=', True),
            '|', '|',
            ('name', 'ilike', q),
            ('summary', 'ilike', q),
            ('keywords', 'ilike', q),
        ]

        # If category specified, try to find KB articles related to that category
        if category_id:
            kb_cats = request.env['ft.helpdesk.kb.category'].sudo().search([
                ('helpdesk_category_id', '=', int(category_id)),
            ])
            if kb_cats:
                domain = [
                    ('portal_published', '=', True),
                    ('category_id', 'in', kb_cats.ids),
                    '|', '|',
                    ('name', 'ilike', q),
                    ('summary', 'ilike', q),
                    ('keywords', 'ilike', q),
                ]

        articles = Article.search(domain, limit=5,
                                  order='helpful_score desc, view_count desc')

        result = [{
            'id': a.id,
            'title': a.name,
            'slug': a.slug,
            'summary': a.summary or '',
        } for a in articles]

        return request.make_json_response(result)

    @http.route('/my/support/kb/vote/<int:article_id>', type='json',
                auth='user', website=True)
    def kb_vote(self, article_id, helpful=True, **kw):
        """AJAX endpoint for helpful/not helpful votes."""
        article = request.env['ft.helpdesk.kb.article'].sudo().browse(article_id)
        if article.exists() and article.portal_published:
            article._vote_helpful(helpful)
            return {'success': True}
        return {'success': False}
