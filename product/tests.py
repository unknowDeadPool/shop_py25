from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import Category, Product
from .views import CategoryAPIView, ProductModelViewSet
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class CategoryTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        # Category.objects.create(title='c1')
        # Category.objects.create(title='c2')
        # Category.objects.create(title='c3')
        category = [
            Category(title='c1'),
            Category(title='c2'),
            Category(title='c3')
        ]
        Category.objects.bulk_create(category)

        self.setup_user()

    def setup_user(self):
        self.user = User.objects.create_user(
            email = 'test@test.com',
            password = 'test0315',
            is_active = True
        )

    def test_get_category(self):
        request = self.factory.get('api/v1/product/category/')
        view = CategoryAPIView.as_view({'get': 'list'})
        response = view(request)
        print(response.data)
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]['title'] == 'c1'

    def test_post_category(self):
        data = {
            'title': 'c4'
        }
        request = self.factory.post('api/v1/product/category/', data)
        force_authenticate(request, self.user)
        view = CategoryAPIView.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == 201
        assert Category.objects.filter(title='c4').exists()

class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.setup_user
        self.access_token = self.setup_user_token()

    def setup_user_token(self):
        data = {
            'email': 'test@test.com',
            'password': 'test0315',
        }
        request = self.factory.post('api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()        
        response = view(request)

        return response.data

        # print(response.status_code)
        # print(response.data)

    @staticmethod
    def setup_category():
        category = [
            Category(title='c1'),
            Category(title='c2'),
            Category(title='c3')
        ]
        Category.objects.bulk_create(category)

    def setup_user(self):
        self.user = User.objects.create_user(
            email = 'test@test.com',
            password = 'test0315',
            is_active = True
        )

    def test_post_product(self):
        image = open('media/products/test.jpeg', 'rb')
        print(image)
        data = {
            'category': Category.objects.first(),
            'title': 'test_product',
            'price': 20,
            'amount': 20,
            'image': image
        }
        request = self.factory.post('api/v1/product/modelviewset_crud/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        force_authenticate(request, self.user)

        view = ProductModelViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == 201
        assert Product.objects.filter(title='test_product').exists() 

        