def main():
    import argparse
    import csv

    from sqlalchemy import create_engine,text

    # Constants
    ERROR_TEXT = "PROGRAM ERROR:"
    SUCCESS_TEXT = "SUCCESS:"


    # creating the parser
    parser = argparse.ArgumentParser(description='Read the database variables')

    # path of the csvfile
    parser.add_argument('--dfile', help="path of the flat file")

    # location of the database
    parser.add_argument('--db_loc', help="database location")

    # table name
    parser.add_argument('--tbl_name', help="table name")

    # columns
    parser.add_argument('--cols', help="columns")


    args = parser.parse_args()


    if not(args.dfile == None) and not(args.db_loc == None) and not(args.tbl_name == None) and not(args.cols == None):


        # splitting the colums passed via the command line
        colArr = args.cols.split(',')

        # connecting to the database
        try:
            # create database engine
            db =  create_engine(args.db_loc)
        except:
            print(ERROR_TEXT + "DATABASE DOES NOT EXIST")


        try:
            # read the csv file
            with open(args.dfile, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:

                    queryCol = col(colArr, False)
                    queryVal = col(row, True)

                    query = f"""
                    INSERT INTO {args.tbl_name}({queryCol})
                    VALUES({queryVal})
                    """
                    
                    try:
                        db.execute(text(query))
                        print(SUCCESS_TEXT + "Inserted row")
                    except:
                        print(ERROR_TEXT + "INVALID DATA")

        except:
            print(ERROR_TEXT + "INVALID CSV FILE")
    else:
        print(ERROR_TEXT + "One of the required arguments is not valid")





# function declaration
def col(colArr,data):
    text = ""

    for i in range(len(colArr)):
        if(data):
            if i == (len(colArr) - 1):
                text = text + f"\'{colArr[i]}\'"
            else :
                text = text + f"\'{colArr[i]}\'" + ','
        else:
            if i == (len(colArr) - 1):
                text = text + colArr[i]
            else :
                text = text + colArr[i] + ','
    return text


if __name__ == "__main__":
    main()
