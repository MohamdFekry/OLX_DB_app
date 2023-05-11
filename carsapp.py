import mysql.connector
import os
from datetime import datetime
#from tabulate import tabulate
import tabulate

print("Hello!\nThis app allows you to interact with a database holding the ads listed on OLX Egypt for used cars posted in the last month in Cairo")

def interface():
    print("\nWhat would you like to do?: ")
    print("1. Register a user")
    print("2. Add a new user sale for an ad")
    print("3. View existing reviews of a given ad")
    print("4. View aggregated rating of a seller / owner")
    print("5. See all the ads for a given brand, body type and year in a specific location , along withthe average price & the number of listings for each model")
    print("6. See all cars in a certain location in a given price range")
    print("7. See the top 5 areas in cairo by amount of inventory and average price a given brand")
    print("8. See the top 5 sellers by the amount of listings they have, along with their avg price")
    print("9. See all the properties listed by a specific owner (given their phone no) ")
    print("10. See the top 5 brands & models by the amount of inventory and their average price for a given year range")
    print("11. Exit")

    choice = input("\nEnter the number of the task you want to do: ")
    choices = ['1','2','3','4','5','6','7','8','9','10','11']
    while choice not in choices:
        choice = input("Invalid. Please enter a number from 1 to 11: ")
    if choice == '1':
      os.system('cls')
      register_user()
    if choice == '2':
      os.system('cls')
      add_user_sale()
    if choice == '3':
      os.system('cls')
      view_review()
    if choice == '4':
      os.system('cls')
      agg_seller_rating()
    if choice == '5':
      os.system('cls')
      show_ads()
    if choice == '6':
      os.system('cls')
      show_cars_loc_price()
    if choice == '7':
      os.system('cls')
      show_top_inventory_loc()
    if choice == '8':
      os.system('cls')
      show_top_listings_seller()
    if choice == '9':
      os.system('cls')
      show_ads_of_seller()
    if choice == '10':
      os.system('cls')
      show_top_cars_in_year()
    if choice == '11':
      os.system('cls')
      quit()

def register_user():
    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    print("Enter your credentials: \n")
    username = input("Username: ")
    email = input("Email: ")
    gender = input("Gender(M/F): ")
    while(gender != 'M' and gender !='F'):
        gender = input("Invalid gender. Please, enter only \'M\' or \'F\': ")
    dob = input("Date of Birth (yyyy/mm/dd): ")
    while True:
      try:
        datetime.strptime(dob, "%Y/%m/%d").date()
      except ValueError:
        dob = input("Please, enter a valid date in the format(yyyy/mm/dd): ")
      else:
        break
    yob = datetime.strptime(dob, "%Y/%m/%d").year
    age = 2023 - yob

    mycursor = mydb.cursor()
    sql = """
    INSERT INTO users
    VALUES  (%s,%s,%s,%s,%s);
    """
    user = (username, email, gender, age, dob) 
    mycursor.execute(sql, user)
    mydb.commit()

    prefs = input("Success!\nDo you want to enter your preferences of Brands & Models(Y/N): ")
    while(prefs != 'Y' and prefs !='N'):
        prefs = input("Invalid choice. Please, enter only \'Y\' or \'N\': ")
    while prefs == 'Y':
        brand = input("Enter a Brand: ")
        model = input("Enter a Model: ")
        sql = """
              INSERT INTO usersprefs
              VALUES  (%s,%s,%s);
              """
        userpref = (username, brand, model) 
        mycursor.execute(sql, userpref)
        mydb.commit()

        prefs = input("Success!\nDo you want to enter another preference(Y/N): ")
        while(prefs != 'Y' and prefs !='N'):
            prefs = input("Invalid choice. Please, enter only \'Y\' or \'N\': ")

    choice = input("You have been registered.\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def add_user_sale():
    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    id = input("Enter the ID of the ad listing the car you bought: ")
    username = input("Enter your username: ")
    price = input("Enter the price you purchased this car for: ")
    rating = input("Please rate your purchase by a number from 1 to 5: ")
    while (rating != '1' and rating !='2' and rating != '3' and rating !='4' and rating !='5'):
        rating = input("Invalid. Please enter a number from 1 to 5: ")
    
    str_review = None
    rev = input("Do you want to add a review(Y/N): ")
    while(rev != 'Y' and rev !='N'):
            rev = input("Invalid choice. Please, enter only \'Y\' or \'N\': ")
    if rev == 'Y':
        print("Write your review: ")
        review = []
        while True:
            line = input()
            if line == '':
                break
            else:
                review.append(line + '\n')
        str_review = ''.join(review)

    mycursor = mydb.cursor()
    sql = """
    UPDATE ads
    SET Purchased = "TRUE", Username = %s, Rating = %s, Review = %s, PurchasingPrice = %s
    WHERE ID = %s;
    """
    val = (username, rating, str_review, price, id) 
    mycursor.execute(sql, val)
    mydb.commit()

    choice = input("The sale has been registered.\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def view_review():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    adID = input("Enter the ID of the ad: ")

    while len(adID) != 9:
      adID = input("Please, enter a valid ad ID: ")

    mycursor = mydb.cursor()
    sql = """
    Select Review from ads where ID = %s;
    """

    mycursor.execute(sql, (adID,))

    result = mycursor.fetchall()
    if not result:
      choice = input("There are no ads with this ID.\nEnter z to continue using the app or any other letter to exit: ")
      if choice == "z":
        interface()
      else:
        quit()

    for r in result:
        if r[0] == None:
          print("There are no written reviews for this ad")
        else:
          print(f"The review of the ad you want is: {r[0]}")
    
    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def agg_seller_rating():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    sellerphone = input("Enter the phone number of the seller you want to get their avg rating: ")
    sellerphone = "2" + sellerphone

    mycursor = mydb.cursor()
    sql = """
    select AVG(Rating) from ads where SellerPhone = %s;
    """
    
    mycursor.execute(sql, (sellerphone,))

    result = mycursor.fetchall()
    if not result:
      choice = input("There are no sellers with that phone number.\nEnter z to continue using the app or any other letter to exit: ")
      if choice == "z":
        interface()
      else:
        quit()

    for r in result:
        if r[0] == None:
          print("This seller has made no sales and so has no rating yet.")
        else:
          print(f"The AVG rating of the Seller with that phone number is: {r[0]}")
    
    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_ads():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    print("Enter the details of the ad:\n")
    brand = input("Brand: ")
    body = input("Body type: ")
    year = input("Year: ")
    loc = input("Location: ")
    val = (brand, body, year, loc)
    #val = ("Peugeot", "Sedan", 1970, "Mokattam")
    mycursor = mydb.cursor()
    sql = """
    select * from ads where Brand = %s AND BodyType = %s AND Year = %s AND Location = %s;
    """
    
    mycursor.execute(sql, val)

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no available ads with these details.")

    else:
      if result[0][0] == None:
          print("\nThere are no available ads with these details.")
      else:
        print("\nThe ads available with these details are:\n")
        table = ["ID", "PostingDate", "Location", "Brand", "Model", "AdType", "FuelType", "Price", "PriceType", "Payment", "Year", "KMsLow",
                  "KMsHigh", "Transmission", "Color", "Body", "CCLow", "CCHigh", "Video", "VirtualTour", "Description", "SellerPhone", "Purchased",
                  "Username", "Rating", "Review", "PurchasingPrice"]
        #print("ID\t\t Posting Date\t Location\t Brand\t\t Model\t Ad Type\t Fuel Type\t Payment\t Year\t KMs low\t KMs high\t Transmission\t Color\t\t Body\t CC low\t CC high\t Seller Phone\t Purchased\t Username\t Rating\t Review\t Price\t Purchasing price\t Description")
        for r in result:
          for i in range(0, 27):
            print(f"{table[i]}: {r[i]}")
          print("-------------------------------------------------------------")
        '''
        for r in result:
          tup = list(r[0:20])
          for i in range(21, 27):
            tup.append(r[i])
          tup.append(r[20])
          #print(tup)
          table.append(tup)
          #print(f"{r[0]}\t {r[1]}\t {r[2]}\t {r[3]}\t {r[4]}\t {r[5]}\t {r[6]}\t {r[9]}\t\t {r[10]}\t {r[11]}\t\t {r[12]}\t\t {r[13]}\t {r[14]}\t\t {r[15]}\t {r[16]}\t {r[17]}\t {r[21]}\t {r[22]}\t {r[23]}\t {r[24]}\t {r[25]}\t {r[7]}\t {r[26]}\t {r[20]}\t")
        '''
        #print(tabulate.tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        #print(table[1])
        sql = """
            select AVG(Price) from ads where Brand = %s AND BodyType = %s AND Year = %s AND Location = %s;
          """
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        print(f"\nThe AVG price of all these cars is: {result[0][0]}")

        sql = """
            select Model, count(*) from ads where Brand = %s AND BodyType = %s AND Year = %s AND Location = %s GROUP BY Model;
          """
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        print("\nThe number of listings for each model of this brand:\n")
        print("Model \t # of listings")
        for r in result:
          print(f"{r[0]} \t {r[1]}")
        
    

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_cars_loc_price():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    print("Enter the details of the ad:\n")
    low = input("Price starts from: ")
    up = input("Price ends at: ")
    loc = input("Location: ")
    val = (loc, low, up)
    #val = ("Peugeot", "Sedan", 1970, "Mokattam")
    mycursor = mydb.cursor()
    sql = """
    select * from ads where Location = %s AND Price >= %s AND Price <= %s;
    """
    
    mycursor.execute(sql, val)

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no available ads with these details.")

    else:
      if result[0][0] == None:
          print("\nThere are no available ads with these details.")
      else:
        print("\nThe ads available with these details are:\n")
        table = ["ID", "PostingDate", "Location", "Brand", "Model", "AdType", "FuelType", "Price", "PriceType", "Payment", "Year", "KMsLow",
                  "KMsHigh", "Transmission", "Color", "Body", "CCLow", "CCHigh", "Video", "VirtualTour", "Description", "SellerPhone", "Purchased",
                  "Username", "Rating", "Review", "PurchasingPrice"]
        for r in result:
          for i in range(0, 27):
            print(f"{table[i]}: {r[i]}")
          print("-------------------------------------------------------------")
        '''
        for r in result:
          tup = list(r[0:20])
          for i in range(21, 27):
            tup.append(r[i])
          tup.append(r[20])
          #print(tup)
          table.append(tup)
        '''
        #print(tabulate.tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_top_inventory_loc():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    brand = input("Enter the Brand you are interested in: ")

    mycursor = mydb.cursor()
    sql = """
    select Location, COUNT(*), AVG(Price) from ads WHERE Brand = %s GROUP BY Location ORDER BY COUNT(*) DESC LIMIT 5;
    """
    
    mycursor.execute(sql, (brand, ))

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no available ads for this brand.")

    else:
      if result[0][0] == None:
          print("\nThere are no available ads for this brand.")
      else:
        print("\nThe ads available with these details are:\n")
        table = [["Location", "Inventory", "AVG Price"]]
        
        for r in result:
          table.append(list(r))
          
        print(tabulate.tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_top_listings_seller():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    mycursor = mydb.cursor()
    sql = """
    select SellerPhone, Name, COUNT(*), AVG(Price) from ads inner join sellers on ads.SellerPhone = sellers.Phone GROUP BY SellerPhone, Name ORDER BY COUNT(*) DESC LIMIT 5;
    """
    
    mycursor.execute(sql)

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no available ads for this brand.")

    else:
      if result[0][0] == None:
          print("\nThere are no available ads for this brand.")
      else:
        print("\nThe ads available with these details are:\n")
        print("Seller Phone\t Name\t\t\t # of listed ads\t AVG Price")
        for i in range(5):
          if i == 0:
            print(f"{result[i][0]}\t {result[i][1]}\t\t  {result[i][2]}\t\t {result[i][3]}")
          else:
            print(f"{result[i][0]}\t {result[i][1]}\t\t\t {result[i][2]}\t\t {result[i][3]}")

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_ads_of_seller():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    phone = input("Enter the phone number of the seller: ")
    phone = "2" + phone
    mycursor = mydb.cursor()
    sql = """
    select * from ads WHERE SellerPhone = %s;
    """
    
    mycursor.execute(sql, (phone, ))

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no sellers with that number.")

    else:
      if result[0][0] == None:
          print("\nThere are no sellers with that number.")
      else:
        print("\nThe ads available with these details are:\n")
        table = ["ID", "PostingDate", "Location", "Brand", "Model", "AdType", "FuelType", "Price", "PriceType", "Payment", "Year", "KMsLow",
                  "KMsHigh", "Transmission", "Color", "Body", "CCLow", "CCHigh", "Video", "VirtualTour", "Description", "SellerPhone", "Purchased",
                  "Username", "Rating", "Review", "PurchasingPrice"]
        
        for r in result:
          for i in range(0, 27):
            print(f"{table[i]}: {r[i]}")
          print("-------------------------------------------------------------")
        '''
        for r in result:
          tup = list(r[0:20])
          for i in range(21, 27):
            tup.append(r[i])
          tup.append(r[20])
          #print(tup)
          table.append(tup)
          '''
        #print(tabulate.tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

def show_top_cars_in_year():

    mydb = mysql.connector.connect(
        host = "db4free.net",
        user = "mohamedfekry",
        password = "forthirdmilestone",
        database = "mycarsdb")

    year = input("Enter the year you are interested in: ")

    mycursor = mydb.cursor()
    sql = """
    select Brand, Model, COUNT(*), AVG(Price) from ads WHERE Year = %s GROUP BY Brand, Model ORDER BY COUNT(*) DESC LIMIT 5;
    """
    
    mycursor.execute(sql, (year, ))

    result = mycursor.fetchall()

    if not result:
      print("\nThere are no available ads for this year.")

    else:
      if result[0][0] == None:
          print("\nThere are no available ads for this year.")
      else:
        print("\nThe top brands and models in this year are:\n")
        table = [["Brand", "Model", "# of cars", "AVG Price"]]
        
        for r in result:
          table.append(list(r))
          
        print(tabulate.tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    choice = input("\nEnter z to continue using the app or any other letter to exit: ")
    if choice == "z":
        interface()
    else:
        quit()

#register_user()
#add_user_sale()
#view_review()
#agg_seller_rating()
#show_ads()
#show_cars_loc_price()
#show_top_inventory_loc()
#show_top_listings_seller()
#show_ads_of_seller()
#show_top_cars_in_year()

interface()