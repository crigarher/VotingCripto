from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Question, Choice

# Crear grupos si no existen
admin_group, created_admin = Group.objects.get_or_create(name='admin')
user_group, created_user = Group.objects.get_or_create(name='user')

# Asignar permisos al grupo admin
if created_admin:
    # Obtener permisos de los modelos
    question_ct = ContentType.objects.get_for_model(Question)
    choice_ct = ContentType.objects.get_for_model(Choice)
    permissions = Permission.objects.filter(content_type__in=[question_ct, choice_ct])
    admin_group.permissions.set(permissions)


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
        'fields': ['pollEndDate'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
