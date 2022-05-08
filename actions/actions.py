from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text, Optional
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
import csv
import textdistance
from operator import itemgetter

class ActionShowLocation(Action):
	"""Takes a city from the user and provides address"""

	def name(self) -> Text:
		return "action_show_location_address"

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		try:
			location_list = ["darmstadt","bonn","haupsitz","niederlassung"]
			dispatcher.utter_message(text= f"slot: {show_address}")
			if not location or location.lower() not in location_list:
				dispatcher.utter_message(template="utter_incorrect_location")
			else:
				if location.lower() == location_list[1] or location.lower() == location_list[2]:
					dispatcher.utter_message(template= "utter_location_Bonn")
				else:
					dispatcher.utter_message(template= "utter_location_Darmstadt")
		except Exception as e:
			dispatcher.utter_message(template= "utter_problem_answering")
			dispatcher.utter_message(template= "utter_problem_answering")
		return [SlotSet("location_category", "None")]

class ActionShowBothLocation(Action):
	"""Takes a city from the user and provides address"""

	def name(self) -> Text:
		return "action_show_both_address"

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		dispatcher.utter_message(template= "utter_location_Bonn")
		dispatcher.utter_message(template= "utter_location_Darmstadt")
		return [SlotSet("location_category", "None")]

class ActionShowCompany(Action):
	"""Takes the category from user and provides the customers"""

	def name(self) -> Text:
		return "action_show_customer"

	def get_data(self) -> dict:
		company_map = {}
		with open('/home/moiz/rasa/owl_bot/actions/action_data/clients.csv', newline='') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				name =  row[0].strip()
				cat = row[1].strip().lower()
				if cat not in company_map:
					company_map[cat] = set()
				company_map[cat].add(name)
		return company_map

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		try:
			company_map = self.get_data()

			category = tracker.get_slot("client_category").lower()
			if category == None and not category:
				dispatcher.utter_message(template= "utter_incorrect_customer_category")
			elif category == "all":
				dispatcher.utter_message(text= "| Kategorie | Kunden |")
				for key,val in company_map.items():
					companies = ",".join(val)
					stmt = f"| {key} | {companies}|"
					dispatcher.utter_message(text= stmt)
			elif category not in company_map:
				dispatcher.utter_message(text= f"Leider habe ich keine Informationen für Kategorie: {category}")
			else:
				companies = ",".join(company_map[category])
				stmt = f"Axxessio hat {companies}  als Kunden in Kategorie {category}"
				dispatcher.utter_message(text= stmt)
		except Exception as e:
			dispatcher.utter_message(template= "utter_problem_answering")
		return [SlotSet("client_category", "None")]

class ActionShowClientCategory(Action):
	"""Takes the category from user and provides the customers"""

	def name(self) -> Text:
		return "action_show_client_category"

	def get_data_list(self) -> set:
		cat_list= set()
		with open('/home/moiz/rasa/owl_bot/actions/action_data/clients.csv', newline='') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				cat = row[1].strip()
				
				cat_list.add(cat.lower())
		return cat_list

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		try:
			cat_list = self.get_data_list()
			stmt = "Axxessio hat Kunden in Kategorien: \n •"+ "\n•".join(cat_list)
			dispatcher.utter_message(text= stmt)
		except Exception as e:
			dispatcher.utter_message(template= "utter_problem_answering")
		return []

class ActionShowEmployee(Action):
	"""Takes the employee"""

	def name(self) -> Text:
		return "action_show_employee"

	def get_data_map(self) -> set:
		name_map= {}
		rank_map= {}
		position_map = {}
		department_map = {}
		with open('/home/moiz/rasa/owl_bot/actions/action_data/employee.csv', newline='') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				names =  row[0].strip().lower().split()
				rank = row[1].strip()
				position = row[2].strip()
				department = row[3].strip()
				name_key = (names[-2],names[-1])

				obj = { "rank" :  rank, "name" : row[0].strip(),"position" :  position,"department" : department}
				if name_key not in name_map:
					name_map[name_key] = obj					

				if rank:
					key = rank.lower()
					if key not in rank_map:
						rank_map[key] = []
					rank_map[key].append(obj)

				if position:
					key = position.lower()
					if key not in position_map:
						position_map[key] = []
					position_map[key].append(obj)

				if department:
					key = department.lower()
					if key not in department_map:
						department_map[key] = []
					department_map[key].append(obj)

				
				
				
		return name_map,rank_map, position_map, department_map

	def search_by_name(self,provided_info,data_map,levenshtein,dispatcher):
		sim_map = {}
		
		if provided_info in data_map:
			max_key = provided_info
		else:
			for key in data_map:
				vor_name,nach_name =  key
				pnames = provided_info.split()
				if len(pnames) == 1:
					v_scr = levenshtein.normalized_similarity(vor_name, provided_info)
					sim_map[key] = v_scr
					n_scr = levenshtein.normalized_similarity(nach_name, provided_info)
					if v_scr< n_scr:
						sim_map[key] = n_scr
				else:
					v_scr = levenshtein.normalized_similarity(vor_name, pnames[-2])
					sim_map[key] = v_scr
					n_scr = levenshtein.normalized_similarity(nach_name, pnames[-1])
					if v_scr< n_scr:
						sim_map[key] = n_scr
			max_key = max(sim_map, key=sim_map.get)
		#dispatcher.utter_message(text= f"{max_key} \n {sim_map}")
		name = data_map[max_key]["name"]
		rank = data_map[max_key]["rank"]
		position = data_map[max_key]["position"]
		department = data_map[max_key]["department"] 
		_found = False
		if sim_map[max_key]> 0.6:				
			dispatcher.utter_message(text= f"Name: {name}\nTitel: {rank}\nPosition: {position}\nAbteilung: {department}")
			_found = True			
		elif sim_map[max_key]> 0.3 and sim_map[max_key]< 0.6:
			dispatcher.utter_message(text= f"Bereitstellen von Informationen für die ähnlichsten Namen \n Name: {name}\nTitel: {rank}\nPosition: {position}\nAbteilung: {department}")
			_found = True

		return _found

	def search_criteria(self,provided_info,data_map,levenshtein,dispatcher):
		sim_map = {}
		_found = False
		if provided_info in data_map:
			cat_key = provided_info
		else:
			for key in data_map:
				sim_map[key] = levenshtein.normalized_similarity(key, provided_info)
				 
			cat_key = max(sim_map, key=sim_map.get)

		dispatcher.utter_message(text= f"Wir haben {len(data_map[cat_key])} Person(en) für {provided_info} gefunden.")
		for val in data_map[cat_key]:
			name = val["name"]
			rank = val["rank"]
			position = val["position"]
			department = val["department"] 
					
			dispatcher.utter_message(text= f"Name: {name}\nTitel: {rank}\nPosition: {position}\nAbteilung: {department}")
			_found = True			
			
		return _found

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		try:
			levenshtein = textdistance.Levenshtein(external=False)
			name_map,rank_map, position_map, department_map = self.get_data_map()
			person = tracker.get_slot("person_name")
			provided_rank= tracker.get_slot("person_rank")
			provided_department = tracker.get_slot("job_department")
			#dispatcher.utter_message(text= f"{person}")
			if person == None and not person and provided_rank == None and provided_department == None:
				dispatcher.utter_message(template="utter_provide_correct_name")
			else:
				# get most similar name as to the provided one
				#dispatcher.utter_message(text= f"tp: {person}\ntr: {provided_rank}, td: {provided_department}")
				_found = False
				

				if not _found and provided_rank != "None" and provided_rank:
					_found = self.search_criteria(provided_rank.lower(),rank_map,levenshtein,dispatcher)	
				
				if not _found and provided_department != "None" and provided_department:
					_found = self.search_criteria(provided_department.lower(),department_map,levenshtein,dispatcher)

				if not _found and person != "None" and person:
					_found = self.search_by_name(person.lower(),name_map, levenshtein,dispatcher)
				
				
				if not _found:
					dispatcher.utter_message(template="utter_provide_correct_name")
		except Exception as e:
			dispatcher.utter_message(text= f"{e}")
			dispatcher.utter_message(template= "utter_problem_answering")	

		return [SlotSet("person_name", "None"),SlotSet("person_rank", "None"),SlotSet("job_department", "None")]

class ActionShowJobs(Action):
	"""Takes the employee"""

	def name(self) -> Text:
		return "action_show_jobs"

	def get_data_map(self) -> set:
		title_map= {}
		dep_map = {}
		level_map = {}
		with open('/home/moiz/rasa/owl_bot/actions/action_data/jobs.csv', newline='') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				title =  row[0].strip().lower()
				dep = row[1].strip().lower()
				level = row[2].strip().lower()
				obj = {"title": title, "dep": dep, "level": level}
				
				if title not in title_map:
					title_map[title] = []
				if dep not in dep_map:
					dep_map[dep] = []

				if level not in level_map:
					level_map[level] = []

				title_map[title].append(obj)
				dep_map[dep].append(obj)
				level_map[level].append(obj)

				
				
		return title_map,dep_map,level_map

	def search_criteria(self,provided_info,data_map,levenshtein,dispatcher):
		sim_map = {}
		if provided_info in data_map:
			dispatcher.utter_message(text= f"Wir haben  {len(data_map[provided_info])} Stelle(n) für {provided_info} gefunden.")
			for obj in  data_map[provided_info]:
				title =obj["title"]
				dep = obj["dep"]
				level = obj["level"] 
						
				dispatcher.utter_message(text= f"Titel: {title}\nAbteilung: {dep}\nLevel: {level}")
				_found = True
		else:
			for key in data_map:
				scr = levenshtein.normalized_similarity(key, provided_info) 
				#developer entwickler synonym hack		
				if "entwickler" in key:						
					alternative = " ".join(key.split()[:-1])+" developer"
					altscr = levenshtein.normalized_similarity(alternative, provided_info)
					if altscr > scr:
						scr = altscr
				elif "developer" in key:
					alternative = " ".join(key.split()[:-1])+" entwickler"
					altscr = levenshtein.normalized_similarity(alternative, provided_info)
					if altscr > scr:
						scr = altscr
				sim_map[key] = scr
			_found= False
			for key,val in sim_map.items():
				if val> 0.40:
					dispatcher.utter_message(text= f"Wir haben  {len(data_map[key])} Stelle(n) für {provided_info} gefunden.")
					for obj in  data_map[key]:
						title =obj["title"]
						dep = obj["dep"]
						level = obj["level"] 
								
						dispatcher.utter_message(text= f"Titel: {title}\nAbteilung: {dep}\nLevel: {level}")
						_found = True

		
		return _found
	
	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		try:
			levenshtein = textdistance.Levenshtein(external=False)
			title_map,dep_map,level_map = self.get_data_map()

			provided_title = tracker.get_slot("job_title")
			provided_department = tracker.get_slot("job_department")
			provided_level = tracker.get_slot("job_level")
			
			if provided_title == None and provided_department == None and provided_level == None:
				dispatcher.utter_message(template="utter_no_job_found")
			else:
				#dispatcher.utter_message(text= f"pt: {provided_title}\npd: {provided_department}pl: {provided_level}")
				_found = False
				if provided_title:				
					_found = self.search_criteria(provided_title.lower(),title_map,levenshtein,dispatcher)
					
				if not _found and provided_department:
					_found = self.search_criteria(provided_department.lower(),dep_map,levenshtein,dispatcher)
					
				if not _found and provided_level:
					_found = self.search_criteria(provided_level.lower(),level_map,levenshtein,dispatcher)
					
				if not _found:
					dispatcher.utter_message(template="utter_no_job_found")
		except Exception as e:
			dispatcher.utter_message(template= "utter_problem_answering")


		return [SlotSet("job_title", "None"),SlotSet("job_department", "None"),SlotSet("job_level", "None")]