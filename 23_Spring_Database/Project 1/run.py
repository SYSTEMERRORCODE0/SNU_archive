from lark import Lark, Transformer
from berkeleydb import db
from sys import exit

# open grammer.lark
with open('grammar.lark') as file:
    sql_parser = Lark(file.read(), start = "command", lexer = "basic")

#
#   tables                          : #max_number_of_tables
#   tablesnum                       : #number_of_tables
#   table-#number                   : tablename
#   tablename                       : None / True (if exist)
#   tablename-columns               : #max_number_of_columns (= number_of_columns)
#   #############################   : #number_of_columns - not necessary
#   tablename-primary               : columnname[-columnname]*
#   tablename-referencedby          : tablename[-tablename]*
#   tablename-data                  : #max_number_of_data
#   tablename-datanum               : #number_of_data
#   tablename-#number               : columnname
#   tablename-columnname            : None / True (if exist)
#   tablename-columnname-type       : int / char+N / date
#   tablename-columnname-notnull    : True / False
#   tablename-columnname-primary    : None / True
#   tablename-columnname-foreign    : None / tablename-columnname[+tablename-columnname]*
#   tablename-columnname-#number    : (data)
#
#   (No I won't now... ) MEMO : IF DELETE, I'll renumber the data
#

myDB = db.DB()
myDB.open('myDB.db', dbtype = db.DB_HASH, flags = db.DB_CREATE)
if myDB.get(b"tables") == None :
    myDB.put(b"tables", b"0")
    myDB.put(b"tablesnum", b"0")


''' Optimized db put/get '''

# myDB.put optimized
def dbput(k, v):
    key = k
    value = v
    if type(key).__name__ == 'int' :
        key = str(key)
    if type(value).__name__ == 'int' :
        value = str(value)
    if type(key).__name__ == 'bool' :
        key = str(key)
    if type(value).__name__ == 'bool' :
        value = str(value)

    key = key.encode('ascii')
    value = value.encode('ascii')
    myDB.put(key, value)

# myDB.get optimized returns string
def dbget(k):
    key = k
    if type(key).__name__ == 'int' :
        key = str(key)

    key = key.encode('ascii')
    try :
        value = myDB.get(key).decode('ascii')
    except :
        return None

    return value



''' for checking key value together in db '''

def byteTupleToStringList(data):
    key = data[0].decode('ascii')
    value = data[1].decode('ascii')

    return [key, value]





##############test in,out
'''
dbput(1435, 376)
print(dbget(1435))
'''
def printAll():
    cursor = myDB.cursor()
    x = cursor.first()

    while x != None:
        print(x)
        x = cursor.next()

########################
#printAll()



''' print functions '''

# print prompt
def printPrompt():
    print("DB_2019-18499> ", end='')

# print requests
def printRequest(query):
    printPrompt()
    print(f'\'{query}\' requested')

# print errors
def printError(error_code):
    printPrompt()
    error_code_list = error_code.split(':')
    error = ""
    name = ""
    error = error_code_list[0]
    if len(error_code_list) > 1 :
        name = error_code_list[1]

    if error == "CreateTableSuccess" :
        print(f'\'{name}\' table is created')
    elif error == "DropSuccess" :
        print(f'\'{name}\' table is dropped')
    elif error == "InsertResult" :
        print('The row is inserted')
    elif error == "DuplicateColumnDefError" :
        print("Create table has failed: column definition is duplicated")
    elif error == "DuplicatePrimaryKeyDefError" :
        print("Create table has failed: primary key definition is duplicated")
    elif error == "ReferenceTypeError" :
        print("Create table has failed: foreign key references wrong type")
    elif error == "ReferenceNonPrimaryKeyError" :
        print("Create table has failed: foreign key references non primary key column")
    elif error == "ReferenceColumnExistenceError" :
        print("Create table has failed: foreign key references non existing column")
    elif error == "ReferenceTableExistenceError" :
        print("Create table has failed: foreign key references non existing table")
    elif error == "NonExistingColumnDefError" :
        print(f'Create table has failed: \'{name}\' does not exist in column definition')
    elif error == "TableExistenceError" :
        print("Create table has failed: table with the same name already exists")
    elif error == "CharLengthError" :
        print("Char length should be over 0")
    elif error == "DropSuccess" :
        print(f'\'{name}\' table is dropped')
    elif error == "NoSuchTable" :
        print("No such table")
    elif error == "DropReferencedTableError" :
        print(f'Drop table has failed: \'{name}\' is referenced by other table')
    elif error == "InsertResult" :
        print("The row is inserted")
    elif error == "SelectTableExistenceError" :
        print(f'Selection has failed: \'{name}\' does not exist')
    elif error == "SyntaxError" :
        print("Syntax error")
    elif error == "InsertTypeMismatchError" :
        print("Insertion has failed: Types are not matched")
    elif error == "InsertColumnExistenceError" :
        print(f"Insertion has failed: \'{name}\' does not exist")
    elif error == "InsertColumnNonNullableError" : 
        print(f"Insertion has failed: \'{name}\' is not nullable")
    elif error == "DeleteResult" :
        print(f"\'{name}\' row(s) are deleted")
    elif error == "SelectColumnResolveError" :
        print(f"Selection has failed: fail to resolve \'{name}\'")
    elif error == "WhereIncomparableError" :
        print("Where clause trying to compare incomparable values")
    elif error == "WhereTableNotSpecified" :
        print("Where clause trying to reference tables which are not specified")
    elif error == "WhereColumnNotExist" :
        print("Where clause trying to reference non existing column")
    elif error == "WhereAmbiguousReference" :
        print("Where clause contains ambiguous reference")



''' explain / describe / desc '''

def explainDescribe(items) :
    #
    #   Requirement : table_name
    #
    table_name = items[1].children[0].lower()

    #   check errors
    if dbget(table_name) == None :
        printError("NoSuchTable")
        return

    #   print columns
    print("--------------------------------------------------------------------------------")
    print(f'table_name [{table_name}]')
    print("column_name".ljust(31), "type".ljust(15), "null".ljust(15), "key".ljust(15))
    column_num = int(dbget(table_name + "-columns"))
    for i in range(0, column_num) :
        #   name
        column_name = dbget(table_name + "-" + str(i))

        column_type = dbget(table_name + "-" + column_name + "-type")
        #   char
        if column_type.split('+')[0] == "char" :
            column_type = "char(" + column_type.split('+')[1] + ")"

        #   null
        column_null = ""
        if dbget(table_name + "-" + column_name + "-notnull") == "True" :
            column_null = "N"
        else :
            column_null = "Y"

        #   key
        column_key = ""
        if dbget(table_name + "-" + column_name + "-primary") != None :
            column_key = "PRI"
        if dbget(table_name + "-" + column_name + "-foreign") != None :
            if column_key == "" :
                column_key = "FOR"
            else :
                column_key = "PRI/FOR"

        print(column_name.ljust(31), column_type.ljust(15), column_null.ljust(15), column_key.ljust(15))
    print("--------------------------------------------------------------------------------")


#   if the value type is string start of "@", that means not a table, return error (is True)
def check_error(value) :
    if type(value) == str and value[0] == '@' :
        return True
    return False

#   get all data in table
def getTable(table_name) :
    # collect columns
    column_num = int(dbget(table_name + "-columns"))
    column_list = ["0,index"] # this name can't be normal columns : for checking index for where clause
    column_type = ["int"]
    column_avail = ["True"]
    for i in range(0, column_num) :
        column_list.append(dbget(table_name + "-" + str(i)))
        column_type.append(dbget(table_name + "-" + column_list[i+1] + "-type"))

    # collect data
    data = []
    data_max_num = int(dbget(table_name + "-data"))
    for i in range(0, data_max_num) :
        a_data = [i]
        for column_name in column_list :
            if column_name == "0,index" :
                continue
            # no data this number
            a_dataget = dbget(table_name + "-" + column_name + "-" + str(i))
            if a_dataget == None :
                break
            a_data.append(a_dataget)
        # if there is record, collect
        if len(a_data) > 1:
            data.append(a_data)
            column_avail.append("True")

    return [[table_name], column_list, data, column_type, column_avail]

#   print all data in table : [table_name, column_list, data]
def printTable(table) :
    column_list = table[1]
    column_num = len(column_list)
    index_list = []
    data = table[2]

    # collect length for print
    length_list = []
    index = 0

    for column_name in column_list :
        index = index + 1
        if column_name.endswith("0,index") :   # column name for check index
            length_list.append(0)
            index_list.append(index - 1)
            continue
        column_name_length = len(column_name)
        column_type_length = 0

        column_type = table[3][index - 1]
        column_main_type = column_type.split('+')[0]
        if column_main_type == "char" :
            column_type_length = int(column_type.split('+')[1])
        else :
            column_type_length = 10

        length_list.append(max(column_name_length, column_type_length))

    ######################### print ########################
    for i in range(0, column_num) :
        if i in index_list :
            continue
        print("+", end = "")
        print("-" * (length_list[i] + 2), end = "")
    print("+")

    # column
    for i in range(0, column_num) :
        if i in index_list :
            continue
        print("| ", end = "")
        print(column_list[i].ljust(length_list[i]), end = "")
        print(" ", end = "")
    print("|")

    for i in range(0, column_num) :
        if i in index_list :
            continue
        print("+", end = "")
        print("-" * (length_list[i] + 2), end = "")
    print("+")

    # data
    index = 0
    for a_data in data :
        if table[4][index] != "True" :
            index = index + 1
            continue
        index = index + 1
        for i in range(0, column_num) :
            if i in index_list :
                continue
            print("| ", end = "")
            if a_data[i] == "" :
                print("null".ljust(length_list[i]), end = "")
            else :
                print(a_data[i].ljust(length_list[i]), end = "")
            print(" ", end = "")
        print("|")

    for i in range(0, column_num) :
        if i in index_list :
            continue
        print("+", end = "")
        print("-" * (length_list[i] + 2), end = "")
    print("+")

#   processing where clause
def where_process(table, where_clause) :
    boolean_expr = where_clause.children[1]
    return boolean_process_expr(table, boolean_expr)

#   OR
def boolean_process_expr(table, expression) :
    # return table1 = table1 [or table2]*
    table1 = boolean_process_term(table, expression.children[0])
    if check_error(table1) :
        return table1

    # check error of [AND], then calculate ["OR"]
    for i in range(1,len(expression.children),2) :
        if expression.children[i] != None :
            table2 = boolean_process_term(table, expression.children[i+1])
            if check_error(table2) :
                return table2

            for i in range(0,len(table2[2])) :
                if table1[4][i] == "True" or table2[4][i] == "True" :
                    table1[4][i] = "True"
                elif table1[4][i] == "False" and table2[4][i] == "False" :
                    table1[4][i] = "False"
                else :
                    table1[4][i] = "Unknown"

    return table1

#   AND
def boolean_process_term(table, expression) :
    # return table1 = table1 [and table2]*
    table1 = boolean_process_factor(table, expression.children[0])
    if check_error(table1) :
        return table1

    # check error of [NOT], then calculate ["AND"]
    for i in range(1,len(expression.children),2) :
        if expression.children[i] != None :
            table2 = boolean_process_factor(table, expression.children[i+1])
            if check_error(table2) :
                return table2

            for i in range(0,len(table2[2])) :
                if table1[4][i] == "True" and table2[4][i] == "True" :
                    table1[4][i] = "True"
                elif table1[4][i] == "False" or table2[4][i] == "False" :
                    table1[4][i] = "False"
                else :
                    table1[4][i] = "Unknown"

    return table1

#   NOT
def boolean_process_factor(table, expression) :
    # return table1 = [not] table1 
    table1 = []
    if expression.children[0] == None :
        table1 = boolean_process_test(table, expression.children[1])
        return table1
    else :  # Not
        table1 = boolean_process_test(table, expression.children[1])
        if check_error(table1) :
            return table1
        processing_table = [table1[0],table1[1],table1[2],table1[3],[]]

        # reverse the result (T -> F, F -> T, U -> U)
        for TF in table1[4] :
            if TF == "True" :
                processing_table[4].append("False")
            elif TF == "False" :
                processing_table[4].append("True")
            else :
                processing_table[4].append("Unknown")

        table1 = processing_table

    return table1

#   Predicate or Parenthesized
def boolean_process_test(table, expression) :
    if expression.children[0].data == "predicate" :
        table1 = predicate_process(table, expression.children[0])
        return table1
    else :  # Parenthesized
        # loop into boolean_expr
        table1 = boolean_process_expr(table, expression.children[0].children[1])
        return table1

def predicate_process(table, expression) :
    if expression.children[0].data == "comparison_predicate" :
        table1 = comparison_predicate_process(table, expression.children[0])
        return table1
    else :  # null_predicate
        table1 = null_predicate_process(table, expression.children[0])
        return table1

def comparison_predicate_process(table, expression) :

    # collect raw 2 operands, operator
    operand1 = comp_operand_process(table, expression.children[0])
    if check_error(operand1) :
        return operand1
    operator = expression.children[1].children[0]
    operand2 = comp_operand_process(table, expression.children[2])
    if check_error(operand2) :
        return operand2

    op1_idx = 0
    op1_type = ""
    op2_idx = 0
    op2_type = ""

    # collect operand1 type
    if type(operand1) != list : # int, char, date
        if operand1.lstrip('-').isnumeric() :
            op1_type = "int"
        elif len(operand1.split('-')) == 3 :
            op1_type = "date"
        else :
            op1_type = "char"
            operand1 = operand1[1:-1]
    else :  # column type, collect idx
        op1_idx = operand1[0]
        op1_type = table[3][op1_idx].split("+")[0]

    # collect operand2 type
    if type(operand2) != list : # int, char, date
        if operand2.lstrip('-').isnumeric() :
            op2_type = "int"
        elif len(operand2.split('-')) == 3 :
            op2_type = "date"
        else :
            op2_type = "char"
            operand2 = operand2[1:-1]
    else :  # column type, collect idx
        op2_idx = operand2[0]
        op2_type = table[3][op2_idx].split("+")[0]
        
    # calculate the comparison, idx == 0 means comparable value, != 0 means data
    table1 = [table[0],table[1],table[2],table[3],[]]
    for data in table1[2]:
        op1 = ""
        op2 = ""
        if op1_idx == 0 :
            op1 = operand1
        else :
            op1 = data[op1_idx]

        if op2_idx == 0 :
            op2 = operand2
        else :
            op2 = data[op2_idx]

        # check comparable, then compare
        if op1 == "" or op2 == "" :
            table1[4].append("Unknown")
        elif op1_type != op2_type :
            return "@error:WhereIncomparableError"
        else :
            if op1_type == "int" :
                op1 = int(op1)
                op2 = int(op2)
            
            if operator == ">" :
                table1[4].append(str(op1>op2))
            elif operator == "<" :
                table1[4].append(str(op1<op2))
            elif operator == "=" :
                table1[4].append(str(op1==op2))
            elif operator == "!=" :
                table1[4].append(str(op1!=op2))
            elif operator == ">=" :
                table1[4].append(str(op1>=op2))
            elif operator == "<=" :
                table1[4].append(str(op1<=op2))

    return table1


def comp_operand_process(table, expression) :
    if expression.children[0] != None and expression.children[0].data == "comparable_value" :
        return expression.children[0].children[0].lower()
    else :  # [table_name.]column_name : return list for divide from comparable_value
        table_name = ""
        column_name = ""
        if expression.children[0] != None :    # find table name
            table_name = expression.children[0].children[0].lower()

            ok = 0
            for table_i in table[0] :
                if table_i == table_name :
                    ok = 1
            # No table name
            if ok == 0 :
                return "@error:WhereTableNotSpecified"

        column_name = expression.children[1].children[0].lower()

        # check column
        column_idx = 0
        for i in range(0, len(table[1])) :
            column_i = table[1][i].split(".")
            if len(column_i) == 2 and (column_i[0] == table_name or table_name == "") and column_i[1] == column_name :
                # same column name -> ambiguous
                if column_idx != 0 :
                    return "@error:WhereAmbiguousReference"
                column_idx = i
            if len(column_i) == 1 and column_i[0] == column_name :
                # same column name -> ambiguous
                if column_idx != 0 :
                    return "@error:WhereAmbiguousReference"
                column_idx = i

        # No column found
        if column_idx == 0 :
            return "@error:WhereColumnNotExist"

        return [column_idx]

def null_predicate_process(table, expression) :
    table_name = ""
    column_name = ""
    null = False

    # collect elements in null predicate
    if expression.children[0] != None :
        table_name = expression.children[0].children[0].lower()
        ok = 0
        for table_i in table[0] :
            if table_i == table_name :
                ok = 1
        # No table name
        if ok == 0 :
            return "@error:WhereTableNotSpecified"
    column_name = expression.children[1].children[0].lower()

    if expression.children[2].children[1] == None :
        null = True

    # find the column
    column_idx = 0
    for i in range(0, len(table[1])) :
        column_i = table[1][i].split(".")
        if len(column_i) == 2 and (column_i[0] == table_name or table_name == "") and column_i[1] == column_name :
            # same column name -> ambiguous
            if column_idx != 0 :
                return "@error:WhereAmbiguousReference"
            column_idx = i
        if len(column_i) == 1 and column_i[0] == column_name :
            # same column name -> ambiguous
            if column_idx != 0 :
                return "@error:WhereAmbiguousReference"
            column_idx = i

    # No column found
    if column_idx == 0 :
        return "@error:WhereColumnNotExist"

    # collect data
    table1 = [table[0],table[1],table[2],table[3],[]]
    for data in table[2] :
        if null == False and data[column_idx] != "" :
            table1[4].append("True")
        elif null == True and data[column_idx] == "" :
            table1[4].append("True")
        else :
            table1[4].append("False")

    return table1


def select_process(table, select_columns) :
    table1 = [table[0],["0,index"],[],["int"],table[4]]

    # add index value into table1
    for data in table[2] :
        table1[2].append([data[0]])

    for select_column in select_columns :

        # divide select_column into table/column_name
        select_table_name = ""
        select_column_name = ""
        if len(select_column.split('.')) == 2 :
            select_table_name = select_column.split('.')[0]
            select_column_name = select_column.split('.')[1]
        else :
            select_column_name = select_column

        # check if table_name exists
        if select_table_name != "" :
            exist = 0
            for table_name in table[0] :
                if select_table_name == table_name :
                    exist = 1
            if exist == 0 :
                return f"@error:SelectColumnResolveError:{select_column}"
        
        # check if column_name exists
        idx = 0
        now_idx = -1
        for column in table[1] :
            now_idx = now_idx + 1
            if len(column.split('.')) == 2 :
                if (select_table_name == "" or select_table_name == column.split('.')[0]) and select_column_name == column.split('.')[1] :
                    if idx != 0 :   # already have that
                        return f"@error:SelectColumnResolveError:{select_column}"
                    idx = now_idx
                else :
                    pass
            else :
                if select_column_name == column :
                    if idx != 0:    # already have that
                        return f"@error:SelectColumnResolveError:{select_column}"
                    idx = now_idx
                else :
                    pass

        # no column exist
        if idx == 0 :
            return f"@error:SelectColumnResolveError:{select_column}"

        # collect data of selected columns
        table1[1].append(select_column)
        table1[3].append(table[3][idx])

        for i in range(0,len(table[2])) :
            table1[2][i].append(table[2][i][idx])
    
    return table1

def joinTable(table1, table2) :
    table = [table1[0],["0,index"],[],["int"],[]]

    # collect column table1
    if len(table1[0]) == 1:
        for i in range(1,len(table1[1])) :
            column_name = table1[1][i]
            table[1].append(table1[0][0] + "." + column_name)
            table[3].append(table1[3][i])
    else :
        for i in range(1,len(table1[1])) :
            column_name = table1[1][i]
            table[1].append(column_name)
            table[3].append(table1[3][i])

    # collect column table2
    for i in range(1,len(table2[1])) :
        column_name = table2[1][i]
        table[1].append(table2[0][0] + "." + column_name)
        table[3].append(table2[3][i])

    # collect data
    index = 0
    for data1 in table1[2] :
        data1 = data1[1:]
        for data2 in table2[2] :

            tot_data = [index]
            data2 = data2[1:]

            tot_data.extend(data1)
            tot_data.extend(data2)
            table[2].append(tot_data)
            table[4].append("True")

            index = index + 1

    # join tables
    table[0].append(table2[0][0])

    return table

# commands will run in here 
class MyTransformer(Transformer):
    def create_table_query(self, items):
        
        #
        #   Requirement : table_name, columns, primary_keys, foreign_keys_list
        #
        table_name = items[2].children[0].lower()
        column_definition_iter = items[3].find_data("column_definition")
        table_constraint_definition_iter = items[3].find_data("table_constraint_definition")

        #   collect column definition
        #   columns = list of 'column' dictionary
        columns = []
        for x in column_definition_iter:
            column_name = next(x.find_data("column_name")).children[0].lower()
            column_type = next(x.find_data("data_type")).children[0].lower()
            if column_type == "char" :
                length = next(x.find_data("data_type")).children[2]
                if int(length) <= 0 :
                    printError("CharLengthError")
                    return
                column_type = column_type + "+" + length
            
            column = {'column_name' : column_name, 'column_type' : column_type}

            #   check not null
            if x.children[2] != None and x.children[2].lower() + x.children[3].lower() == "notnull" :
                column['notnull'] = True
            else :
                column['notnull'] = False

            columns.append(column)

        #   check duplicate column definition
        column_num = len(columns)
        for i in range(1, column_num):
            for j in range(0, i):
                if columns[i]['column_name'] == columns[j]['column_name']:
                    printError("DuplicateColumnDefError")
                    return

        #   collect table constraint definition
        #   primary_keys : list of column
        #   foreign_keys_list : list of dict of "column : table-column"
        primary_keys = []
        foreign_keys_list = []
        for x in table_constraint_definition_iter:
            if x.children[0].children[0].lower() == "primary" :
                #   check duplicate primary key
                if len(primary_keys) > 0 :
                    printError("DuplicatePrimaryKeyDefError")
                    return
                column_name_iter = x.children[0].children[2].find_data("column_name")
                for col_name in column_name_iter :
                    primary_keys.append(col_name.children[0].lower())

            else :
                column_name_iter = x.children[0].children[2].find_data("column_name")
                ref_table_name = x.children[0].children[4].children[0].lower()
                ref_column_name_iter = x.children[0].children[5].find_data("column_name")
                
                col_names = []
                idx = 0
                n = 0
                for col_name in column_name_iter :
                    col_names.append(col_name.children[0].lower())
                    n = n + 1

                foreign_keys = {}
                # if ref multiple keys are ok, this must be change
                for ref_col_name in ref_column_name_iter :
                    #   over referencing ?
                    if idx > n :
                        printError("NonExistingColumnDefError:")
                        return
                    foreign_keys[col_names[idx]] = ref_table_name + "-" + ref_col_name.children[0].lower()
                    idx = idx + 1

                foreign_keys_list.append(foreign_keys)

                #   deficient referencing ?
                if idx < n :
                    printError("ReferenceColumnExistenceError")
                    return

        #   check primary key column exist
        for primary_key in primary_keys :
            exist = 0
            for column in columns :
                if column['column_name'] == primary_key :
                    exist = 1
                    break
            if exist == 0 :
                printError(f'NonExistingColumnDefError:{primary_key}')
                return

        #   check foreign key column exist
        for foreign_keys in foreign_keys_list :
            exist = 0
            for foreign_key in foreign_keys.keys() :
                for column in columns :
                    if column['column_name'] == foreign_key :
                        exist = 1
                        break
                if exist == 0 :
                    printError(f'NonExistingColumnDefError:{foreign_key}')
                    return

        #   check table already exists
        if dbget(table_name) != None :
            printError("TableExistenceError")
            return
                
        #   check foreign referenced table & column existence, primary, type
        for foreign_keys in foreign_keys_list :
            ### existence
            referenced_keys = list(foreign_keys.values())
            for referenced_key in referenced_keys :
                referenced_table_name = referenced_key.split('-')[0]
                referenced_column_name = referenced_key.split('-')[1]

                if dbget(referenced_table_name) == None :
                    printError("ReferenceTableExistenceError")
                    return

                if dbget(referenced_table_name + "-" + referenced_column_name) == None :
                    printError("ReferenceColumnExistenceError")
                    return

            ### reference primary
            referenced_table_name = referenced_keys[0].split('-')[0]
            referenced_table_primary_keys = dbget(referenced_table_name + "-primary")
            if referenced_table_primary_keys == None:
                printError("ReferenceNonPrimaryKeyError")
                return
            referenced_table_primary_keys_list = referenced_table_primary_keys.split('-')

            # Is foreign key referenced non-primary key?
            for referenced_key in referenced_keys :
                exist = 0
                for referenced_table_primary_key in referenced_table_primary_keys_list :
                    if referenced_table_primary_key == referenced_key.split('-')[1]:
                        exist = 1
                        break
                if exist == 0 :
                    printError("ReferenceNonPrimaryKeyError")
                    return
                    
            # Is foreign key referenced part of composite primary key?
            for referenced_table_primary_key in referenced_table_primary_keys_list :
                exist = 0
                for referenced_key in referenced_keys :
                    if referenced_table_primary_key == referenced_key.split('-')[1]:
                        exist = 1
                        break
                if exist == 0 :
                    printError("ReferenceNonPrimaryKeyError")
                    return

            ### type
            for foreign_key, referenced_key in foreign_keys.items() :

                # type
                for column in columns :
                    if column['column_name'] != foreign_key :
                        continue
                    ref_type = dbget(referenced_key + "-type")
                    if column['column_type'] != ref_type :
                        printError("ReferenceTypeError")
                        return

        # have table_name, columns, primary_keys, foreign_keys_list
        ############### put in db ####################
        tables_max_num = int(dbget("tables"))
        tables_num = int(dbget("tablesnum"))
        dbput("tables", tables_max_num + 1)
        dbput("tablesnum", tables_num + 1)
        
        dbput("table-" + str(tables_num), table_name)

        dbput(table_name, True)

        dbput(table_name + "-columns", len(columns))

        if len(primary_keys) > 0:
            dbput(table_name + "-primary", '-'.join(primary_keys))

        dbput(table_name + "-data", 0)
        dbput(table_name + "-datanum", 0)

        # column characteristic
        for i in range(0, len(columns)) :
            dbput(table_name + "-" + str(i), columns[i]['column_name'])
            dbput(table_name + "-" + columns[i]['column_name'], True)
            dbput(table_name + "-" + columns[i]['column_name'] + "-type", columns[i]['column_type'])
            dbput(table_name + "-" + columns[i]['column_name'] + "-notnull", columns[i]['notnull'])

        for primary_key in primary_keys :
            dbput(table_name + "-" + primary_key + "-primary", True)
            dbput(table_name + "-" + primary_key + "-notnull", True)    # primary -> not null

        referenced_tables = []
        for foreign_keys in foreign_keys_list :
            for foreign_key, referenced_key in foreign_keys.items() :
                referenced_tables.append(referenced_key.split('-')[0])
                if dbget(table_name + "-" + foreign_key + "-foreign") == None :
                    dbput(table_name + "-" + foreign_key + "-foreign", referenced_key)
                else :
                    dbput(table_name + "-" + foreign_key + "-foreign", dbget(table_name + "-" + foreign_key + "-foreign") + "+" + referenced_key)
        
        # to record referenced by this table
        referenced_tables = set(referenced_tables)
        referenced_tables = list(referenced_tables)
        for referenced_table in referenced_tables :
            if dbget(referenced_table + "-referencedby") == None :
                dbput(referenced_table + "-referencedby", table_name)
            else :
                dbput(referenced_table + "-referencedby", dbget(referenced_table + "-referencedby") + "-" + table_name)
        ##############################################

        printError(f"CreateTableSuccess:{table_name}")


        
        
    def select_query(self, items):
        
        #
        #   Requirement : selected_column / is_star, table_name_list FROM from_clause, [where_clause]
        #
        selected_column_iter = items[1].find_data("selected_column")

        #   collect select_columns(list) and check '*'
        select_column_list = []
        is_star = True
        for selected_column in selected_column_iter :
            select_column = ""
            if selected_column.children[0] != None:
                select_column = selected_column.children[0].children[0].lower() + "."
            select_column = select_column + selected_column.children[1].children[0].lower()

            select_column_list.append(select_column)
            is_star = False
            pass
            
        #   collect table_names in from clause
        referred_table_iter = items[2].children[0].children[1].find_data("referred_table")
        table_name_list = []
        for referred_table in referred_table_iter :
            table_origin_name = referred_table.children[0].children[0].lower()
            table_change_name = ""
            try :
                table_change_name = referred_table.children[2].children[0].lower()
            except :
                table_change_name = table_origin_name

            table_name_list.append(table_origin_name + ":" + table_change_name)
        
        processed_table = []
        #   check table_name in from clause
        for i in range(0,len(table_name_list)) :
            table_name = table_name_list[i].split(':')[0]
            if dbget(table_name) == None :
                printError(f"SelectTableExistenceError:{table_name}")
                return

            add_table = getTable(table_name)

            change_table_name = table_name_list[i].split(':')[1]
            if change_table_name != "" :
                add_table[0][0] = change_table_name

            if i == 0 :
                processed_table = add_table
            else :
                processed_table = joinTable(processed_table, add_table)

        #   run where clause
        where_clause = items[2].children[1]
        if where_clause != None :
            processed_table = where_process(processed_table, where_clause)

        #   check error of normal/[where clause]
        if check_error(processed_table) :
            printError(processed_table.split(':')[1])
            return

        #   run select clause after from, where clause
        if is_star == False :
            processed_table = select_process(processed_table, select_column_list)

            #   check error of select clause
            if check_error(processed_table) :
                printError(processed_table.lstrip('@error:'))
                return

        printTable(processed_table)
        


    def insert_query(self, items):
        
        #
        #   Requirement : table_name, [column_name_list], values_element_list
        #
        table_name = items[2].children[0].lower()

        #   check errors
        if dbget(table_name) == None :
            printError("NoSuchTable")
            return

        #   get columns in list
        column_num = int(dbget(table_name + "-columns"))
        columns = []
        column_type = {}
        column_notnull = {}
        column_primary = {}
        column_foreign = {}
        data = {}
        for i in range(0, column_num) :
            column_name = dbget(table_name + "-" + str(i))
            columns.append(column_name)
            column_type[column_name] = dbget(table_name + "-" + column_name + "-type")
            column_notnull[column_name] = dbget(table_name + "-" + column_name + "-notnull")
            column_primary[column_name] = dbget(table_name + "-" + column_name + "-primary")
            column_foreign[column_name] = dbget(table_name + "-" + column_name + "-foreign")
            data[column_name] = ""

        #   column_name_list is partial when table_name(column names...) comes
        column_name_list = []
        values_element_list = []
        
        #   collect values
        values_element_iter = items[5].find_data("values_element")

        for values_element in values_element_iter :
            values_element_list.append(values_element.children[0].lower())

        #   check is there column_name_list
        if items[3] != None :
            column_name_iter = items[3].find_data("column_name")           

            for column_name in column_name_iter :
                # if there is no column_name in table
                if column_name.children[0].lower() not in columns :
                    printError(f"InsertColumnExistenceError:{column_name.children[0].lower()}")
                    return
                column_name_list.append(column_name.children[0].lower())
        else :
            for i in range(0, column_num) :
                column_name_list.append(columns[i])

        #   over / deficient values : error
        if len(column_name_list) != len(values_element_list) :
            printError("InsertTypeMismatchError")
            return

        #   make data dictionary
        for i in range(0, len(column_name_list)) :
            column_name = column_name_list[i]
            values_element = values_element_list[i]

            # int
            if column_type[column_name].split('+')[0] == "int" :
                if values_element.lstrip('-').isnumeric() :
                    pass
                elif values_element == "null" :
                    values_element = ""
                    pass
                else :
                    printError("InsertTypeMismatchError")
                    return

            # char & truncate
            if column_type[column_name].split('+')[0] == "char" :
                if values_element[0] == values_element[-1] and (values_element[0] == '"' or values_element[0] == "'") :
                    char_length = int(column_type[column_name].split('+')[1])
                    char_value = values_element[1:-1]
                    values_element = char_value[0:char_length] if len(char_value) > char_length else char_value
                elif values_element == "null" :
                    values_element = ""
                    pass
                else :
                    printError("InsertTypeMismatchError")
                    return

            # date
            if column_type[column_name].split('+')[0] == "date" :
                date_temp = values_element.split('-')
                if len(date_temp) == 3 and len(date_temp[0]) == 4 and len(date_temp[1]) == 2 and len(date_temp[2]) == 2 :
                    pass
                elif values_element == "null" :
                    values_element = ""
                    pass
                else :
                    printError("InsertTypeMismatchError")
                    return

            data[column_name] = values_element

        # check non-nullable
        for column_name, value in data.items() :
            if value == "" and column_notnull[column_name] == "True":
                printError(f"InsertColumnNonNullableError:{column_name}")
                return

        #   put into db
        data_max_num = int(dbget(table_name + "-data"))
        data_num = int(dbget(table_name + "-datanum"))

        for column_name, value in data.items() :
            dbput(table_name + "-" + column_name + "-" + str(data_max_num), value)

        dbput(table_name + "-data", data_max_num + 1)
        dbput(table_name + "-datanum", data_num + 1)

        printError("InsertResult")



    def drop_table_query(self, items):
        
        #
        #   Requirement : table_name
        #
        table_name = items[2].children[0].lower()

        #   check errors
        if dbget(table_name) == None :
            printError("NoSuchTable")
            return

        if dbget(table_name + "-referencedby") != None :
            printError(f"DropReferencedTableError:{table_name}")
            return

        cursor = myDB.cursor()
        x = cursor.next()

        #   keys starting with tablename
        while x != None:
            key, value = byteTupleToStringList(x)
            if key.split('-')[0] == table_name :
                del myDB[key.encode('ascii')]
            x = cursor.next()

        #   delete from {table-number : tablename}
        table_max_num = int(dbget("tables"))
        for i in range(0, table_max_num) :
            table = dbget("table-" + str(i))
            if table == None :
                continue
            if table == table_name :
                del myDB[("table-" + str(i)).encode('ascii')]

            #   delete in other tablename-referencedby
            referenced_bys = dbget(table + "-referencedby")
            if referenced_bys == None :
                continue
            referenced_by_list = referenced_bys.split('-')
            referenced_by_list = [ref for ref in referenced_by_list if ref != table_name]
            if len(referenced_by_list) == 0:
                del myDB[(table + "-referencedby").encode('ascii')]
            else :
                dbput(table + "-referencedby", '-'.join(referenced_by_list))

        #   decrease tablesnum
        tables_num = int(dbget("tablesnum"))
        dbput("tablesnum", tables_num - 1)

        printError(f"DropSuccess:{table_name}")

        

    def explain_query(self, items):

        #
        #   Requirement : table_name
        #
        explainDescribe(items)
        
    def describe_query(self, items):

        #
        #   Requirement : table_name
        #
        explainDescribe(items)
        
    def desc_query(self, items):

        #
        #   Requirement : table_name
        #
        explainDescribe(items)
        


    def show_query(self, items):
        
        #
        #   Requirement : None
        #
        print("--------------------------------------------------------------------------------")

        tables_max_num = int(dbget("tables"))
        for i in range(0, tables_max_num) :
            if dbget("table-" + str(i)) == None :
                continue
            print(dbget("table-" + str(i)))

        print("--------------------------------------------------------------------------------")



    def delete_query(self, items):
        
        #
        #   Requirement : table_name, [where_clause]
        #
        table_name = items[2].children[0].lower()

        
        #   check errors
        if dbget(table_name) == None :
            printError("NoSuchTable")
            return

        #   run where clause
        where_clause = items[3]
        processed_table = getTable(table_name)
        if where_clause != None :
            processed_table = where_process(processed_table, where_clause)

        #   check errors of where clause
        if check_error(processed_table) :
            printError(processed_table.split(':')[1])
            return

        # delete from db
        data_num = int(dbget(table_name + "-datanum"))
        deleted = 0

        for i in range(0,len(processed_table[2])) :
            table_name = processed_table[0][0]
            columns = processed_table[1]
            data = processed_table[2][i]
            TF = processed_table[4][i]

            if TF == "True" :
                deleted = deleted + 1
                for column_name in columns :
                    if column_name == "0,index" :
                        continue
                    del myDB[(table_name + "-" + column_name + "-" + str(data[0])).encode('ascii')]

        # number of data (not max)
        dbput(table_name + "-datanum", data_num - deleted)

        printError(f"DeleteResult:{deleted}")





    def update_query(self, items):
        printRequest("UPDATE")
    def exit_program(self, items):
        myDB.close()
        exit() # sys.exit(). exit the program

# running the program until exit
while(True):

    # initialize querys and print prompt
    querys = "" 
    printPrompt()
    query_list = []

    # receive querys until ';' comes in
    while(len(query_list)==0 or not query_list[-1].isspace()):
        query_input = input()
        querys = querys + query_input + " "
        query_list = querys.split(";")
    
    # last item is space
    for idx in range(0, len(query_list)-1):

        # reattach ';' after split
        query = query_list[idx] + ";"

        # parse and check Systax error
        try:
            output = sql_parser.parse(query)
            #print(output.pretty())
        except:
            printError("SyntaxError")
            break

        # to not catch exit() in try ~ except, syntax error doesn't do anything
        MyTransformer().transform(output)