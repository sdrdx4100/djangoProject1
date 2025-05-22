from django import template
from information.models import Information

register = template.Library()

@register.inclusion_tag('information/_latest.html')
def latest_information():
    info = Information.objects.order_by('-created_at').first()
    return {'information': info}