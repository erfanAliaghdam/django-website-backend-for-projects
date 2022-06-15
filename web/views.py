# TODO : complete the following View
# class ProjectList(ListAPIView):
#     queryset = Project.objects.prefetch_related('tag').all().annotate(
#         num_tags=Count('tag'))
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         return Response({'projects': self.queryset}, template_name='index.html')


