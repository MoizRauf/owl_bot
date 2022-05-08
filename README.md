# Owl - the Axxessio Demo Bot

Welcome to owl-bot built with open source Rasa framework. This virtual assistant is able to provide you information on various aspects pertaining to Axxessio. The current implementation of Owl comes with a web client. Owl is designed to understand and answer in German language. It supports the following user goals:

1. Provides information regarding different **clients** Axxessio has worked with.
2. Getting the **address** details.
3. Answering the **size** of the company.
4. Listing the **prizes** awarded to Axxessio.
5. Information regarding **Managing team** of the company
	- search based on Names
	- Department
	- Position 	
6. **Ethos** of Axxessio
7. Any new **Job vacancies** in the company
	- Search based on Title
	- karrier level
	- department 

## To Run Owl
 1. Before running Owl you would need to train the a model. Inorder to accomplish this task use `rasa train`.
 2. Afterwards, you would need to run the rasa model and the action server using following commands.
 	```bash
		rasa run --enable-api --cors "*"
		rasa run actions
	```
3. Load the [index.html](front_end/chatroom/index.html) to talk to the bot.

## Data
Data for answering all inquiries answered by Owl are sourced from [Axxessio](https://www.axxessio.com/de). To extract the data we employ a custom python based web scrapper `scripts\scrapper.py` built using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). To generate training examples we utilize a basic template based example generator `scripts\generate_training_examples.py`. Finally, basic seed set of intents (greet,bye, help etc) are adopted from [rasa german demo](https://github.com/gras64/rasa-german-demo) repository.

### Rasa Custom Actions
- Owl implements a rudemantry search based approach to answer various questions for topics such as (job listings, employee information, clients etc) on the above-collected data. 
- To mitigate risk of unaswered queries, Owl utilizes [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to provide most similar answer in case of wrong employee name, job criteria provided. Note, that this approach also leads to partial incorrect answers.

## Future Direction
- **Dynamic Intent Generation**:
	+ generating intent through templates or using synonyms etc to generate more examples
	+ Text generation using LM
	+ Knowledge managment repository for identifying intents and generating responses
- **Intelligent Entity identification**:
	+ A system to identify different entities which can also form questions 
		* e.g In welcher Abteilung arbeitet Andreas Bartsch? 
		* Entities: Abteilung (subject), Andreas Bartsch (person)
- **Reducing Corner case handling**:
	+ Building Rasa with [Haystack](https://github.com/deepset-ai/rasa-haystack) or pretrained QA model for mitigating story overhead and generating more semantically similar reponses
- **Data generation**:
	+ Model to identify story patterns
	


## Requirements

```bash
Rasa Version      :         3.1.0
Rasa SDK Version  :         3.1.0
Rasa X Version    :         None
Python Version    :         3.8.13
Operating System  :         Linux
Python Path       :         /bin/python3
textdistance      :         4.2.2
BeautifulSoup	  :         4.6.0
```

