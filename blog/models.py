from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django.conf import settings

from django.contrib.auth.models import User

from time import time


def gen_slug(s):
	new_slug=slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))





class Post(models.Model):
	title=models.CharField(max_length=200, db_index=True, verbose_name='Название')
	slug=models.SlugField(max_length=200, blank=True, unique=True, verbose_name='Слаг', allow_unicode=True)
	body=models.TextField(blank=True, db_index=True, verbose_name='Описание')
	date=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
	updated=models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
	tag=models.ManyToManyField('Tag', blank=True, related_name='posts')
	image=models.ImageField(upload_to='posts', verbose_name='Картинка', null=True)
	link=models.URLField(blank=True, null=True, verbose_name='Ссылка', help_text='Введите адрес ссылки')
	user=models.ForeignKey(
		User, on_delete=models.CASCADE,
		verbose_name='Автор', related_name='posts',
		db_index=True, null=True
		)
	
	

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug=gen_slug(self.title)

		super().save(*args, **kwargs)



	def __str__(self):
		return f'{self.title}'


	def __repr__(self):
		return f'{self.title}'


	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug})


	class Meta:
		verbose_name='Статья'
		verbose_name_plural='Статьи'
		ordering=['-date']





class Tag(models.Model):
	title=models.CharField(max_length=50, db_index=True, verbose_name='Тэг')
	slug=models.SlugField(max_length=50, unique=True, verbose_name='Слаг')
	user=models.ForeignKey(
		User, on_delete=models.CASCADE,
		verbose_name='Автор', related_name='tags',
		db_index=True, null=True
		)
	
	

	def __str__(self):
		return f'{self.title}'


	def __repr__(self):
		return f'{self.title}'


	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug':self.slug})


	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug':self.slug})


	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug':self.slug})


	class Meta:
		verbose_name='Тэг'
		verbose_name_plural='Тэги'





class Comment(models.Model):

	post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments', verbose_name='Статья')
	name=models.CharField(max_length=50, verbose_name='Имя пользователя')
	email=models.EmailField()
	body=models.TextField(verbose_name='Текст')
	created=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	updated=models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
	active=models.BooleanField(default=True, verbose_name='Видим ли для пользователей?')
	user=models.ForeignKey(
		User, on_delete=models.CASCADE,
		verbose_name='Автор', related_name='comments',
		db_index=True, null=True
		)
	
	


	class Meta:
		ordering=('created',)
		verbose_name='Комментарий'
		verbose_name_plural='Комментарии'


	def __str__(self):
		return 'Комментарий от пользователя {} к статье {}: {}'.format(self.name, self.post, self.body)


	def get_delete_url(self):
		return reverse('comment_delete_url', kwargs={'id':self.id})




class Profile(models.Model):

	user=models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth=models.DateField(blank=True, null=True, verbose_name='Дата рождения')
	foto=models.ImageField(upload_to='users', blank=True, null=True, verbose_name='Аватарка')



	def __str__(self):
		return f'Профиль пользователя {self.user.username}'


	class Meta:
		verbose_name='Профиль пользователя'
		verbose_name_plural='Профили пользователей'
		ordering=('-date_of_birth',)


	def get_absolute_url(self):
		return reverse('home_user', kwargs={'id':self.id})




	