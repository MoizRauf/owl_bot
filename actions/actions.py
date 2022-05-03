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
		location_list = ["darmstadt","bonn"]
		location = tracker.get_slot("location_category")
		if not location or location.lower() not in location_list:
			dispatcher.utter_message(text= f"Leider habe ich keine Informationen für {location}")
		else:
			if location.lower() == location_list[1]:
				dispatcher.utter_message(text= f"Die Addresse für Haupsitz ist: Kurfürstenallee 5 • 53177 Bonn")
			else:
				dispatcher.utter_message(text= f"Die Niederlassung für Haupsitz ist:Hilpertstraße 20 • 64295 Darmstadt")
		return []

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

		category = tracker.get_slot("client_category")
		if category == None and not category:
			dispatcher.utter_message(text= f"Leider diese Kategorie ist nicht korrect.")
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
		return []

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
