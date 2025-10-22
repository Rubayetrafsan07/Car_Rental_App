# Car Rental APP

## Project Overview

The Car Rental App is an online application developed using Django (Python framework) that allows users to view, search, and book cars for rental. The app is easy to use with a simple interface for users and administrators with authentication, car listing, filtered search, and booking functionality. The app is desktop and mobile responsive.

**key Goals:**
- provide a platform for user to rent car easily .
- Allow administrators to manage car listings and bookings.
- Demonstrate Django-based web development with database models, views, templates, and authentication.
- Include basic unit tests and filtering functionalities for better maintainability.

## Features

 **User Features:**
- **User Authentication:** Users can sign up, log in, and log out.
- **Browse Cars:** Users can see a list of available cars with details such as model, brand, price, and availability.
- **Search & Filter:** Users can search cars by name or filter based on car details.
- **Booking:** Users can book a car for a specific duration.
- **Responsive Design:** Works seamlessly on mobile devices (CSS media queries used for responsiveness).
  
 **Admin Features:**
- **Manage Cars:** Admin can add, edit, or delete cars.
- **View Bookings:** Admin can see all bookings and manage them accordingly.

## Database Models

**Car Model**
```python
 class Car(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
 ``` 
**Booking Model**
```python
 class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
  ```
**References:**
```bash
https://docs.djangoproject.com/en/4.2/topics/db/models/
  ```
## Views & Filtering

**Car Listing:**
```python
@login_required(login_url='/login/')
def car_list(request):
    cars= Car.objects.all()
    return render(request,'car_list.html',{'cars':cars})
```

**Car Filtered Page:**
```python
@login_required(login_url='/login/')
def filtered_car(request,car_id):
    car=get_object_or_404(Car,id=car_id)
    return render(request,'car_filtered.html',{'car':car})
  ```
 **References:**
 ```bash
https://stackoverflow.com/questions/58315639/login-required-decorator-is-not-working-properly-in-the-django
```
```bash
https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#get-object-or-404
  ```

## Docker Deployment

**docker-compose.yml**
```python
   version: "3.9"
   services:
       web:
       build: .
        ports:
          - "8000:8000"
        volumes:
           - .:/app
```
 **steps to run :**
 
 **1. Build Docker image:** docker-compose build
 
 **2. Run container:** docker-compose up
 
 **3. Access app:** http://localhost:8000

**Reference:**
```bash
 https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
 ```
## Testing

All the project's unit tests are located in the  ```rental/tests.py``` file.The application has successfully passed all tests implemented, with the assurance that essential functions — including car listing, filtering, and booking operations — are functioning as required.

**To run:**
```bash
python manage.py test rental
 ```
**Reference:**
```bash
https://docs.djangoproject.com/en/4.2/topics/testing/overview/
```
```bash
https://stackoverflow.com/questions/15073227/django-unit-test-simple-example
  ```
```bash
https://docs.djangoproject.com/en/4.2/topics/testing/tools/#jsonresponse
```
## How to Run

**1. Clone the repository:**
```bash
https://github.com/Rubayetrafsan07/Car_Rental_App.git
 ```
**2. Install dependencies:**
```bash
pip install -r requirements.txt
  ```
**3. Run Migration:**
```bash
python manage.py migrate
  ```
**4. Create SuperUser:**
```bash
python manage.py createsuperuser
 ```
**5. Run server:**
```bash
python manage.py runserver
```
**6. Open Browser:** 
```bash
http://127.0.0.1:8000
```

## Technologies Used
- **Python 3.11** — Core programming language
- **Django 5.x** — Web framework for building the app’s backend logic, models, views, and authentication.
- **SQLite3** — Default relational database used during development.
- **Django ORM** — For database queries and relationships between models.
- **HTML5 / CSS3** — Structure and styling for all templates.
- **AJAX**  — Used for filtering cars dynamically without refreshing the page.
- **Media Queries** — To ensure responsiveness across mobile and desktop devices.
- **Docker & Docker Compose** — For containerized development and easy deployment.
- **Git & GitHub** — Version control and collaboration.
- **PyCharm / VS Code** — Development environment used for writing and testing code.
  
## ScreenShots
**1. Login Page:** Allows users to securely sign in to their accounts.

   ![login](https://github.com/user-attachments/assets/98e3976a-b976-4521-b52a-05872dd59efa)
   
**2. Car_list Page:** It shows the available Cars

   ![Available Car](https://github.com/user-attachments/assets/7349d044-cb1f-43de-8a27-65f915d37e90)
   
**3. Filtered Page:** After searching for a car using the search box, the results are dynamically filtered using AJAX technology. When a user selects a specific car from the results, they are redirected to a detailed page displaying that car’s information.
  
   ![Filtered Car](https://github.com/user-attachments/assets/d8550107-9977-4f7b-8125-f448530cda48)
   
**4. My Booking:** Displays the list and total number of cars booked by the logged-in user.
    ![Bookings](https://github.com/user-attachments/assets/7f146d22-9b6c-4b94-b4fc-b99d9f98d98b)


## Conclusion

The Car Rental Application is a fully functional web application built with Django that provides a basic way of viewing, filtering, and booking automobiles. It demonstrates an end-to-end web development process, from backend database management to frontend responsiveness, AJAX-powered interactivity, and unit testing. The project highlights the seamless integration of modern web technologies to build a user-friendly and maintainable application.





