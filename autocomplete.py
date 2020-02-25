from dal import autocomplete

from users.models import EmploymentDetail


class UserProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return UserProfile.objects.none()

        qs = EmploymentDetail.objects.all()

        if self.q:
            qs = qs.filter(borower__istartswith=self.q)
        return qs


# class TagAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated():
#             return Tag.objects.none()
#
#         qs = Tag.objects.all()
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs