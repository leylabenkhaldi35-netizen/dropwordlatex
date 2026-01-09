from rest_framework.throttling import SimpleRateThrottle


class FreeUserRateThrottle(SimpleRateThrottle):
    scope = "free_user"

    def get_cache_key(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return None
        if user.role != "free":
            return None
        return self.cache_format % {
            "scope": self.scope,
            "ident": user.pk,
        }
