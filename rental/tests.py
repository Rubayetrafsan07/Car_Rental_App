from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User,Group
from .models import Car, Booking
from django.test import Client
from datetime import date


class CarModelTest(TestCase):

    def test_create_car(self):
        car = Car.objects.create(
            name="Toyota Corolla",
            description="A reliable car",
            price_per_day=50.00,
            is_available=True
        )
        self.assertEqual(car.name, "Toyota Corolla")
        self.assertEqual(car.description, "A reliable car")
        self.assertEqual(car.price_per_day, 50.00)
        self.assertTrue(car.is_available)

    def test_car_str_method(self):
        car = Car.objects.create(name="Honda Civic", price_per_day=40.00)
        self.assertEqual(str(car), "Honda Civic")



class BookingModelTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='testuser',password='testpass')
        self.car=Car.objects.create(
            name="Toyota Corolla",
            price_per_day=50.00,
        )

        def test_create_booking(self):

            booking = Booking.objects.create(
                user=self.user,
                car=self.car,
                start_date=date(2025,10,20),
                end_date=date(2025,11,25),
                total_price=250.00,
            )
            self.assertEqual(booking.user.username,'testuser')
            self.assertEqual(booking.car.name, 'Toyota Corolla')
            self.assertEqual(booking.start_date,date(2025,10,20))
            self.assertEqual(booking.end_date,date(2025,11,25))
            self.assertEqual(booking.total_price,250.00)



class CarListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Car.objects.create(name="Toyota Camery", price_per_day=50.00)

    def test_car_list_view_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('rental:car_list'))
        self.assertEqual(response.status_code, 200)


class FilteredCarViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.car = Car.objects.create(name="Honda Civic", price_per_day=40.00)

    def test_filtered_car_view_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('rental:filtered_car', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)


class BookCarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.car = Car.objects.create(
            name='Toyota Corolla',
            price_per_day=100,
            is_available=True
        )

    def test_book_car_post_creates_booking(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('rental:book_car', args=[self.car.id])

        data = {
            'start_date': '2025-10-20',
            'end_date': '2025-10-22'
        }
        response = self.client.post(url, data)

        booking = Booking.objects.first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.car, self.car)
        self.assertEqual(booking.total_price, 3 * self.car.price_per_day)  # 3 days
        self.assertTemplateUsed(response, 'booking_success.html')

    def test_book_car_get_renders_form(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('rental:book_car', args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_car.html')


class AddCarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='normaluser', password='12345')
        self.manager = User.objects.create_user(username='manager', password='12345')
        manager_group, created = Group.objects.get_or_create(name='Manager')
        self.manager.groups.add(manager_group)

    def test_add_car_get_renders_form(self):
        self.client.login(username='manager', password='12345')
        url = reverse('rental:add_car')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_car.html')

    def test_add_car_post_creates_car(self):
        self.client.login(username='manager', password='12345')
        url = reverse('rental:add_car')
        data = {
            'name': 'Honda Civic',
            'description': 'Test car',
            'price_per_day': 80,
            'is_available': True,
        }
        response = self.client.post(url, data, follow=True)

        car = Car.objects.first()
        self.assertIsNotNone(car)
        self.assertEqual(car.name, 'Honda Civic')

        self.assertRedirects(response, reverse('rental:car_list'))

    def test_non_manager_redirected(self):
        self.client.login(username='normaluser', password='12345')
        url = reverse('rental:add_car')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)



class CarSearchViewTest(TestCase):
    def setUp(self):
        Car.objects.create(name='Toyota Corolla', price_per_day=50)
        Car.objects.create(name='Honda Civic', price_per_day=40)
        Car.objects.create(name='Ford Fiesta', price_per_day=30)

    def test_car_search_returns_results(self):
        url = reverse('rental:car_search_api')
        response = self.client.get(url, {'q': 'Toyota'})

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Toyota Corolla')

    def test_car_search_no_results(self):
        url = reverse('rental:car_search_api')
        response = self.client.get(url, {'q': 'BMW'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['results'], [])



class ManagerDashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='normaluser', password='12345')
        self.manager = User.objects.create_user(username='manager', password='12345')
        manager_group, created = Group.objects.get_or_create(name='Manager')
        self.manager.groups.add(manager_group)

    def test_manager_can_access_dashboard(self):
        self.client.login(username='manager', password='12345')
        response = self.client.get(reverse('rental:manager_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_non_manager_redirected(self):
        self.client.login(username='normaluser', password='12345')
        response = self.client.get(reverse('rental:manager_dashboard'))
        self.assertEqual(response.status_code, 302)