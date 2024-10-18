#import pymysql # dummy
from mysql.connector import connect
import csv
import numpy as np

connection = connect(
    host = '###',
    port = 0,
    user = '###',
    password = '###',
    db = '###',
    charset = 'utf8'
)

cursor = connection.cursor(dictionary=True)

def get_movie_from_title(title):
    cursor.execute(f"SELECT id, price \
                    FROM movie \
                    WHERE title=\"{title}\"")
    return cursor.fetchall()

def get_movie_from_movie_id(movie_id):
    cursor.execute(f"SELECT *\
                    FROM movie\
                    WHERE id={movie_id}")
    return cursor.fetchall()

def get_user_from_name_age(name, age):
    cursor.execute(f"SELECT id \
                    FROM user \
                    WHERE name=\"{name}\" and age={age}")
    return cursor.fetchall()

def get_user_from_user_id(user_id):
    cursor.execute(f"SELECT *\
                    FROM user\
                    WHERE id={user_id}")
    return cursor.fetchall()

def get_reservation_from_ids(movie_id, user_id):
    cursor.execute(f"SELECT *\
                    FROM reservation\
                    WHERE movie_id={movie_id} and user_id={user_id}")
    return cursor.fetchall()

def get_reservation_from_movie_id(movie_id):
    cursor.execute(f"SELECT count(*) AS cnt\
                    FROM reservation\
                    WHERE movie_id={movie_id}")
    return cursor.fetchall()

def put_movie(title, director, price):
    cursor.execute(f"INSERT INTO movie(title, director, price)\
                    VALUES(\"{title}\", \"{director}\", {price})")
    return

def put_user(name, age, _class):
    cursor.execute(f"INSERT INTO user(name, age, class)\
                    VALUES(\"{name}\", {age}, \"{_class}\")")
    return

def put_reservation(movie_id, user_id, reserve_price):
    cursor.execute(f"INSERT INTO reservation\
                    VALUES({movie_id}, {user_id}, {reserve_price}, null)")
    return  

# Problem 1 (5 pt.)
def initialize_database():
    # YOUR CODE GOES HERE
    # make tables
    try:
        cursor.execute("CREATE TABLE movie (\
                            id int PRIMARY KEY AUTO_INCREMENT,\
                            title varchar(255),\
                            director varchar(255),\
                            price int,\
                            UNIQUE(title)\
                        )")
    except:
        pass

    try:
        cursor.execute("CREATE TABLE user (\
                            id int PRIMARY KEY AUTO_INCREMENT,\
                            name varchar(255) NOT NULL,\
                            age int NOT NULL,\
                            class varchar(255),\
                            UNIQUE(name, age)\
                        )")
    except:
        pass

    try:
        cursor.execute("CREATE TABLE reservation (\
                            movie_id int NOT NULL,\
                            user_id int NOT NULL,\
                            reserve_price int,\
                            rating int,\
                            PRIMARY KEY(movie_id, user_id),\
                            FOREIGN KEY(movie_id) REFERENCES movie(id) ON DELETE CASCADE,\
                            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE\
                        )")
    except:
        pass

    #return # for only remain table schema

    # open csv
    f = open('data.csv', 'r')
    reader = csv.reader(f)
    column_name = 0

    # insert data
    for line in reader:
        if column_name == 0:
            column_name = 1
            continue
        
        title, director, price, name, age, _class = line


        # check value error in line
        if (not price.isdecimal()) or int(price) < 0 or int(price) > 100000 or \
            (not age.isdecimal()) or int(age) < 12 or int(age) > 110 or (_class not in ['basic', 'premium', 'vip']):
            continue

        movie_id = -1
        user_id = -1
        reserve_price = -1


        # find the movie already exist
        result = get_movie_from_title(title)

        if len(result) == 1:
            movie_id = int(result[0]['id'])
            reserve_price = int(result[0]['price'])
        

        # find the user already exist
        result = get_user_from_name_age(name, age)

        if len(result) == 1:
            user_id = int(result[0]['id'])


        # check duplicate reservation
        if movie_id > 0 and user_id > 0:
            result = get_reservation_from_ids(movie_id, user_id)

            if len(result) > 0:
                continue


        # check fully booked
        if movie_id > 0:
            result = get_reservation_from_movie_id(movie_id)

            if int(result[0]['cnt']) >= 10:
                continue


        # insert data into movie if not exist
        if movie_id == -1:
            put_movie(title, director, price)

            result = get_movie_from_title(title)

            movie_id = int(result[0]['id'])
            reserve_price = int(result[0]['price'])


        # insert data into user if not exist
        if user_id == -1:
            put_user(name, age, _class)

            result = get_user_from_name_age(name, age)

            user_id = int(result[0]['id'])


        # insert data into reservation
        if _class == 'premium' :
            reserve_price = reserve_price * 3 // 4
        elif _class == 'vip' :
            reserve_price = reserve_price // 2

        put_reservation(movie_id, user_id, reserve_price)
            
    f.close()

    print('Database successfully initialized')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 15 (5 pt.)
def reset():
    # YOUR CODE GOES HERE

    r = input("Do you really want to reset DATABASE? (y/n) : ")

    if r not in ['y','Y']:
        return
    
    try:
        cursor.execute("DROP TABLE reservation")
    except:
        pass

    try:
        cursor.execute("DROP TABLE user")
    except:
        pass

    try:
        cursor.execute("DROP TABLE movie")
    except:
        pass

    initialize_database(); # make this to annotation for just reset

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 2 (4 pt.)
def print_movies():
    # YOUR CODE GOES HERE

    # get all columns
    cursor.execute("SELECT * \
                    FROM movie LEFT OUTER JOIN \
                        (SELECT movie_id, \
                            AVG(Cast(reserve_price as Float)) AS avg_price, \
                            count(*) AS reserve_num, \
                            AVG(Cast(rating as Float)) AS avg_rating\
                        FROM reservation\
                        GROUP BY movie_id) AS movies ON id = movie_id\
                    ORDER BY id ASC")
    result = cursor.fetchall()

    # print all columns
    print("------------------------------------------------------------------------------------------------------------------")
    print("id      title                         director                      price   avg. price   reservation   avg. rating")
    print("------------------------------------------------------------------------------------------------------------------")
    
    for data in result:
        print(str(data['id']).ljust(7), end = " ")
        print(data['title'].ljust(29), end = " ")
        print(data['director'].ljust(29), end = " ")
        print(str(data['price']).ljust(7), end = " ")

        # checking there is no reservation / rating

        if data['avg_price'] == None:
            print("None".rjust(10), end = "   ")
        else:
            print(format(round(float(data['avg_price']),2),'.2f').rjust(10), end = "   ")
        
        if data['reserve_num'] == None:
            print("0".rjust(11), end = "   ")
        else:
            print(str(data['reserve_num']).rjust(11), end = "   ")

        if data['avg_rating'] == None:
            print("None".rjust(11))
        else:
            print(format(round(float(data['avg_rating']),2),'.2f').rjust(11))

    print("------------------------------------------------------------------------------------------------------------------")

    # YOUR CODE GOES HERE
    pass

# Problem 3 (3 pt.)
def print_users():
    # YOUR CODE GOES HERE

    # get all columns
    cursor.execute("SELECT *\
                    FROM user\
                    ORDER BY id ASC")
    result = cursor.fetchall()

    # print all columns
    print("------------------------------------------------------------------------------------------------------------------")
    print("id      name                                                        age                  class                    ")
    print("------------------------------------------------------------------------------------------------------------------")
    
    for data in result:
        print(str(data['id']).ljust(7), end = " ")
        print(data['name'].ljust(59), end = " ")
        print(str(data['age']).ljust(20), end = " ")
        print(data['class'].ljust(25))

    print("------------------------------------------------------------------------------------------------------------------")
    
    # YOUR CODE GOES HERE
    pass

# Problem 4 (4 pt.)
def insert_movie():
    # YOUR CODE GOES HERE
    title = input('Movie title: ')
    director = input('Movie director: ')
    price = input('Movie price: ')

    # check duplicate title
    result = get_movie_from_title(title)

    if len(result) > 0:
        print(f'Movie {title} already exists')
        return
    
    # check price range
    if (not price.isdecimal()) or int(price) < 0 or int(price) > 100000:
        print('Movie price should be from 0 to 100000')
        return

    # put the data in
    put_movie(title, director, price)

    # success message
    print('One movie successfully inserted')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 6 (4 pt.)
def remove_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')

    # check movie exist
    result = get_movie_from_movie_id(movie_id)

    if len(result) == 0:
        print(f'Movie {movie_id} does not exist')
        return

    # delete from movie (also delete from reservation by on delete cascade)
    cursor.execute(f"DELETE FROM movie\
                    WHERE id={movie_id}")

    # success message
    print('One movie successfully removed')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 5 (4 pt.)
def insert_user():
    # YOUR CODE GOES HERE
    name = input('User name: ')
    age = input('User age: ')
    _class = input('User class: ')

    # check age range
    if (not age.isdecimal()) or int(age) < 12 or int(age) > 110:
        print('User age should be from 12 to 110')
        return

    # check duplicate user
    result = get_user_from_name_age(name, age)

    if len(result) > 0:
        print(f'User ({name}, {age}) already exists')
        return

    # check class
    if _class not in ['basic', 'premium', 'vip']:
        print('User class should be basic, premium or vip')
        return
    
    # put the data in
    put_user(name, age, _class)

    # success message
    print('One user successfully inserted')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 7 (4 pt.)
def remove_user():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return

    # delete from user (also delete from reservation by on delete cascade)
    cursor.execute(f"DELETE FROM user\
                    WHERE id={user_id}")

    # success message
    print('One user successfully removed')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 8 (5 pt.)
def book_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')
    user_id = input('User ID: ')


    # check title exist
    result = get_movie_from_movie_id(movie_id)

    if len(result) == 0:
        print(f'Movie {movie_id} does not exist')
        return

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return
    
    # check duplicate reservation
    result = get_reservation_from_ids(movie_id, user_id)

    if len(result) > 0:
        print(f'User {user_id} already booked movie {movie_id}')
        return

    # check fully booked
    result = get_reservation_from_movie_id(movie_id)

    if int(result[0]['cnt']) >= 10:
        print(f'Movie {movie_id} has already been fully booked')
        return

    # get informations and put data in
    result = get_movie_from_movie_id(movie_id)

    reserve_price = int(result[0]['price'])

    result = get_user_from_user_id(user_id)

    _class = result[0]['class']

    if _class == 'premium' :
        reserve_price = reserve_price * 3 // 4
    elif _class == 'vip' :
        reserve_price = reserve_price // 2

    put_reservation(movie_id, user_id, reserve_price)

    # success message
    print('Movie successfully booked')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 9 (5 pt.)
def rate_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')
    user_id = input('User ID: ')
    rating = input('Ratings (1~5): ')


    # check title exist
    result = get_movie_from_movie_id(movie_id)

    if len(result) == 0:
        print(f'Movie {movie_id} does not exist')
        return

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return

    # check rating range
    if (not rating.isdecimal()) or int(rating) < 1 or int(rating) > 5:
        print(f'Wrong value for a rating')
        return

    # check reservation & already rated
    result = get_reservation_from_ids(movie_id, user_id)

    if len(result) == 0:
        print(f'User {user_id} has not booked movie {movie_id} yet')
        return
    elif result[0]['rating'] != None:
        print(f'User {user_id} has already rated movie {movie_id}')
        return

    # update rating
    cursor.execute(f"UPDATE reservation\
                    SET rating = {rating}\
                    WHERE movie_id={movie_id} and user_id={user_id}")

    # success message
    print('Movie successfully rated')

    connection.commit()
    # YOUR CODE GOES HERE
    pass

# Problem 10 (5 pt.)
def print_users_for_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')

    # check title exist
    result = get_movie_from_movie_id(movie_id)

    if len(result) == 0:
        print(f'Movie {movie_id} does not exist')
        return

    # print users of the movie
    cursor.execute(f"SELECT *\
                    FROM reservation LEFT JOIN user ON user_id = id\
                    WHERE movie_id={movie_id}\
                    ORDER BY user_id ASC")
    result = cursor.fetchall()

    # print all columns
    print("------------------------------------------------------------------------------------------------------------------")
    print("id      name                                               age        res. price         rating                   ")
    print("------------------------------------------------------------------------------------------------------------------")
    
    for data in result:
        print(str(data['user_id']).ljust(7), end = " ")
        print(data['name'].ljust(50), end = " ")
        print(str(data['age']).ljust(10), end = " ")
        print(str(data['reserve_price']).ljust(18), end = " ")

        if data['rating'] == None:
            print("None".ljust(25))
        else:
            print(str(data['rating']).ljust(25))

    print("------------------------------------------------------------------------------------------------------------------")
    
    # YOUR CODE GOES HERE
    pass


# Problem 11 (5 pt.)
def print_movies_for_user():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return

    # print movies of the user
    cursor.execute(f"SELECT *\
                    FROM reservation LEFT JOIN movie ON movie_id = id\
                    WHERE user_id={user_id}\
                    ORDER BY movie_id ASC")
    result = cursor.fetchall()

    # print all columns
    print("------------------------------------------------------------------------------------------------------------------")
    print("id      title                          director                       res. price         rating                   ")
    print("------------------------------------------------------------------------------------------------------------------")

    for data in result:
        print(str(data['movie_id']).ljust(7), end = " ")
        print(data['title'].ljust(30), end = " ")
        print(data['director'].ljust(30), end = " ")
        print(str(data['reserve_price']).ljust(18), end = " ")

        if data['rating'] == None:
            print("None".ljust(25))
        else:
            print(str(data['rating']).ljust(25))

    print("------------------------------------------------------------------------------------------------------------------")

    # YOUR CODE GOES HERE
    pass

# Problem 12 (6 pt.)
def recommend_popularity():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return

    # get user class
    _class = result[0]['class']

    movie1 = []
    movie2 = []

    # get rating based recommend movie
    cursor.execute(f"SELECT * \
                    FROM movie LEFT OUTER JOIN \
                        (SELECT movie_id, \
                            count(*) AS reserve_num, \
                            AVG(Cast(rating as Float)) AS avg_rating\
                        FROM reservation\
                        GROUP BY movie_id) AS movies ON id = movie_id\
                    WHERE id not in (SELECT movie_id FROM reservation WHERE user_id={user_id})\
                    ORDER BY avg_rating IS NULL ASC, avg_rating DESC, id ASC")
    result = cursor.fetchall()

    if len(result) > 0:
        movie1 = result[0]

    # get popularity based recommend movie
    cursor.execute(f"SELECT * \
                    FROM movie LEFT OUTER JOIN \
                        (SELECT movie_id, \
                            count(*) AS reserve_num, \
                            AVG(Cast(rating as Float)) AS avg_rating\
                        FROM reservation\
                        GROUP BY movie_id) AS movies ON id = movie_id\
                    WHERE id not in (SELECT movie_id FROM reservation WHERE user_id={user_id})\
                    ORDER BY reserve_num DESC, id ASC")
    result = cursor.fetchall()

    if len(result) > 0:
        movie2 = result[0]


    # print recommend
    print("------------------------------------------------------------------------------------------------------------------")
    print("Rating-based")
    print("id      title                                                               res. price   reservation   avg. rating")
    print("------------------------------------------------------------------------------------------------------------------")

    if movie1 != []:
        print(str(movie1['id']).ljust(7), end = " ")
        print(movie1['title'].ljust(67), end = " ")

        if _class == "premium":
            movie1['price'] = movie1['price'] * 3 // 4
        elif _class == "vip":
            movie1['price'] = movie1['price'] // 2
        print(str(movie1['price']).rjust(10), end = "   ")

        if movie1['reserve_num'] == None:
            print("0".rjust(11), end = "   ")
        else:
            print(str(movie1['reserve_num']).rjust(11), end = "   ")

        if movie1['avg_rating'] == None:
            print("None".rjust(11))
        else:
            print(format(round(float(movie1['avg_rating']),2),'.2f').rjust(11))

    print("------------------------------------------------------------------------------------------------------------------")
    print("Popularity-based")
    print("id      title                                                               res. price   reservation   avg. rating")
    print("------------------------------------------------------------------------------------------------------------------")

    if movie2 != []:
        print(str(movie2['id']).ljust(7), end = " ")
        print(movie2['title'].ljust(67), end = " ")

        if _class == "premium":
            movie2['price'] = movie2['price'] * 3 // 4
        elif _class == "vip":
            movie2['price'] = movie2['price'] // 2
        print(str(movie2['price']).rjust(10), end = "   ")

        if movie2['reserve_num'] == None:
            print("0".rjust(11), end = "   ")
        else:
            print(str(movie2['reserve_num']).rjust(11), end = "   ")

        if movie2['avg_rating'] == None:
            print("None".rjust(11))
        else:
            print(format(round(float(movie2['avg_rating']),2),'.2f').rjust(11))

    print("------------------------------------------------------------------------------------------------------------------")

    # YOUR CODE GOES HERE
    pass


# Problem 13 (10 pt.)
def recommend_item_based():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')
    rec_count = input('Recommend Count: ')

    # check user exist
    result = get_user_from_user_id(user_id)

    if len(result) == 0:
        print(f'User {user_id} does not exist')
        return

    # get user class
    _class = result[0]['class']

    # added id to idx dict for fast index search
    users = []
    id_to_users_idx = {}    # user_id : user_idx
    movies = []
    id_to_movies_idx = {}   # movie_id : movie_idx

    # get users who rated
    cursor.execute("SELECT distinct user_id\
                    FROM reservation\
                    WHERE rating IS NOT NULL")
    result = cursor.fetchall()

    for data in result:
        id_to_users_idx[data['user_id']] = len(users)
        users.append(data['user_id'])

    # check the user rated any
    if int(user_id) not in users:
        print('Rating does not exist')
        return

    # get all movies
    cursor.execute("SELECT id\
                    FROM movie")
    result = cursor.fetchall()

    for data in result:
        id_to_movies_idx[data['id']] = len(movies)
        movies.append(data['id'])

    # initial table to 0
    origin_table = np.zeros((len(users), len(movies)))

    # apply rating into table
    cursor.execute("SELECT *\
                    FROM reservation\
                    WHERE rating IS NOT NULL")
    result = cursor.fetchall()

    for data in result:
        for_user_idx = id_to_users_idx[data['user_id']]
        for_movie_idx = id_to_movies_idx[data['movie_id']]
        for_rating = data['rating']

        origin_table[for_user_idx, for_movie_idx] = for_rating

    average_table = origin_table.copy() # table after put average in '0's, will be decr by 'total avg'
    average_vector = []

    # put average rating in '0's
    for j in range(0, len(movies)):
        rated = 0
        rating_sum = 0

        for i in range(0, len(users)):
            if average_table[i, j] > 0:
                rated = rated + 1
                rating_sum = rating_sum + average_table[i, j]

        if rated == 0:
            average_vector.append(0)
        else:
            average_vector.append(round(rating_sum / rated, 2))

        for i in range(0, len(users)):
            if average_table[i, j] == 0:
                average_table[i, j] = average_vector[j]

    # total average
    average = average_table.mean()

    diff_table = average_table - average
    square_table = diff_table * diff_table

    # sum of column
    sum_square_vector = square_table.sum(axis = 0)
    root_sum_square_vector = sum_square_vector ** 0.5

    # get similarity matrix
    similarity_matrix = np.zeros((len(movies), len(movies)))

    for i in range(0, len(movies)):
        for j in range(i, len(movies)):
            if i == j: # diagonal
                similarity_matrix[i, j] = 1
                continue
            numerator = (diff_table[:,i] * diff_table[:,j]).sum() # numerator
            denominator = root_sum_square_vector[i] * root_sum_square_vector[j]
            if denominator == 0:
                similarity_matrix[i,j] = 0
            else:
                similarity_matrix[i,j] = round(numerator / denominator, 4)
            similarity_matrix[j,i] = similarity_matrix[i,j]

    # get not seen movie of user
    cursor.execute(f"SELECT id\
                    FROM movie\
                    WHERE id not in (SELECT movie_id FROM reservation WHERE user_id={user_id})")
    result = cursor.fetchall()

    recommend = []

    for data in result:
        recommend.append([data['id'], 0])

    # calculate weighted sum
    user_idx = id_to_users_idx[int(user_id)]
    
    for i in range(0, len(recommend)):
        movie_idx = id_to_movies_idx[recommend[i][0]]
        
        numerator = 0
        denominator = 0

        for j in range(0, len(movies)):
            if j == movie_idx:
                continue
            numerator = numerator + average_table[user_idx, j] * similarity_matrix[movie_idx, j]
            denominator = denominator + similarity_matrix[movie_idx, j]

        if denominator == 0:
            recommend[i][1] = 0
        else:
            recommend[i][1] = round(numerator / denominator, 2)

    recommend = sorted(recommend, key=lambda x:(-x[1], x[0]))

    # print recommend movies
    print("------------------------------------------------------------------------------------------------------------------")
    print("id      title                                                           res. price   avg. rating   expected rating")
    print("------------------------------------------------------------------------------------------------------------------")

    for i in range(0, min(len(recommend), int(rec_count))):
        result = get_movie_from_movie_id(recommend[i][0])

        print(str(result[0]['id']).ljust(7), end = " ")
        print(result[0]['title'].ljust(63), end = " ")

        reserve_price = result[0]['price']
        if _class == "premium":
            reserve_price = reserve_price * 3 // 4
        elif _class == "vip":
            reserve_price = reserve_price // 2
        print(str(reserve_price).rjust(10), end = "   ")

        if average_vector[id_to_movies_idx[result[0]['id']]] == 0:
            print("None".rjust(11), end = "   ")
        else:
            print(format(average_vector[id_to_movies_idx[result[0]['id']]],'.2f').rjust(11), end = "   ")

        print(format(recommend[i][1], '.2f').rjust(15))

    print("------------------------------------------------------------------------------------------------------------------")
    
    # YOUR CODE GOES HERE
    pass


# Total of 70 pt.
def main():
    while True:
        print('============================================================')
        print('1. initialize database')
        print('2. print all movies')
        print('3. print all users')
        print('4. insert a new movie')
        print('5. remove a movie')
        print('6. insert a new user')
        print('7. remove an user')
        print('8. book a movie')
        print('9. rate a movie')
        print('10. print all users who booked for a movie')
        print('11. print all movies booked by an user')
        print('12. recommend a movie for a user using popularity-based method')
        print('13. recommend a movie for a user using item-based collaborative filtering')
        print('14. exit')
        print('15. reset database')
        print('============================================================')
        menu = int(input('Select your action: '))

        if menu == 1:
            initialize_database()
        elif menu == 2:
            print_movies()
        elif menu == 3:
            print_users()
        elif menu == 4:
            insert_movie()
        elif menu == 5:
            remove_movie()
        elif menu == 6:
            insert_user()
        elif menu == 7:
            remove_user()
        elif menu == 8:
            book_movie()
        elif menu == 9:
            rate_movie()
        elif menu == 10:
            print_users_for_movie()
        elif menu == 11:
            print_movies_for_user()
        elif menu == 12:
            recommend_popularity()
        elif menu == 13:
            recommend_item_based()
        elif menu == 14:
            print('Bye!')
            break
        elif menu == 15:
            reset()
        else:
            print('Invalid action')


if __name__ == "__main__":
    main()
    cursor.close()
    connection.commit()
    connection.close()
