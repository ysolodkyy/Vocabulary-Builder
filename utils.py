''' 
open and save cvs files at the beginning and end of every session
'''
import pandas

file_read = False

def save_list(len, words_list, weights):

    global file_read

    if file_read == False: # if the list is empty
        print("file_read == False: save nothing...")
        pass
    
    else:
        print("file_read == True: saving file...")
        df = pandas.DataFrame(words_list)
        if words_list: # if list not empty add weights. 
            df['weight'] = weights
            
        df.to_csv(f"./data/weighted_vocab/ESL_vocabulary_{len}_in_progress.csv", index=False)
        file_read = False


def open_newlist(len):

    global file_read
    try: 
        df = pandas.read_csv(f"./data/weighted_vocab/ESL_vocabulary_{len}_in_progress.csv")
    
    except FileNotFoundError as error_message: # if the file's not found 
        print(f"Exception Caught: {error_message}. opening ESL_vocabulary_{len}.csv instead")
        df = pandas.read_csv(f"./data/weighted_vocab/ESL_vocabulary_{len}.csv")
    
    except pandas.errors.EmptyDataError as error_message:
        print(f"Exception Caught: {error_message} ESL_vocabulary_{len}_in_progress.csv is empty! Opening ESL_vocabulary_{len}.csv")
        df = pandas.read_csv(f"./data/weighted_vocab/ESL_vocabulary_{len}.csv")

    words_list = df[['word', 'definition']].to_dict(orient="records")
    weights = df['weight'].tolist()
    file_read = True

    return words_list, weights

