import random
from faker import Faker
from faker.providers import DynamicProvider
from utils import hash_plain_text

organisatie_typen = DynamicProvider(
     provider_name="organisatie_type",
     elements=["Commericeel", "Non-profit"],
)

onderzoek_typen = DynamicProvider(
     provider_name="onderzoek_type",
     elements=["Fysiek", "Online", "Telefonisch"],
)

status_typen_ex_o = DynamicProvider(
     provider_name="status_type_ex_o",
     elements=["Nieuw", "Goedgekeurd", "Afgekeurd"],
)

status_typen_inc_o = DynamicProvider(
     provider_name="status_type_inc_o",
     elements=["Nieuw", "Goedgekeurd", "Afgekeurd", "Gesloten"],
)

beloningen = DynamicProvider(
     provider_name="beloning",
     elements=["Freefiddy", "10 euro", "25 euro", "50 euro", "75 euro"],
)

voorkeuren_benadering = DynamicProvider(
     provider_name="voorkeur_benadering",
     elements=["E-mail", "Telefonisch"],
)

beschikbaarheden = DynamicProvider(
     provider_name="beschikbaarheid",
     elements=["Ochtend", "Middag", "Avond", "Ochtend, Middag", "Ochtend, Avond", "Middag, Avond", "Ochtend, Middag, Avond"],
)

beperkings_categorieën = DynamicProvider(
     provider_name="beperking_categorie",
     elements=["Visuele beperkingen", "Auditieve beperkingen"],
)

tussenvoegsels = DynamicProvider(
     provider_name="tussenvoegsel",
     elements=[None, "de"],
)

geslachten = DynamicProvider(
     provider_name="geslacht",
     elements=["Man", "Vrouw"],
)

hulpmiddelen = DynamicProvider(
     provider_name="hulpmiddel",
     elements=[None, "Gehoorapparaat", "Schermlezer"],
)

fake = Faker("nl_NL")

fake.add_provider(organisatie_typen)
fake.add_provider(onderzoek_typen)
fake.add_provider(status_typen_ex_o)
fake.add_provider(status_typen_inc_o)
fake.add_provider(beloningen)
fake.add_provider(voorkeuren_benadering)
fake.add_provider(beschikbaarheden)
fake.add_provider(beperkings_categorieën)
fake.add_provider(tussenvoegsels)
fake.add_provider(geslachten)
fake.add_provider(hulpmiddelen)

def get_research_titles(amount:int) -> list[str]:
    unique_titles = set()
    while len(unique_titles) < amount:
        disability = random.choice(["visuele beperking", "auditieve beperking"])
        unique_titles.add(f"{fake.word()}-{random.randint(1, 1000)}-{disability}-{random.randint(1, 1000)}")
        
    return list(unique_titles)
    
def get_org_names(amount:int) -> list[str]:
    unique_names = set()
    while len(unique_names) < amount:
        unique_names.add(fake.company())
    
    return list(unique_names)

def get_urls(amount:int) -> list[str]:
    unique_urls = set()
    while len(unique_urls) < amount:
        unique_urls.add(fake.url())
        
    return list(unique_urls)
        
def get_emails(amount:int) -> list[str]:
    unique_emails = set()
    while len(unique_emails) < amount:
        unique_emails.add(fake.email())

    return list(unique_emails)

def get_numbers(amount:int) -> list[str]:
    unique_numbers = set()
    while len(unique_numbers) < amount:
        unique_numbers.add(fake.phone_number())

    return list(unique_numbers)
        
def create_orgs():
    AMOUNT = 4
    organisaties = []
    
    org_names = get_org_names(AMOUNT)
    urls = get_urls(AMOUNT)
    emails = get_emails(AMOUNT)
    numbers = get_numbers(AMOUNT)
    
    demo_organisatie = (
        "Demo Organisatie",
        fake.organisatie_type(),                    
        "https://demo-organisatie-1.nl/",
        fake.paragraph(nb_sentences=3),
        fake.name(),
        "demo@organisatie.nl",
        hash_plain_text("demo123"),
        fake.phone_number(),
        fake.sentence(nb_words=10),
        "Goedgekeurd"
    )
    organisaties.append(demo_organisatie)
    
    for i in range(AMOUNT):
        organisatie = (
            org_names[i],               
            fake.organisatie_type(),                    
            urls[i], 
            fake.paragraph(nb_sentences=3),
            fake.name(),
            emails[i],
            fake.password(length=10),
            numbers[i],
            fake.sentence(nb_words=10),
            "Nieuw"
        )
        organisaties.append(organisatie)
    return organisaties

def create_new_research():
    AMOUNT = 5
    nieuwe_onderzoeken = []
    
    research_titles = get_research_titles(AMOUNT)
    
    for i in range(AMOUNT):
        onderzoek = (
            research_titles[i],               
            "Nieuw",                    
            0, 
            fake.paragraph(nb_sentences=3),
            str(fake.date_between(start_date="+3w", end_date="+6w")),
            str(fake.date_between(start_date="+7w", end_date="+11w")),
            fake.onderzoek_type(),
            fake.province(),
            1,
            fake.beloning(),
            random.randint(18, 30),
            random.randint(67, 80),
            fake.beperking_categorie(),
            1
        )
        nieuwe_onderzoeken.append(onderzoek)
    return nieuwe_onderzoeken
    
def create_approved_research():
    goedgekeurde_onderzoeken = []
    for _ in range(10):
        vb_onderzoek = (
            f"{fake.word()}-{random.randint(1, 1000)}-visuele beperking-{random.randint(1, 1000)}",             
            "Goedgekeurd",                    
            1, 
            fake.paragraph(nb_sentences=3),
            str(fake.date_between(start_date="+2w", end_date="+5w")),
            str(fake.date_between(start_date="+6w", end_date="+10w")),
            fake.onderzoek_type(),
            fake.province(),
            1,
            fake.beloning(),
            random.randint(18, 25),
            random.randint(67, 80),
            "Visuele beperkingen",
            1
        )
        goedgekeurde_onderzoeken.append(vb_onderzoek)
        
    for _ in range(10):
        ab_onderzoek = (
            f"{fake.word()}-{random.randint(1, 1000)}-auditieve beperking-{random.randint(1, 1000)}",              
            "Goedgekeurd",                    
            1, 
            fake.paragraph(nb_sentences=3),
            str(fake.date_between(start_date="+2w", end_date="+5w")),
            str(fake.date_between(start_date="+6w", end_date="+10w")),
            fake.onderzoek_type(),
            fake.province(),
            1,
            fake.beloning(),
            random.randint(18, 30),
            random.randint(67, 80),
            "Auditieve beperkingen",
            1
        )
        goedgekeurde_onderzoeken.append(ab_onderzoek)
    return goedgekeurde_onderzoeken
    
def create_rejected_research():
    AMOUNT = 3
    afgekeurde_onderzoeken = []
    
    research_titles = get_research_titles(AMOUNT)
    
    for i in range(AMOUNT):
        onderzoek = (
            research_titles[i],               
            "Afgekeurd",                    
            0, 
            fake.paragraph(nb_sentences=3),
            str(fake.date_between(start_date="+2w", end_date="+5w")),
            str(fake.date_between(start_date="+6w", end_date="+10w")),
            fake.onderzoek_type(),
            fake.province(),
            1,
            fake.beloning(),
            random.randint(18, 30),
            random.randint(67, 80),
            fake.beperking_categorie(),
            1
        )
        afgekeurde_onderzoeken.append(onderzoek)
    return afgekeurde_onderzoeken
    
def create_closed_research(): 
    AMOUNT = 2
    gesloten_onderzoeken = []
    
    research_titles = get_research_titles(AMOUNT)
    
    for i in range(AMOUNT):
        onderzoek = (
            research_titles[i],               
            "Gesloten",                    
            0, 
            fake.paragraph(nb_sentences=3),
            str(fake.date_between(start_date="-20w", end_date="-16w")),
            str(fake.date_between(start_date="-15w", end_date="-10w")),
            fake.onderzoek_type(),
            fake.province(),
            1,
            fake.beloning(),
            random.randint(18, 30),
            random.randint(67, 80),
            fake.beperking_categorie(),
            1
        )
        gesloten_onderzoeken.append(onderzoek)
    return gesloten_onderzoeken

def create_users():
    AMOUNT = 8
    ervaringsdeskundigen = []
    
    emails = get_emails(AMOUNT)
    numbers = get_numbers(AMOUNT)
        
    demo_beheerder = (
        fake.first_name(),
        fake.tussenvoegsel(),
        fake.last_name(),
        str(fake.date_of_birth(minimum_age=18, maximum_age=30)),
        fake.geslacht(),
        fake.postcode(),
        fake.phone_number(),
        "demo@admin.nl",
        hash_plain_text("demo123"),
        None,
        "E-mail",
        fake.paragraph(nb_sentences=3),
        None,
        None,
        None,
        "Goedgekeurd",
        1,
        1,
        0,
        None,
        None,
        None
    )
    ervaringsdeskundigen.append(demo_beheerder)
    
    demo_ervaringsdeskundige = (
        fake.first_name(),
        fake.tussenvoegsel(),
        fake.last_name(),
        str(fake.date_of_birth(minimum_age=26, maximum_age=32)),
        fake.geslacht(),
        fake.postcode(),
        fake.phone_number(),
        "demo@ervaringsdeskundige.nl",
        hash_plain_text("demo123"),
        fake.hulpmiddel(),
        fake.voorkeur_benadering(),
        fake.paragraph(nb_sentences=3),
        fake.onderzoek_type(),
        None,
        fake.beschikbaarheid(),
        "Goedgekeurd",
        0,
        1,
        0,
        None,
        None,
        None
    )
    ervaringsdeskundigen.append(demo_ervaringsdeskundige)
    
    for i in range(3):
        ervaringsdeskundige = (
            fake.first_name(),
            fake.tussenvoegsel(),
            fake.last_name(),
            str(fake.date_of_birth(minimum_age=18, maximum_age=80)),
            fake.geslacht(),
            fake.postcode(),
            numbers[i],
            emails[i],
            fake.password(length=10),
            fake.hulpmiddel(),
            fake.voorkeur_benadering(),
            fake.paragraph(nb_sentences=3),
            fake.onderzoek_type(),
            None,
            fake.beschikbaarheid(),
            "Goedgekeurd",
            0,
            1,
            0,
            None,
            None,
            None
        )
        ervaringsdeskundigen.append(ervaringsdeskundige)
        
    for i in range(3, AMOUNT):
        ervaringsdeskundige = (
            fake.first_name(),
            fake.tussenvoegsel(),
            fake.last_name(),
            str(fake.date_of_birth(minimum_age=18, maximum_age=80)),
            fake.geslacht(),
            fake.postcode(),
            numbers[i],
            emails[i],
            fake.password(length=10),
            fake.hulpmiddel(),
            fake.voorkeur_benadering(),
            fake.paragraph(nb_sentences=3),
            fake.onderzoek_type(),
            None,
            fake.beschikbaarheid(),
            "Nieuw",
            0,
            1,
            0,
            None,
            None,
            None
        )
        ervaringsdeskundigen.append(ervaringsdeskundige)
    return ervaringsdeskundigen

def create_research_registrations():
    aanmeldingen = []
    onderzoek_ids = random.sample(range(6, 16), 10)
    for onderzoek_id in onderzoek_ids:
        for i in range(3, 6):
            aanmelding = (
                (onderzoek_id, i, fake.status_type_ex_o())
            )
            aanmeldingen.append(aanmelding)
    return aanmeldingen

def create_user_disabilities():
    gebruiker_beperkingen = []
    demo_ervaringsdeskundige_beperking = (
        (2, 4)
    )
    gebruiker_beperkingen.append(demo_ervaringsdeskundige_beperking)
    for i in range(3, 6):
        gebruiker_beperking = (
            (i, 4)
        )
        gebruiker_beperkingen.append(gebruiker_beperking)
    
    for i in range(6, 11):
        gebruiker_beperking = (
            (i, random.choice([1, 4]))
        )
        gebruiker_beperkingen.append(gebruiker_beperking)
    return gebruiker_beperkingen