from django.conf import settings

class trial:

	def__init__(self, get_response):
		self.get_response = get_response
		print(get_response)
		pass

	def__call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs)