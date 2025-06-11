    # Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'rental_properties.db'

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close()

TABLES = (" rental_properties "
            "LEFT JOIN suburb ON rental_properties.suburb_id = suburb.suburb_id "
            "LEFT JOIN type ON rental_properties.type_id = type.type_id "
            "LEFT JOIN pets ON rental_properties.pets_id = pets.pets_id ")


def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  

new_properties = []

menu_choice =''
while menu_choice != 'Z':
    menu_choice = input('Welcome to the Rental Properties database\n\n'
                        'Type the letter for the information you want:\n'
                        'A: All data\n'
                        'B: Cheap apartments\n'
                        'C: Cheap properties where you can either keep or negotiate pets\n'
                        'D: Properties with atleast 3 doublebeds\n'
                        'E: Properties with atleast 4 beds\n'
                        'F: Properties that have more than 2 parking spaces\n'
                        'G: Properties with the most amount of master beds\n'
                        'H: Total amount of beds for each property\n'
                        'I: Townhouses in Riccarton\n'
                        'J: Info about a specific street\n'
                        'K: Properties in a specific suburb\n'
                        'L: Add data for a new property\n'
                        'Z: Exit\n\nType option here: ')
    menu_choice = menu_choice.upper()
    if menu_choice == 'A':
        print_query('all_data')
    elif menu_choice == 'B':
        print_query('cheap_apart')
    elif menu_choice == 'C':
        print_query('cheap_pets')   
    elif menu_choice == 'D':    
        print_query('doublebed_3')
    elif menu_choice == 'E':
        print_query('has4_beds')
    elif menu_choice == 'F':
        print_query('more_parking')
    elif menu_choice == 'G':
        print_query('most_masterbeds')
    elif menu_choice == 'H':
        print_query('total_beds')
    elif menu_choice == 'I':
        print_query('townhouse_ricc')
    elif menu_choice == 'J':
        street_name = input("What street  do you want to know more about: ")
        print_parameter_query("street_no, street_name, suburb, type, masterbed_no, doublebed_no, singlebed_no, bathrooms, parking_space, pets, price_week",  "street_name = ?",street_name)
    elif menu_choice == 'K':
        suburb = input("What suburb do you want to know more about: ")
        print_parameter_query("street_no, street_name, suburb, type, masterbed_no, doublebed_no, singlebed_no, bathrooms, parking_space, pets, price_week",  "suburb = ?",suburb)
    elif menu_choice == 'L':
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()
        street_no = input("What is the street number, eg:15c, 11: ")
        new_properties.append(street_no)
        street_name = input("What is the street name, eg:Amelia Place: ")
        new_properties.append(street_name)
        suburb_id = int(input("What is the suburb id: "))
        new_properties.append(suburb_id)
        type_id = int(input("What is the property type id: "))
        new_properties.append(type_id)
        masterbed_no = int(input("What is the number of master beds in the property: "))
        new_properties.append(masterbed_no)
        doublebed_no = int(input("What is the number of double beds in the property: "))
        new_properties.append(doublebed_no)
        singlebed_no = int(input("What is the number of single beds in the property: "))
        new_properties.append(singlebed_no)
        bathrooms = int(input("What is the number of bathrooms in the property: "))
        new_properties.append(bathrooms)
        parking_space = int(input("How much parking space is available: "))
        new_properties.append(parking_space)
        pets_id = int(input("What is the pet id: "))
        new_properties.append(pets_id)
        price_week = int(input("What is the price charged per week: "))
        new_properties.append(price_week)
        a =  '''INSERT INTO rental_properties(street_no, street_name, suburb_id, type_id, masterbed_no,
                     doublebed_no, singlebed_no, bathrooms, parking_space, pets_id, price_week) 
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''

        cursor.execute(a,new_properties)
        db.commit()
        db.close()