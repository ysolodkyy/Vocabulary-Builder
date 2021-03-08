# Vocabulary_Builder
Python vocabulary builder app using web scraped Newbury House Dictionary

This is a basic vocabulary builder app that uses Newbury House Dictionary vocabulary that I scraped as part of an exercise. http://nhd.heinle.com/home.aspx

DISCLAIMER: 
I DO NOT own the vocabulary, and it is copyrighted exclusively to Heinle Cengage Learning. Heinle enjoys an exclusive license with respect to the copyright and all the exclusive rights comprised in the copyright in the work and all revisions thereof.

The app grew out of my personal experience having to learn English vocabulary as a teen. In retrospect I thought an effective way of subdividing the vocabulary into digestible pieces would be based on word lengths. The user selects the length of words for the session and an appropriate vocabulary list is retrieved. 

Each word entry is a dictionary with keys "word", "definition", and "weight". 

The application does weighted random selection of words. Each time the user states they know the word, the weight of the word is reduced and it becomes less likely to be recommended in subsequent sessions. The learning sessions are saved as "in progress" lists so that the original vocabulary lists aren't changed and can be reused in the future. If the weight of the word drops down to 0, the word is removed from the list. Once all words are dropped from an " in progress" session list and the list becomes empty, the subsequent session will use the original vocabulary list to create a new "in progress" list. 

The app utilized macOS speech functionality so every word can be pronounced for the user. 

Future TODOs:

1. Since the data was scraped from an HTML webpage, there are pronunciation aides demarcated with forward slashes "/" that no longer serve their purpose and need to be removed. 
2. Need to improve the alignment of words in the text box. 
3. Explore adding a quiz functionality that will allow the user to practice the words they've learned. 
