from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa



def sendmail(subject,template,to,context):
    subject = subject
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'nextgenscrap@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmail_invoice(subject,template,to,context):
    subject = subject
    template_str = 'ecom/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'nextgenscrap@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmail_invoice_subscription_sc(subject,template,to,context):
    subject = subject
    template_str = 'rc/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'nextgenscrap@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmail_invoice_subscription_sc(subject,template,to,context):
    subject = subject
    template_str = 'sc/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'nextgenscrap@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None