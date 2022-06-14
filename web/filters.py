from admin_searchable_dropdown.filters import AutocompleteFilter

class TagAutoCompleteFilter(AutocompleteFilter):
    title = 'filter by Tag'
    field_name = 'tag'