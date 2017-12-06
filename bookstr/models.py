from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Publisher(models.Model):
    name = models.CharField(max_length = 75)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 250)
    ISBN = models.IntegerField()
    price = models.FloatField()
    publication_year = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    bookcover = models.CharField(max_length=500)
    number_of_books_instock = models.IntegerField()


    def __str__(self):
        return self.title

    #Same book with differnt versions are stored as differnt books in my DB

class Genre(models.Model):
    class Meta:
        unique_together = ('bookname','genre')

    bookname = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.CharField(max_length = 50)

    def __str__(self):
        return self.genre



class Author(models.Model):
    FName = models.CharField(max_length = 75)
    LName = models.CharField(max_length = 75)

    def __str__(self):
        return self.FName + " " + self.LName

class Customer(models.Model):
    cust_id = models.OneToOneField(User, primary_key = True)
    FName = models.CharField(max_length = 75)
    LName = models.CharField(max_length = 75)
    HouseNo = models.IntegerField()
    StreetNo = models.IntegerField()
    City = models.CharField(max_length = 100)
    State = models.CharField(max_length = 75)
    Country = models.CharField(max_length = 75)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list
    def __str__(self):
        return self.FName + self.LName

class Owner(models.Model):
    store_id = models.IntegerField()
    own_id = models.OneToOneField(User)
    OwnName = models.CharField(max_length = 75)

    def __str__(self):
        return self.OwnName

class CreditCard(models.Model):

    CC_No = models.CharField(max_length = 20)
    NameOnCard = models.CharField(max_length = 75)
    exp_date = models.DateField()
    cvv = models.IntegerField()

    #One user can have N credit cards, but the same credit card cannot be used to register multiple users.

    def __str__(self):
        return self.NameOnCard

class CrediCardOwner(models.Model):
    class Meta:
        unique_together = ('cc','userid')

    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    cc = models.ForeignKey(CreditCard)

    def __str__(self):
        return str(self.cc) + " " + str(self.userid)



class BookBuyTrans(models.Model):


    amount = models.IntegerField()
    timestamp = models.DateTimeField(default = datetime.now)
    cc_num = models.ForeignKey(CreditCard)
    cust_id = models.ForeignKey(User)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cust_id) + " bought " + str(self.book_id) + " on " + str(self.timestamp) + " which costed " + str(self.amount)


class WrittenBy(models.Model):
    class Meta:
        unique_together = ('book_id','author_id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.book_id) +" "+ str(self.author_id)


class BookReorder(models.Model):
    storeid = models.ForeignKey(Owner)
    timestamp = models.DateTimeField(default = datetime.now)

class BooksInReorder(models.Model):
    class Meta:
        unique_together = ('reorder_id','book_id')
    reorder_id = models.ForeignKey(BookReorder)
    book_id =  models.ForeignKey(Book, on_delete = models.CASCADE)

class Cart(models.Model):
    book_id = models.ForeignKey(Book)
    number_of_copies = models.IntegerField()
    us = models.ForeignKey(User)



    def __str__(self):
        return str(self.book_id) + str(self.number_of_copies)


    def get_absolute_url(self):
        return reverse('bookstr:cart')
