import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse


def link_callback(uri, rel):
    # convert URIs to absolute system paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        # handle absolute uri (i.e., "http://my.tld/a.png")
        return uri

    # make sure that the local file exists
    if not os.path.isfile(path):
        raise Exception(
            "Media URI must start with "
            f"'{settings.MEDIA_URL}' or '{settings.STATIC_URL}'")
    return path


def generate_pdf(template, context_pdf, filename):
    # Template that we are going to use to render the pdf
    template_path = template
    context = context_pdf
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download:
    # response['Content-Disposition'] = 'attachment;
    # filename="historia-clínica.pdf"'
    # If display on browser
    response['Content-Disposition'] = 'filename="'+filename+'.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response,
        link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
