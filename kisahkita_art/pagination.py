from rest_framework import pagination, serializers

class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000000
    min_limit = 1
    min_offset = 0
    max_offset = 1000000

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError) as e:
                raise e  # Re-raise the caught exception

        return self.default_limit

    def get_offset(self, request):
        try:
            return _positive_int(
                request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError) as e:
            raise e  # Re-raise the caught exception