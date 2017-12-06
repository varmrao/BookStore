from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from datetime import *
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    all_books = Book.objects.all()
    context = {
        'all_books' : all_books
    }
    return render(request,'bookstr/home.html',context)

def logouts(request):
    logout(request)
    return render(request, 'bookstr/logins.html')

def custsignup(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        houseno = request.POST['house_no']
        streetno = request.POST['street_no']
        city = request.POST['city']
        state = request.POST['state']
        cntry = request.POST['ctry']
        pnum = request.POST['ph_no']

        cc_no = request.POST['cc_no']
        nc = request.POST['ncc']
        exp = request.POST['exp_date']
        cv = request.POST['cvv']


        customer = Customer.objects.create(cust_id=request.user,FName=fname,LName=lname,HouseNo=houseno,StreetNo = streetno,City = city,State = state,Country = cntry,phone_number = pnum)
        customer.save()
        creditc = CreditCard.objects.create(CC_No=cc_no,NameOnCard=nc,exp_date=exp,cvv = cv)
        creditc.save()
        creditccown = CrediCardOwner.objects.create(userid = request.user,cc = creditc)
        return redirect('/bookstr/home/')
    else:
        return render(request, 'bookstr/custsignup.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('custsignup/')
    else:
        form = UserCreationForm()
    return render(request, 'bookstr/index2.html', {'form': form})

def prelogin(request):
    return render(request,'bookstr/logins.html')

def logins(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        logger = authenticate(username=username, password=password)
        if logger is not None:
            login(request, logger)
            return redirect('/bookstr/home/')
        else:
            return render(request, 'bookstr/loginerror.html')
    else :
        return redirect('signup/')



def book(request, book_id):
    book = get_object_or_404(Book,pk = book_id)
    writtenby = get_list_or_404(WrittenBy,book_id = book_id)
        # Gets list of all authors for a particular book.
    author = [w.author_id for w in writtenby]

    gen = get_list_or_404(Genre,bookname = book_id)

    ge = [g.genre for g in gen]

    context = {
        'book' : book,
        'author' : author,
        'ge' : ge,
    }
    return render(request,'bookstr/book.html',context)


def cart(request):
    cart = Cart.objects.all().filter(us = request.user)
    cart_books = [c.book_id for c in cart]
    cart_books = []

    data = []
    for c in cart:
        if(c.book_id not in cart_books):
            cart_books.append(c.book_id)

    for c in cart:
        for n in cart_books:
            if (c.book_id == n):
                resultdict = {}

                # Change this
                resultdict['title'] = n.title
                resultdict['numberofcopies'] = c.number_of_copies
                resultdict['priceofentry'] = (n.price) * (c.number_of_copies)

                data.append(resultdict)
    total = 0
    for d in data:
        total += d['priceofentry']
        total = round(total,2)

    context = {
        'data' : data,
        'total' : total,
    }
    return render(request,'bookstr/cart.html',context)
def cartadded(request, book_id):
    book = get_object_or_404(Book,pk = book_id)
    writtenby = get_list_or_404(WrittenBy,book_id = book_id)
            # Gets list of all authors for a particular book.
    author = [w.author_id for w in writtenby]

    context = {
        'book' :book,
        'author' : author,

    }
    return render(request, 'bookstr/cart_form.html',context)

def cartaddedbook(request, book_id):
    book = get_object_or_404(Book,pk = book_id)

    if request.method=='POST':
        number_of_copies = int(request.POST.get('noc', "0"))
        if (book.number_of_books_instock >= number_of_copies):
            cart_entry = Cart.objects.create(book_id=book, number_of_copies=number_of_copies,us = request.user)
            cart_entry.save()
            book.number_of_books_instock = (book.number_of_books_instock) - 1
            book.save()
        else:
            context = {
                'noinstock' : book.number_of_books_instock,
            }
            return render(request,'bookstr/error.html',context)

    cart = Cart.objects.all().filter(us = request.user)
    cart_books = [c.book_id for c in cart]
    cart_books = []

    data = []
    for c in cart:
        if(c.book_id not in cart_books):
            cart_books.append(c.book_id)

    for c in cart:
        for n in cart_books:
            if (c.book_id == n):
                resultdict = {}

                # Change this
                resultdict['title'] = n.title
                resultdict['numberofcopies'] = c.number_of_copies
                resultdict['priceofentry'] = (n.price) * (c.number_of_copies)

                data.append(resultdict)
    total = 0
    for d in data:
        total += d['priceofentry']
        total = round(total,2)
    context = {
        'data' : data,
        'total' : total,
    }
    return render(request,'bookstr/cart.html',context)

def checkout(request):
    if request.method == 'POST':
        card_num = request.POST['noc']

        return redirect('/bookstr/checkedout/' + (card_num))


    else:
        cardsowned = CrediCardOwner.objects.all().filter(userid = request.user)

        cards = [card.cc for card in cardsowned]

        context = {
            'cards' : cards,
        }

        return render(request,'bookstr/checkout.html',context)

def cardadder(request):
    if request.method == 'POST':
        cc_no = request.POST['cc_no']
        nc = request.POST['ncc']
        exp = request.POST['exp_date']
        cv = request.POST['cvv']


        creditc = CreditCard.objects.create(CC_No=cc_no,NameOnCard=nc,exp_date=exp,cvv = cv)
        creditc.save()
        creditccown = CrediCardOwner.objects.create(userid = request.user,cc = creditc)

        return redirect('/bookstr/checkedout/' + (cc_no))

    else:
        return render(request,'bookstr/cardadder.html')



def checkedout(request, card_num):
    card = CreditCard.objects.get(CC_No = card_num)


    if request.method == 'POST':
        exp = request.POST['exp_date']
        cv = request.POST['cv']
        expp = datetime.strptime(exp, "%Y-%m-%d").date()




        if (card.exp_date == expp and card.cvv == int(cv) and date.today() < card.exp_date):

            cart = Cart.objects.all().filter(us = request.user)
            cart_books = [c.book_id for c in cart]
            cart_books = []

            data = []
            for c in cart:
                if(c.book_id not in cart_books):
                    cart_books.append(c.book_id)

            for c in cart:
                for n in cart_books:
                    if (c.book_id == n):
                        resultdict = {}

                        # Change this
                        title = n.title
                        numberofcopies = c.number_of_copies
                        priceofentry = (n.price) * (c.number_of_copies)

                        bookbuytrans = BookBuyTrans.objects.create(cust_id=request.user,cc_num = card,book_id = c.book_id,amount = priceofentry,timestamp = datetime.now())
                        bookbuytrans.save()

                        cart = Cart.objects.all().filter(us = request.user).delete()

            cust = Customer.objects.get(cust_id = request.user)
            context = {
                'house_no' : cust.HouseNo,
                'street_no' : cust.StreetNo,
                'city' : cust.City,
                'state' : cust.State,
                'country' : cust.Country,
                'ph' : cust.phone_number,


            }
            return render(request,'bookstr/done.html',context)






        else:
            return render(request,'bookstr/paymenterror.html')

    else:
            context = {
                'card' : card_num,
            }

            return render(request,'bookstr/checkedout.html',context)


def search(request):

    if request.method == 'POST':
        sr = request.POST['sr']

        try:
            book = Book.objects.get(title__contains = sr)
        except ObjectDoesNotExist:
            return render(request,'bookstr/nobook.html')

        writtenby = get_list_or_404(WrittenBy,book_id = book)
            # Gets list of all authors for a particular book.
        author = [w.author_id for w in writtenby]

        gen = get_list_or_404(Genre,bookname = book)

        ge = [g.genre for g in gen]

        context = {
            'book' : book,
            'author' : author,
            'ge' : ge,
        }
        return render(request,'bookstr/book.html',context)

def ownsignin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        store_id = request.POST['storeid']

        logger = authenticate(username=username, password=password)
        if logger is not None:
            login(request, logger)

            own = Owner.objects.get(own_id = request.user)


            if (int(store_id) == (own.store_id)):
                return redirect('/bookstr/reorder/')
            else:
                return render(request, 'bookstr/ownloginerror.html')

        else:
            return render(request, 'bookstr/ownloginerror.html')

    else:
        return render(request, 'bookstr/ownersignin.html')


def reorder(request):
    if request.method == 'POST':
        bookISBN = int(request.POST['bk'])
        number_of_copies = int(request.POST['nc'])

        own = Owner.objects.get(own_id = request.user)

        bkrdr = BookReorder.objects.create(storeid=own,timestamp = datetime.now())
        bkrdr.save()
        book = Book.objects.get(ISBN = bookISBN)

        book.number_of_books_instock = book.number_of_books_instock + number_of_copies
        book.save()


        bkinrdr = BooksInReorder.objects.create(reorder_id=bkrdr,book_id = book)
        bkinrdr.save()

        return render(request, 'bookstr/DoneReorder.html')


    else:
        b = Book.objects.all()
        ran = [1,2,3,4,5,6,7,8,9,10]
        context = {
            'books' : b,
            'ran' : ran,
        }
        return render(request, 'bookstr/reorder.html',context)
