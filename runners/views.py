from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import NewRunnerForm
from .models import Runner
from oauth2.models import Platform
from django.urls import reverse_lazy

class PlatformListView(ListView):
	model = Platform
	template_name='runners/platform_index.html'
	
class NewRunnerFormView(FormView):
	template_name='runners/newrunner_form.html'
	form_class=NewRunnerForm
	
	def form_valid(self, form):
		first_name=form.cleaned_data['first_name']
		username=form.cleaned_data['username']
		goal=form.cleaned_data['goal']
		
		user=User.objects.create_user(username=username,
									  first_name=first_name,
									  )
		user.set_unusable_password()
		user.save()
	
		login(self.request, user)

		platform=Platform.objects.get(id=self.kwargs['platform_id'])
		
		runner=Runner(user=user,platform=platform,goal=goal)
		runner.save()

		return super(NewRunnerFormView, self).form_valid(form)
	
	def get_success_url(self):
		return reverse_lazy('new_runner_oauth2', kwargs={'platform_id': self.kwargs['platform_id']})
	