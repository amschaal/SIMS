from rest_framework import filters
from django.db.models.query import Q

class ContainsSampleFilter(filters.BaseFilterBackend):
    """
    Find Pools containing sample where contains_sample=sample_id.  This is necessary if the sample is in a pool which is added to another pool.
    """
    def filter_queryset(self, request, queryset, view):
        sample_id = view.request.query_params.get('contains_sample',None)
        if sample_id is not None:
            return queryset.filter(Q(samples__id=sample_id)|Q(pools__samples__id=sample_id))
        else:
            return queryset
