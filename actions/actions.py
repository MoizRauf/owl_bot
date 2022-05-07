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
		location_list = ["darmstadt","bonn","haupsitz","niederlassung"]
		location = tracker.get_slot("location_category")
		if not location or location.lower() not in location_list:
			dispatcher.utter_message(template="utter_incorrect_location")
		else:
			if location.lower() == location_list[1] or location.lower() == location_list[2]:
				dispatcher.utter_message(text= f"Die Addresse für Haupsitz ist: Kurfürstenallee 5 • 53177 Bonn")
			else:
				dispatcher.utter_message(text= f"Die Addresse für Niederlassung ist:Hilpertstraße 20 • 64295 Darmstadt")
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
		cat_list = self.get_data_list()
		stmt = "Axxessio hat Kunden in Kategorien: "+ ",".join(cat_list)
		dispatcher.utter_message(text= stmt)

		return []

class ActionShowEmployee(Action):
	"""Takes the employee"""

	def name(self) -> Text:
		return "action_show_employee"

	def get_data_map(self) -> set:
		employee_map= {}
		with open('/home/moiz/rasa/owl_bot/actions/action_data/employee.csv', newline='') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				name =  row[0].strip().lower()
				rank = row[1].strip().lower()
				position = row[2].strip().lower()
				department = row[3].strip().lower()
				if name not in employee_map:
					employee_map[name] = {}

				employee_map[name]["rank"] =  rank
				employee_map[name]["position"] =  position
				employee_map[name]["department"] =  department
		return employee_map

	def run(
	self,
	dispatcher: CollectingDispatcher,
	tracker: Tracker,
	domain: Dict[Text, Any],
	) -> List[EventType]:
		levenshtein = textdistance.Levenshtein(external=False)
		employee_map = self.get_data_map()
		person = tracker.get_slot("person_name")
		if person == None and not person:
			dispatcher.utter_message(template="utter_provide_correct_name")
		else:
			# get most similar name as to the provided one
			sim_map = {}
			for name in employee_map:
				sim_map[name] = levenshtein.normalized_similarity(name, person)

			max_key = max(sim_map, key=sim_map.get)
			rank = employee_map[max_key]["rank"]
			position = employee_map[max_key]["position"]
			department = employee_map[max_key]["department"] 
			if sim_map[max_key]> 0.6:				
				dispatcher.utter_message(text= f"Name: {max_key}\nTitel: {rank}\nPosition: {position}\nAbteilung: {department}")
				
			elif sim_map[max_key]> 0.4 and sim_map[max_key]< 0.6:
				dispatcher.utter_message(text= f"Bereitstellen von Informationen für die ähnlichsten Namen \n Name: {max_key}\nTitel: {rank}\nPosition: {position}\nAbteilung: {department}")
				
			else:
				dispatcher.utter_message(template="utter_provide_correct_name")

		

		return [SlotSet("person_name", "None")]

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
			if val> 0.5:
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
				if _found:
					return[SlotSet("job_title", "None")]

			if not _found and provided_department:
				_found = self.search_criteria(provided_department.lower(),dep_map,levenshtein,dispatcher)
				if _found:
					return[SlotSet("job_department", "None")]

			if not _found and provided_level:
				_found = self.search_criteria(provided_level.lower(),level_map,levenshtein,dispatcher)
				if _found:
					return[SlotSet("job_level", "None")]

			if not _found:
				dispatcher.utter_message(template="utter_no_job_found")

				

				

		return []