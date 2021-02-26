import pandas as pd
import sqlite3   
conn = sqlite3.connect("mydatabase.db")# if it is first time it creates DB
df=pd.DataFrame()
df["name"]=["orhan"]
df["age"]=[10]
df["surname"]=["NURKAN"]
df.to_sql(name='students', con=conn,if_exists='replace', index=False)
null=0
true=True
req={"lang":"fr","title":"","superTheme":"","theme":"","textSearchTerms":"",
"signatureDate":{"start":"2018-01-01T00:00:00.000Z", "end":"2021-12-31T00:00:00.000Z1",
"depositNumber":{"start":49933,"end":null},"noticeDeposaMBDate":{"start":null,"end":null},
"enforced":"", "royalDecreeDate":{"star":null,"end":null},
"publicationRoyalDecreeDate":{"start":null,"end":null},"recordDate":{"start":null,"end":null}, 
"correctedDate":{"start":null,"end":null},"depositDate":{"start":null,"end":null},"advancedSearch":true}}

res1={'jcId': 3290200, 
'jcFr': 'SOUS-COMMISSION PARITAIRE POUR LE SECTEUR SOCIO-CULTUREL DE LA COMMUNAUTE FRANCAISE ET GERMANOPHONE ET DE LA REGION WALLONNE', 
'jcNl': 'PARITAIR SUBCOMITE VOOR DE SOCIO-CULTURELE SECTOR VAN DE FRANSTALIGE EN DUITSTALIGE GEMEENSCHAP EN HET WAALSE GEWEST', 
'titleFr': 'Prime dÂ\x92encouragement', 
'titleNl': 'Aanmoedigingspremie', 
'themesFr': None, 
'themesNl': None, 
'signatureDate': '2021-01-18T11:00:00.000+0000', 
'validityDate': '2021-03-31T10:00:00.000+0000', 
'depositDate': '2021-01-28T11:00:00.000+0000', 
'recordDate': '2021-02-23T11:00:00.000+0000', 
'depositRegistrationDate': '2021-02-23T11:00:00.000+0000', 
'depositNumber': 163428, 
'enforced': True, 
'royalDecreeDate': None, 
'noticeDepositMBDate': None, 
'publicationRoyalDecreeDate': None, 
'correctedDate': None, 
'documentLink': '32902/32902-2021-000649.pdf', 
'documentSize': '388 Kb', 
'scopeFr': ["Employeurs tels que dÃ©finis et agrÃ©Ã©s par la COCOF via le dÃ©cret du 27/04/1995 relatif Ã\xa0 l'agrÃ©ment de certains organismes d'insertion sociopro. et au subventionnement de leurs activitÃ©s de formation pro. en vue d'accroÃ®tre les chances de demandeurs d'emploi inoccupÃ©s et peu qualifiÃ©s de trouver ou de retrouver du travail dans le cadre de dispositifs coordonnÃ©s d'insertion sociopro. et ...", 
    "... ayant une convention de partenariat avec Actiris telle que prÃ©vue par les arrÃªtÃ©s de l'ExÃ©cutif de la RÃ©gion de Bruxelles-Capitale du 27/06/1991 autorisant Actiris Ã\xa0 conclure des conventions de partenariat en vue d'accroÃ®tre les chances de certains demandeurs d'emploi de trouver ou de retrouver du travail dans le cadre de dispositifs coordonnÃ©s d'insertion socioprofessionnelle.", 
    "Personnel occupÃ© au sens de la Loi sur les contrats de travail du 3/07/1978 affectÃ©s Ã\xa0 des projets d'insertion socioprofessionnelle tels que dÃ©finis par le DÃ©cret de la COCOF du 27/04/1995.", 
    'Dans les Missions locales, outre le personnel Ã©noncÃ© ci-dessus : les travailleurs affectÃ©s aux missions de l\'ordonnance du 27/11/2008 relative au soutien des missions locales pour l\'emploi et des "lokale werkwinkels", les encadrants des programmes de transition professionnelle, le personnel des ateliers de recherche active d\'emploi.'], 
'scopeNl': ['Werkgevers zoals bepaald en erkend door de COCOF door het Decreet van 27/04/1995 betreffende de erkenning van organismen voor socio-pro. inschakeling en de subsidiering van hun beroepsopleidingsactiviteiten voor werklozen en laag geschoolde werkzoekenden gericht op het vergroten van hun kans op het vinden of terugvinden van werk in het raam van gecoÃ¶rdineerde voorzieningen voor socio-pro. inschakeling en...', 
    '...die een partnerschapsovereenkomst hebben met Actiris zoals bepaald door de Besluiten van de Brusselse Hoofdstedelijke Executieve van 27/06/1991 houdende machtiging voor Actiris tot het sluiten van partnerschapsovereenkomsten ter vergroting van de kansen van bepaalde werkzoekenden om werk te vinden of terug te vinden in het raam van gecoÃ¶rdineerde voorzieningen voor socioprofessionele inschakeling.', 
    'Personeel tewerkgesteld in de zin van de wet op de arbeidsovereenkomsten van 3/07/1978, aangesteld voor projecten voor socio-professionele inschakeling zoals bepaald door het Decreet van de COCOF van 27/04/1995.', 'Bij de "Missions locales", bovenop het personeel dat hierboven is vermeld: de werknemers aangesteld voor de opdrachten van de ordonnantie van 27/11/2008 betreffende de ondersteuning van de "missions locales pour l\'emploi" en van de "lokale werkwinkels", de begeleiders van de doorstromingsprogramma\'s, het personeel van de ateliers dat actief zoekt naar werk.'], 
'noScopeFr': ["Travailleurs affectÃ©s Ã\xa0 des missions relevant d'un autre agrÃ©ment et bÃ©nÃ©ficiant des avantages relevant d'un accord non-marchand d'une autre entitÃ© fÃ©dÃ©rÃ©e.", "Les travailleurs affectÃ©s Ã\xa0 des missions d'Ã©conomie sociale d'insertion auprÃ¨s d'employeurs agrÃ©Ã©s en vertu de l'ordonnance du 18/03/2004 relative Ã\xa0 l'agrÃ©ment et au financement des initiatives locales de dÃ©veloppement de l'emploi et des entreprises d'insertion ou de l'ordonnance du 23/07/2018 relative Ã\xa0 l'agrÃ©ment et au soutien des entreprises sociales."], 
'noScopeNl': ['Werknemers aangesteld voor opdrachten die vallen onder een andere erkenning en die voordelen genieten die vallen onder een non-profitakkoord van een andere gefedereerde entiteit.', 'Werknemers aangesteld voor opdrachten inzake sociale inschakelingseconomie bij werkgevers erkend krachtens de ordonnantie van 18/03/2004 betreffende de erkenning en de financiering van de plaatselijke initiatieven voor de ontwikkeling van de werkgelegenheid en de inschakelingsondernemingen of de ordonnantie van 23/07/2018 met betrekking tot de erkenning en de ondersteuning van de sociale ondernemingen.']}
res2 = {'jcId': 3310000, 
'jcFr': "COMMISSION PARITAIRE POUR LE SECTEUR FLAMAND DE L'AIDE SOCIALE ET DES SOINS DE SANTE", 
'jcNl': 'PARITAIR COMITE VOOR DE VLAAMSE WELZIJNS- EN GEZONDHEIDSSECTOR', 
'titleFr': 'ChÃ¨ques consommation',
'titleNl': 'Consumptiecheques', 
'themesFr': None, 
'themesNl': None, 
'signatureDate': '2021-01-20T11:00:00.000+0000', 
'validityDate': '2021-12-31T11:00:00.000+0000', 
'depositDate': '2021-02-02T11:00:00.000+0000', 
'recordDate': '2021-02-23T11:00:00.000+0000', 
'depositRegistrationDate': '2021-02-23T11:00:00.000+0000', 
'depositNumber': 163431, 
'enforced': True, 
'royalDecreeDate': None, 
'noticeDepositMBDate': None, 
'publicationRoyalDecreeDate': None, 
'correctedDate': None, 
'documentLink': '331/331-2021-000975.pdf', 
'documentSize': '277 Kb', 
'scopeFr': None, 
'scopeNl': None, 
'noScopeFr': None, 
'noScopeNl': None}
