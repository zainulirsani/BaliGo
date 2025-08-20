from django.conf import settings

def api_maps_view(request):
	return {'API_MAPS_VIEW': settings.API_MAPS_VIEW}

def api_open_route_service(request):
	return {'API_OPEN_ROUTE_SERVICE': settings.API_OPEN_ROUTE_SERVICE}