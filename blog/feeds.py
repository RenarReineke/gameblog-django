from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):

	title='gameblog'
	link='/blog/'
	descriptions='New post in gameblog'

	def items(self):

		return Post.objects.order_by('-date')[:6]



	def item_title(self, item):

		return item.title



	def item_descriptions(self, item):

		return truncatewords(item.body, 30)