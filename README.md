# owl_bot
Welcome to owl-bot pwoered by Rasa. I am able to provide you information regarding Axxessio.

Here is the list of topics I can answer about
- Clients
- Location
- Size of the company
- Prizes awarded to Axxessio
- Managing team of the company
- Ethos of Axxessio
- Any new job opennings in the company
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
	+ Building rasa with haystack or pretrained QA model for mitigating story overhead and generating more semantically similar reponses
- **Data generation**:
	+ Model to identify story patterns
## Requirements
- rasa opensource verison 3.1
- Beautiful soup
- textdistance

