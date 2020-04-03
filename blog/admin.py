from django.contrib import admin

from .models import*



#admin.site.register(Post)
#admin.site.register(Tag)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display=('title', 'slug', 'date', 'user', 'link')
	search_fields=('title', 'body', 'user')
	list_filter=('date',)
	prepopulated_fields={'slug':('title',)}
	date_hierarchy='date'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display=('title', 'slug', 'user')
	search_fields=('title', 'user')
	prepopulated_fields={'slug':('title',)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display=('name', 'email', 'post', 'body', 'created', 'updated', 'active', 'user')
	search_fields=('name', 'email', 'body', 'user')
	list_filter=('active', 'created', 'updated')
	date_hierarchy='created'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display=('user', 'date_of_birth', 'foto')
	
	list_filter=('date_of_birth',)
	date_hierarchy='date_of_birth'




	
	