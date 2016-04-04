from django.shortcuts import get_object_or_404
from .models import Node
from django.http import Http404


class NodeMixin(object):

    node = False
    node_model = Node

    def dispatch(self, request, *args, **kwargs):
        self.node_pk = kwargs.get('node_pk', None)
        self.get_node()
        return super(NodeMixin, self).dispatch(request, *args, **kwargs)

    def get_node(self):
        if self.node:
            return self.node
        if self.node_pk:
            self.node = get_object_or_404(self.node_model, id=self.node_pk)
        else:
            raise Http404
        return self.node

    def get_context_data(self, **kwargs):
        context = super(NodeMixin, self).get_context_data(**kwargs)
        context.update({
            'node_id': (self.node_pk and int(self.node_pk)) or self.get_node().id,
            'node': self.get_node()
        })
        return context

    # def get_user_can_edit(self):
    #     user = self.request.user
    #     try:
    #         if user and (self.node.org and self.node.org.is_owner(user)) or user.is_superuser:
    #             return True
    #     except AttributeError, e:
    #         return False
    #     return False
