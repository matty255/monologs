from ajax_select import register, LookupChannel
from .models import Tag


@register("tags")
class TagsLookup(LookupChannel):

    model = Tag

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def create_item(self, name):
        tag, created = self.model.objects.get_or_create(name=name)
        return tag

    def format_item_display(self, item):
        return "<span class='tag'>{}</span>".format(item.name)
