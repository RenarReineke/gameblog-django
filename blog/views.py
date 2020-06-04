from django.shortcuts import render, get_object_or_404, redirect
from .models import*
from .forms import*

from django.views.generic import View
from .utils import*

from django.urls import reverse

from django.core.paginator import Paginator

from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.contrib.auth.signals import user_logged_in




@login_required
def home_user(request, id):

	profile=get_object_or_404(Profile, id=id)
	return render(request, 'blog/home_user.html', {'profile':profile})



@login_required
def users_list(request):

	
	profiles=Profile.objects.all()
	return render(request, 'blog/users_list.html', {'profiles':profiles})





def posts_list(request):

	search_query=request.GET.get('search', '')

	if search_query:
		posts=Post.objects.filter(Q(title__icontains=search_query)|Q(body__icontains=search_query))

	else:
		posts=Post.objects.order_by('-pk')

	search_query=request.GET.get('search', '')

	paginator=Paginator(posts, 6)
	page_number=request.GET.get('page', 1)
	page=paginator.get_page(page_number)

	is_paginated=page.has_other_pages()

	if page.has_previous():
		prev_url=f'?page={page.previous_page_number()}'
	else:
		prev_url=''

	if page.has_next():
		next_url=f'?page={page.next_page_number()}'
	else:
		next_url=''


	context={
	'page':page,
	'is_paginated':is_paginated,
	'prev_url':prev_url,
	'next_url':next_url,
	}

	return render(request, 'blog/index.html', context=context)



def tags_list(request):
	tags=Tag.objects.all()
	return render(request, 'blog/tags_list.html', {'tags':tags})




#def post_detail(request, slug):
#	post=Post.objects.get(slug__iexact=slug)
#	return render(request, 'blog/post.html', context={'post':post})


#def tag_detail(request, slug):
#	tag=Tag.objects.get(slug__iexact=slug)
#	return render(request, 'blog/tag.html', {'tag':tag})

def post_detail(request, slug):
	post=get_object_or_404(Post, slug__iexact=slug)

	comments=post.comments.filter(active=True)
	new_comment=None

	user=request.user
	
	
	if request.method=='POST':
		comment_form=CommentForm(request.POST)
		if comment_form.is_valid:
			new_comment=comment_form.save(commit=False)
			new_comment.post=post
			new_comment.user=user
			new_comment.save()
			return redirect(post)




	else:
		comment_form=CommentForm()


	return render(request, 'blog/post.html', {
		'post':post,
		'admin_object':post, 'detail':post,
		'comments':comments,
		'new_comment':new_comment,
		'comment_form':comment_form,
		})



class TagDetail(ObjectDetailMixin, View):
	model=Tag
	template='blog/tag.html'

	#def get(self, request, slug):
	#	tag=Tag.objects.get(slug__iexact=slug)
	#	tag=get_object_or_404(Tag, slug__iexact=slug)
	#	return render(request, 'blog/tag.html', {'tag':tag})






class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
	model_form=PostForm
	template='blog/post_create_form.html'

	raise_exception=True
	



class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
	model_form=TagForm
	template='blog/tag_create_form.html'

	raise_exception=True




class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model=Post
	model_form=PostForm
	template='blog/post_update.html'

	raise_exception=True




class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model=Tag
	model_form=TagForm
	template='blog/tag_update.html'

	raise_exception=True




class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

	model=Post
	template='blog/post_delete_form.html'
	redirect_url='posts_list_url'

	raise_exception=True



class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):

	model=Tag
	template='blog/tag_delete_form.html'
	redirect_url='tags_list_url'

	raise_exception=True



class CommentDelete(LoginRequiredMixin, View):

	

	raise_exception=True

	def get(self, request, id):
		comment=Comment.objects.get(id=id)
		return render(request, 'blog/comment_delete_form.html', {'comment':comment})


	def post(self, request, id):
		comment=Comment.objects.get(id=id)
		comment.delete()
		return redirect(comment.post)






class PostShare(View):

	def get(self, request, slug):
		post=get_object_or_404(Post, slug__iexact=slug)
		sent=False
		form=EmailPostForm()
		return render(request, 'blog/post_share.html', {'post':post, 'form':form, 'sent':sent})


	def post(self, request, slug):
		post=get_object_or_404(Post, slug__iexact=slug)
		form=EmailPostForm(request.POST)

		if form.is_valid():
			cd=form.cleaned_data

			post_url=request.build_absolute_uri(post.get_absolute_url())
			subject='{} ({}) рекомендует вам прочитать статью {}'.format(cd['name'],cd['email'], post.title)
			message='Прочитайте {} по ссылке {}.\n\nКомментарий от {}: {}'.format(post.title, post_url, cd['name'], cd['comment']) 

			send_mail(subject, message, 'imperecdiego@gmail.com', [cd['recipient'],])

			sent=True

			return render(request, 'blog/post_share.html', {'post':post, 'form':form, 'sent':sent})



#обработчик формы регистрации пользователя
def register(request):

	if request.method=='POST':
		user_form=UserRegistrationForm(request.POST)
		if user_form.is_valid:
			new_user=user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			Profile.objects.create(user=new_user)

			return render(request, 'blog/register_done.html', {'new_user':new_user})

	else:
		user_form=UserRegistrationForm()
		return render(request, 'blog/register.html', {'user_form':user_form})



#обаботчик редактирования профиля
@login_required
def edit(request):
	if request.method=='POST':
		user_form=UserEditForm(instance=request.user, data=request.POST)
		profile_form=ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

		if user_form.is_valid and profile_form.is_valid:
			user_form.save()
			profile_form.save()


	else:
		user_form=UserEditForm(instance=request.user)
		profile_form=ProfileEditForm(instance=request.user.profile)

	return render(request, 'blog/edit.html', {'user_form':user_form, 'profile_form':profile_form})

			