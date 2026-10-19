from django.test import TestCase
from django.urls import reverse

from .models import Blog


class BlogModelTests(TestCase):
    def test_new_blog_has_zero_likes(self):
        blog = Blog.objects.create(
            title='Test article',
            description='Test description'
        )

        self.assertEqual(blog.likes, 0)

    def test_blog_string_representation(self):
        blog = Blog.objects.create(
            title='My first article',
            description='Test description'
        )

        self.assertEqual(str(blog), 'My first article')


class BlogListViewTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(
            title='Test article',
            description='Article description',
            author='Test author'
        )

    def test_list_page_returns_200(self):
        response = self.client.get(reverse('blog_list'))

        self.assertEqual(response.status_code, 200)

    def test_list_page_uses_correct_template(self):
        response = self.client.get(reverse('blog_list'))

        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_list_page_shows_blog_content(self):
        response = self.client.get(reverse('blog_list'))

        self.assertContains(response, 'Test article')
        self.assertContains(response, 'Article description')
        self.assertContains(response, 'Test author')

    def test_list_page_contains_detail_link(self):
        response = self.client.get(reverse('blog_list'))
        detail_url = reverse('blog_detail', args=[self.blog.id])

        self.assertContains(response, f'href="{detail_url}"')


class BlogDetailViewTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(
            title='Detail article',
            description='Detailed description',
            author='Detail author'
        )

    def test_detail_page_returns_200(self):
        response = self.client.get(
            reverse('blog_detail', args=[self.blog.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_detail_page_shows_blog_content(self):
        response = self.client.get(
            reverse('blog_detail', args=[self.blog.id])
        )

        self.assertContains(response, 'Detail article')
        self.assertContains(response, 'Detailed description')
        self.assertContains(response, 'Detail author')

    def test_detail_page_returns_404_for_missing_blog(self):
        response = self.client.get(
            reverse('blog_detail', args=[9999])
        )

        self.assertEqual(response.status_code, 404)

    def test_visiting_detail_increases_likes(self):
        self.assertEqual(self.blog.likes, 0)

        self.client.get(
            reverse('blog_detail', args=[self.blog.id])
        )

        self.blog.refresh_from_db()

        self.assertEqual(self.blog.likes, 1)

    def test_each_detail_visit_increases_likes(self):
        detail_url = reverse('blog_detail', args=[self.blog.id])

        self.client.get(detail_url)
        self.client.get(detail_url)

        self.blog.refresh_from_db()

        self.assertEqual(self.blog.likes, 2)