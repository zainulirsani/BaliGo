from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

import io
import barcode
from barcode import Code128
from xhtml2pdf import pisa
from xhtml2pdf.config.httpconfig import httpConfig
from barcode.writer import ImageWriter
import pyqrcode
import base64

def render_to_pdf(template_src, context_dict={}):
	httpConfig.save_keys('nosslcheck', True)
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def render_barcode(data):
	# Write the barcode to a binary stream
	rv = BytesIO()
	Code128(str(data), writer=ImageWriter()).write(rv)
	encoded = base64.b64encode(rv.getvalue()).decode("ascii")
	image_png = 'data:image/png;base64,'+encoded
	return image_png

def render_qrcode(data):
	c = pyqrcode.create(data)
	s = io.BytesIO()
	c.png(s,scale=6)
	encoded = base64.b64encode(s.getvalue()).decode("ascii")
	image_png = 'data:image/png;base64,'+encoded
	return image_png