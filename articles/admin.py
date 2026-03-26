from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    """Formset для проверки наличия одного основного раздела"""
    
    def clean(self):
        super().clean()
        
        # Проверяем, что есть хотя бы один раздел
        if not self.forms:
            raise ValidationError('Добавьте хотя бы один раздел')
        
        main_count = 0
        for form in self.forms:
            # Пропускаем пустые и удаленные формы
            if form.cleaned_data.get('DELETE', False):
                continue
            
            # Проверяем, что is_main установлен
            if form.cleaned_data.get('is_main', False):
                main_count += 1
            
            # Проверяем, что is_main может быть только True/False
            if 'is_main' in form.cleaned_data and form.cleaned_data['is_main'] is None:
                form.cleaned_data['is_main'] = False
        
        # Проверяем количество основных разделов
        if main_count == 0:
            raise ValidationError('Укажите основной раздел')
        elif main_count > 1:
            raise ValidationError('Может быть только один основной раздел')


class ScopeInline(admin.TabularInline):
    """Inline для редактирования разделов статьи"""
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    verbose_name = "Раздел"
    verbose_name_plural = "Разделы"
    fields = ['tag', 'is_main']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для разделов"""
    list_display = ['name', 'id']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админка для статей"""
    list_display = ['title', 'published_at', 'get_main_tag']
    list_filter = ['published_at']
    search_fields = ['title', 'text']
    inlines = [ScopeInline]
    
    def get_main_tag(self, obj):
        """Возвращает основной раздел статьи для отображения в списке"""
        main_scope = obj.scopes.filter(is_main=True).first()
        return main_scope.tag.name if main_scope else '-'
    get_main_tag.short_description = 'Основной раздел'
    
    def save_model(self, request, obj, form, change):
        """Сохраняем статью"""
        super().save_model(request, obj, form, change)
