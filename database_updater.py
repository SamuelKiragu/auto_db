def main():
    import argparse
    import csv

    from sqlalchemy import create_engine,text

    # Constants
    ERROR_TEXT = "PROGRAM ERROR:"
    SUCCESS_TEXT = "SUCCESS:"


    # creating the parser
    parser = argparse.ArgumentParser(description='Read the database variables')


    # path of the config file
    parser.add_argument('--config', help="specify the configuration file")

    args = parser.parse_args()


    if not(args.config == None):

    # reading the configuration file
        with open(args.config, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=">",quotechar='|')
            for row in file:
                if row[0] == "database_url":
                    # connecting to the database
                    try:
                        # create database engine
                        db =  create_engine(row[1])
                    except:
                        print(ERROR_TEXT + "DATABASE DOES NOT EXIST")
                elif row[0] == "columns":
                    # splitting the colums passed via the command line
                    colArr = row[1].split(',')
                elif row[0] == "table":
                    table_name = row[1]
                elif row[0] == "csv":
                    csv_path = row[1]

        try:
            # read the csv file
            with open(csv_path, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:

                    queryCol = col(colArr, False)
                    queryVal = col(row, True)

                    query = f"""
                    INSERT INTO {table_name}({queryCol})
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
