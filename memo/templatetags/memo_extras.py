from django import template
import markdown as md

register = template.Library()

@register.filter
def markdown(value):
    return md.markdown(value, extensions=['fenced_code', 'tables'])

@register.filter
def get_tag_name(tags, tag_id):
    try:
        tag_id = int(tag_id)
        tag = tags.get(id=tag_id)
        return tag.name
    except (ValueError, tags.model.DoesNotExist):
        return ''