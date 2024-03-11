from ajax_select import register, LookupChannel
from .models import Tag, Category


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


@register("category")
class CategoryLookup(LookupChannel):

    model = Category

    def get_query(self, q, request):
        # 여기서는 예를 들어 사용자별로 카테고리를 제한할 수 있습니다.
        return self.model.objects.filter(name__icontains=q, author=request.user)

    def format_item_display(self, item):
        return "<span class='category'>{}</span>".format(item.name)
