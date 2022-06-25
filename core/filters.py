from admin_searchable_dropdown.filters import AutocompleteFilter
from django.contrib.admin.filters import SimpleListFilter



class MentorVerificationFilter(SimpleListFilter):
    title = 'mentor Verification'
    field_name = 'profile_mentor__is_verified'
    parameter_name = 'mentor_verification'
    
    def lookups(self, request, model_admin):

        return (
            (True, ('yes')),
            (False, ('no')),
        )
    def queryset(self, request, queryset):
        if self.value() == True:
            return queryset.select_related('profile_mentor').filter(is_mentor = True, profile_mentor__is_verified=True)
        if self.value() == False:
            return queryset.select_related('profile_mentor').filter(is_mentor = True, profile_mentor__is_verified=False)
