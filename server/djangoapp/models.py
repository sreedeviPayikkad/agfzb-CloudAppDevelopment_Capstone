from django.db import models
from django.utils.timezone import now


# Create your models here.
# CarMake
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Dacia')
    description = models.CharField(null=False, max_length=50, default='A brand from Renault')

    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description


# CarModel
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CARMODEL_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerid = models.IntegerField(default=0)
    name = models.CharField(null=False, max_length=30, default='Sandero')
    cartype = models.CharField(max_length=5, choices=CARMODEL_TYPES, default=SEDAN)
    year = models.DateField(null=True)
	
    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment ):
        # dealership
        self.dealership = dealership
        # name
        self.name = name
        # purchase
        self.purchase = purchase
        # review
        self.review = review
        # purchase_date
        self.purchase_date = purchase_date
        # car_make
        self.car_make = car_make
        # car_model
        self.car_model = car_model
        # car_year
        self.car_year = car_year
        # sentiment
        self.sentiment = sentiment
        # id
        #self.id = id

    def __str__(self):
        return "Review: " + self.review
