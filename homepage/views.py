from django.shortcuts import render

from django.views.generic import TemplateView

class HomepageView(TemplateView):
	template_name="homepage.html"

class StarView(TemplateView):
	template_name="star.html"
