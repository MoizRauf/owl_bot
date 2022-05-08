def gen_data_for_position():
    titles = ["Computerlinguisten","App Developer","Geschäftsführung","Java Developer",
    "Design","Python Developer","Testautomatisierer","Frontend Entwickler","Web Developer","mobile Entwickler","Human Resource"]
    for title in titles:
        print(f"    - Gibt es eine Stelle für einen [{title}](job_title)")
        print(f"    - Gibt es eine öffnung für einen [{title}](job_title)")
        print(f"    - alle Jobs auflisten für [{title}](job_title)")
        print(f"    - Ich möchte die Jobs für [{title}](job_title) kennen")
        print(f"    - Machst du irgendwelche Jobs für [{title}](job_title)")
        if "developer" in title.lower():
            name = title.split(" ")[0]
            print(f"    - Gibt es eine Stelle für einen [{name} Entwickler](job_title)")
            print(f"    - Gibt es eine öffnung für einen [{name} Entwickler](job_title)")
            print(f"    - alle Jobs auflisten für [{name}  Entwickler](job_title)")
            print(f"    - Ich möchte die Jobs für [{name}  Entwickler](job_title) kennen")
            print(f"    - Machst du irgendwelche Jobs für [{name}  Entwickler](job_title)")

        if "entwickler" in title.lower():
            name = title.split(" ")[0]
            print(f"    - Gibt es eine Stelle für einen [{name} developer](job_title)")
            print(f"    - Gibt es eine öffnung für einen [{name} developer](job_title)")
            print(f"    - alle Jobs auflisten für [{name} developer](job_title)")
            print(f"    - Ich möchte die Jobs für [{name} developer](job_title) kennen")
            print(f"    - Machst du irgendwelche Jobs für [{name} developer](job_title)")

def gen_data_for_category():
    titles = ["Software Development","Central Functions","Software Testing","Business Consulting",
    "IT-Architecture"]
    for title in titles:
        print(f"    - Gibt es eine Stelle für Kategorie [{title}](job_dep)")
        print(f"    - Gibt es eine öffnung für Kategorie [{title}](job_dep)")
        print(f"    - Gibt es eine Stelle in Kategorie [{title}](job_dep)")
        print(f"    - Gibt es eine öffnung in Kategorie [{title}](job_dep)")
        print(f"    - Ich möchte die Jobs für [{title}](job_dep) kennen")
        print(f"    - Machst du irgendwelche Jobs für [{title} Entwickler](job_dep)")
        if "developer" in title.lower():
            name = title.split(" ")[0]
            print(f"    - Gibt es eine Stelle für Kategorie [{name} Entwickler](job_dep)")
            print(f"    - Gibt es eine öffnung für Kategorie [{name} Entwickler](job_dep)")
            print(f"    - Gibt es eine Stelle in Kategorie [{name} Entwickler](job_dep)")
            print(f"    - Gibt es eine öffnung in Kategorie [{name} Entwickler](job_dep)")
            print(f"    - Ich möchte die Jobs für [{name} Entwickler](job_dep) kennen")
            print(f"    - Machst du irgendwelche Jobs für [{name} Entwickler](job_dep)")

        if "entwickler" in title.lower():
            name = title.split(" ")[0]
            print(f"    - Gibt es eine Stelle für Kategorie [{name} developer](job_dep)")
            print(f"    - Gibt es eine öffnung für Kategorie [{name} developer](job_dep)")
            print(f"    - Gibt es eine Stelle in Kategorie [{name} developer](job_dep)")
            print(f"    - Gibt es eine öffnung in Kategorie [{name} developer](job_dep)")
            print(f"    - Ich möchte die Jobs für [{name} developer](job_dep) kennen")
            print(f"    - Machst du irgendwelche Jobs für [{name} developer](job_dep)")

def gen_data_for_level():
    titles = ["Professional","Young Professional","Freelancer","Werkstudent",
    "Praktikant"]
    for title in titles:
        print(f"    - Gibt es eine Stelle für Karrierlevel [{title}](job_level)")
        print(f"    - Gibt es eine öffnung für Karrierlevel [{title}](job_level)")
        print(f"    - Ich möchte die Jobs für Karrierlevel [{title}](job_level) kennen")
        print(f"    - Machst du irgendwelche Jobs für Karrierlevel [{title}](job_level)")

def gen_data_for_person_rank():
    titles = ["CEO","ProkuristHead","Senior Manager","Executive Software-Architect","Manager","Senior IT-Manager"
    ,"Senior Test Manager","Principal Software Developer","Lead Software Developer","Team Lead"]
    for title in titles:
        print(f"    - Wer ist der [{title}](person_rank) von axxessio?")
        print(f"    - Nennen Sie alle [{title}](person_rank)")
        print(f"    - Wer sind die [{title}](person_rank) im axxessio")
        print(f"    - Wer sind die [{title}](person_rank) im Firma")
        print(f"    - geben Sie die Namen an [{title}](person_rank)")

def gen_data_for_dep():
    titles = ["Human Resources and Finances","Business Consulting and Digital Management","Software Engineering","Executive Software-Architect",
    "Business and Technology Innovation ",  "Digital Consulting and Innovation","Test Automation","New Technologies","Test Management"
    ,"Software Development"]
    for title in titles:
        print(f"    - Wer ist der Team Lead von [{title}](job_dep) in axxessio?")
        print(f"    - Nennen Sie alle Leiter [{title}](job_dep)")
        print(f"    - wer ist der gruppenleiter [{title}](job_dep)")
        print(f"    - wer leitet die [{title}](job_dep)")
      
if __name__ == '__main__':
    gen_data_for_person_rank()
    gen_data_for_dep()
    #gen_data_for_position()
    #gen_data_for_category()
    #gen_data_for_level()
    quit()


       