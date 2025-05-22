from django import template
from information.models import Information

register = template.Library()

@register.inclusion_tag('information/_latest.html')
def latest_information():
    infos = Information.objects.filter(delete_flg=False).order_by('-created_at')[:3]
    return {'information_list': infos}