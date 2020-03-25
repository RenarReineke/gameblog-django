from django.shortcuts import render, get_object_or_404, redirect
from .models import*


class ObjectDetailMixin():
	model=None
	template=None

	def get(self, request, slug):
		obj=get_object_or_404(self.model, slug__iexact=slug)
		return render(request, self.template, context={self.model.__name__.lower():obj, 'admin_object':obj, 'detail':obj})




class ObjectCreateMixin:

	model_form=None
	template=None



	def get(self, request):
		obj=self.model_form()
		return render(request, self.template, {self.model_form.__name__.lower():obj})


	def post(self, request):
		message_error_create_form='Вы неправильно заполнили форму! Попробуйте снова.'


		user=request.user

		bound_form=self.model_form(request.POST, files=request.FILES)
		if bound_form.is_valid():
			new_obj=bound_form.save(commit=False)
			new_obj.user=user
			new_obj.save()
			return redirect(new_obj)
		return render(request, self.template, {self.model_form.__name__.lower():bound_form, 'message_error_create_form':message_error_create_form})



class ObjectUpdateMixin():

	model=None
	model_form=None
	template=None


	def get(self, request, slug):
		obj=self.model.objects.get(slug__iexact=slug)
		bound_form=self.model_form(instance=obj)

		return render(request, self.template, {'form':bound_form, self.model_form.__name__.lower():obj})


	def post(self, request, slug):
		message_error_create_form='Вы неправильно заполнили форму! Попробуйте снова.'

		obj=self.model.objects.get(slug__iexact=slug)
		bound_form=self.model_form(request.POST, instance=obj, files=request.FILES)

		if bound_form.is_valid():
			new_obj=bound_form.save()
			return redirect(new_obj)

		return render(request, self.template, {'form':bound_form, self.model_form.__name__.lower():obj, 'message_error':message_error_create_form})




class ObjectDeleteMixin():

	model=None
	template=None
	redirect_url=None

	def get(self, request, slug):
		obj=self.model.objects.get(slug__iexact=slug)
		return render(request, self.template, {self.model.__name__.lower():obj})


	def post(self, request, slug):
		obj=self.model.objects.get(slug__iexact=slug)
		obj.delete()
		return redirect(reverse(self.redirect_url))