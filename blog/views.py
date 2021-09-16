from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag

def post_list(request, tag_slug=None):
	posts = Post.published.all().order_by('-publish')
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(posts, 4) #По 3 статьи на каждой странице
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# Если страница не является целым числом, возвращаем первую страницу.
		posts = paginator.page(1)
	except EmptyPage:
		# Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/post/list.html', {'page' : page, 'posts': posts, 'tag' : tag})

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, 
								   status='published',
								   publish__year=year,
								   publish__month=month,
								   publish__day=day)

	#Список активных комментариев этой статьи
	comments = post.comments.filter(active=True).order_by('-created')

	new_comment = None

	if request.method == 'POST':
		#Пользователь отправил коммент
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			#Создаём коммент, но не сохраняем в БД
			new_comment = comment_form.save(commit=False)
			#Привязываем коммент к статье
			new_comment.post = post
			#SAVE COMMENT IN BASEDATE
			new_comment.save()
	else:
		comment_form = CommentForm()

	post_tags_ids = post.tags.values_list('id', flat=True) #получает все ID тегов текущей статьи. Метод валуе_лист возвр кортеж. flat=True, чтобы получить «плоский» список вида [1, 2, 3, ...]
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)#получает все статьи, содержащие хоть один тег из полученных ранее, исключая текущую статью;
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

	# использует функцию агрегации Count для формирования вычисляемого 
	#поля same_tags, которое содержит определенное количество совпадающих тегов;

	# сортирует список опубликованных статей в убывающем порядке по количеству совпадающих тегов 
	# для отображения первыми максимально похожих статей и делает срез результата для отображения только четырех статей.
											

	return render(request, 'blog/post/detail.html', {'post': post, 
													'comments' : comments, 
													'new_comment' : new_comment, 
													'comment_form' : comment_form,
													'similar_posts' : similar_posts})


class PostListViews(ListView):
	queryset = Post.published.all().order_by('-publish')
	context_object_name = 'posts'
	paginate_by = 4
	template_name = 'blog/post/list.html'


def post_share(request, post_id):
	post = get_object_or_404(Post,
								id=post_id,
								status='published')
	sent = False

	if request.method == 'POST':
		#форма была отправлена на сохранение
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#все поля формы прошли валид
			cd = form.cleaned_data
			#отправка электронной почты
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post' : post, 'form' : form, 'sent' : sent})











