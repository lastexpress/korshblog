from django.contrib import admin
from .models import Post, Comment


'''
Так мы говорим Django, что наша модель зарегистрирована на сайте адми - 
нистрирования с  помощью пользовательского класса, наследника ModelAdmin.
'''

#Декоратор @admin.register() выполняет те же действия, 
#что и функция admin.site.register(): регистрирует декорируемый класс – 
#наследник ModelAdmin.



#ДОБАВЛЯЕМ ФИЛЬТР НА САЙТ АДМИНИСТРОВАНИЯ
#metaclass
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status') #Отображение заголовков в списке созданных статей
	list_filter = ('status', 'created', 'publish', 'author') #Поля в фильтрах
	search_fields = ('title', 'body') #Поиск по заголовкам только заголовок и сам текст
	prepopulated_fields = {'slug': ('title',)} # В создании статьи, слаг заполняется автоматически за title
	raw_id_fields = ('author',) #Можно выбирать из списка авторов для создании статьи.
	date_hierarchy = 'publish' # добавлены ссылки для навигации по датам.
	ordering = ('status', 'publish') #По умолчанию статьи отсортированы по полям status и publish.
 
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')