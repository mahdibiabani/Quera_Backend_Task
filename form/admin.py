from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Form, Question, FormResponse


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0  # No extra empty rows will be shown
    fields = ('text', 'question_type', 'required', 'max_length', 'min_value', 'max_value', 'number_type')
    readonly_fields = ('text', 'question_type', 'required', 'max_length', 'min_value', 'max_value', 'number_type')

    def get_extra(self, request, obj=None, **kwargs):
        # Limit questions display for a specific form in the admin panel
        if obj:
            return 0  # Show no extra question rows in form
        return super().get_extra(request, obj, **kwargs)
    

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Ensures the clean method is triggered
        except ValidationError as e:
            form.add_error(None, e)
        super().save_model(request, obj, form, change)


class ResponseInline(admin.TabularInline):
    model = FormResponse
    extra = 0
    fields = ('question', 'answer')
    readonly_fields = ('question', 'answer')

    def get_queryset(self, request):
        # This limits the responses to only the form being viewed
        queryset = super().get_queryset(request)
        form_id = request.resolver_match.kwargs.get('object_id')
        return queryset.filter(form__id=form_id)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)
    inlines = [QuestionInline]
    ordering = ('-created_at',)
    
    def get_inline_instances(self, request, obj=None):
        # Show ResponseInline only when viewing a specific form
        inline_instances = super().get_inline_instances(request, obj)
        if obj:
            inline_instances.append(ResponseInline(self.model, self.admin_site))
        return inline_instances



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'text', 'question_type', 'required', 'max_length', 'number_type', 'min_value', 'max_value')
    list_filter = ('form', 'question_type', 'required')
    search_fields = ('text',)
    ordering = ('form', 'id')


@admin.register(FormResponse)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'question', 'answer')
    list_filter = ('form', 'question')
    search_fields = ('answer',)
    ordering = ('form', 'id')

