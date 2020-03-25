from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from .models import*





class PostForm(forms.ModelForm):
	class Meta:
		model=Post 
		fields=['title','slug', 'body', 'tag', 'image', 'link']

		widgets={
		'title':forms.TextInput(attrs={'class':'Здесь должно быть название класса для инпута'}),
		'slug':forms.TextInput(attrs={'class':'Здесь должно быть название класса для инпута'}),
		'body':forms.Textarea(attrs={'class':'Здесь должно быть название класса для инпута'}),
		'tag':forms.SelectMultiple(attrs={'class':'Здесь должно быть название класса для инпута'}),
		
		}

	def clean_slug(self):
		new_slug=self.cleaned_data['slug'].lower()

		if new_slug=='create':
			raise ValidationError('Слаг не может быть "Create" ')

		return new_slug




class TagForm(forms.ModelForm):
	class Meta:
		model=Tag 
		fields=['title','slug']

		widgets={
		'title':forms.TextInput(attrs={'class':'Здесь должно быть название класса для инпута'}),
		'slug':forms.TextInput(attrs={'class':'Здесь должно быть название класса для инпута'}),
		}

	def clean_slug(self):
		new_slug=self.cleaned_data['slug'].lower()

		if new_slug=='create':
			raise ValidationError('Слаг не может быть "Create" ')

		
		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError(f'Слаг должен быть уникальным. Слаг {new_slug} уже существует')

		return new_slug




class EmailPostForm(forms.Form):

	name=forms.CharField(max_length=30, label='Имя отправителя')
	email=forms.EmailField(label='Емайл отправителя')

	recipient=forms.EmailField(label='Емайл получателя')
	comment=forms.CharField(required=False, widget=forms.Textarea, label='Комментарий')





class CommentForm(forms.ModelForm):

	class Meta:
		model=Comment
		fields=['body',]




class UserRegistrationForm(forms.ModelForm):

	password=forms.CharField(label='Password', widget=forms.PasswordInput)
	password2=forms.CharField(label='Repeat_Password', widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=('username', 'first_name', 'email')


	def clean_password2(self):

		cd=self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Пароли не совпадают!')
		return cd['password2']





class UserEditForm(forms.ModelForm):

	class Meta:
		model=User
		fields=('username', 'first_name', 'email')



class ProfileEditForm(forms.ModelForm):

	class Meta:
		model=Profile
		fields=('date_of_birth', 'foto')


