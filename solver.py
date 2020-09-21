import logging
import configparser

#TODO work out useful info logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

#################
# read Soduku to solve #
#################
logging.info("Open Sudoku")
config_loc='./input_puzzle.properties'
config = configparser.RawConfigParser()
config.read(config_loc)

sudoku=[]
for (key,value) in config.items("Input"):
    r = value.replace(" ","").split(",")
    logging.info("{},  {}".format(key, r))
    # ri= [int(i) for i in r] # TODDO it errors on the dots...
    sudoku.append(r)

def print_sudoku(sudoku):
    print("-------------------------")
    i=0
    for r in sudoku:
        print("| {} {} {} | {} {} {} | {} {} {} | ".format(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
        i+=1
        if i % 3==0:
            print("-------------------------")
    print("\n")
    

def print_square(sq):
    for r in sq:
        print("{} {} {}".format(r[0],r[1],r[2]))

def check_row(row,search):
    logging.debug("looking for {} in {}".format(search,sudoku[row]))
    for item in sudoku[row]:
        if (item==search):
            return True
    return False

def check_col(col,search):
    logging.debug("looking for {} in {}".format(search,col))
    for row in sudoku:
        if row[col] == search:
            return True
    
    return False

def get_col(c):
    column=[]
    for row in sudoku:
        column.append(row[c])
    return column

def get_square(r,c):
    if r < 3:
        return get_sq_rows(sudoku[0:3],c)
    if r < 6:
        return get_sq_rows(sudoku[3:6],c)
    else:
        return get_sq_rows(sudoku[6:9],c)

def get_sq_rows(rows,c):
    if c < 3:
        return get_sq_cols(rows,range(0,3))
    if c < 6:
        return get_sq_cols(rows,range(3,6))
    else:
        return get_sq_cols(rows,range(6,9))

def get_sq_cols(rows,cols):
    square = []
    for r in rows:
        row = []
        for c in cols:
            row.append(r[c])
        square.append(row)
    return square

def check_square(r,c,search):
    for row in get_square(r,c):
        if search in row:
            return True
    return False

print_sudoku(sudoku)

logging.debug("Column 2: {}".format(get_col(1)))
logging.debug("Column 8: {}".format(get_col(7)))

#print_square(get_square(1,2))
#print_square(get_square(3,5))
#print_square(get_square(5,4))
#print_square(get_square(7,8))


logging.debug("Row 0 contains 8 (T) = {}".format(check_row(0,"8")))
logging.debug("Row 1 contains 4 (F) = {}".format(check_row(1,"4")))

logging.debug("Col 2 contains 9 (T) = {}".format(check_col(2,"9")))
logging.debug("Col 6 contains 5 (F) = {}".format(check_col(6,"5")))



def solve():
    allowed_sudoku = []

    unsolved = True
    change_made = True

    # Simple solve - check cols, rows, squares
    while (unsolved & change_made):
        unsolved = False
        change_made = False
        
        for r in range(0,9):
            row = sudoku[r]
            allowed_row = []
            for c in range(0,9):
                item = row[c]
                allowed_items =[]
                if item == ".":
                    for nn in range(1,10):
                        n = str(nn)
                        if ((n in row) | (n in get_col(c)) | (check_square(r,c,n))):
                            continue
                        else:
                            allowed_items.append(n)
                    logging.debug("Allowed Items: {}".format(allowed_items))

                if len(allowed_items)==1:
                    sudoku[r][c]=allowed_items[0]
                    change_made = True
                
                if len(allowed_items)>1:
                    unsolved = True

                allowed_row.append(allowed_items)
            allowed_sudoku.append(allowed_row)
        
        print_sudoku(sudoku)

    # Check rows for only 1 instance of digit in allowed values
    # Check cols for only 1 instance of digit in allowed values
    # Check squares for only 1 instance of digit in allowed values
    
#    while unsolved:
#        for r in range(0,9):
#            row = allowed_sudoku[r]
#            vals = []
#            for av in row:
#                for item in av:
#                    vals


    if unsolved:
        logging.info("I Failed you :(")
    else:
        logging.info("Victory!")    


solve()