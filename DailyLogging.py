from Database import insertToDb



if __name__ == "__main__": 
    try: 
        insertToDb()
    except Exception as e: 
        print(e)
        print("Error while inserting to DB")
        exit(5)