### Aktualni chyby
- Při spuštění run.bat --> chyba v dockeru import module 'couchdb', ale při spuštění lokálně vše all right. (asi nejak spatne nainstalovane requirments ?)
- prozatimní řešení : spouštět FastAPI server lokálně (příkaz do terminálu ve složce:    uvicorn main:app --reload)<br/>
<br/>

- GQL chyba načtení schémat ---> udělat znovu schémata, modely, queries a resolvery !!!

### Úkoly

- časová osa
- Dokončit [konfiguraci databáze v DOCKERU](https://docs.couchdb.org/en/3.2.0/setup/single-node.html)! 
- navrhnutí programu
- tvorba resolverů (root resolver, parent reoslver) (graphql - každá databáze stejné resolvery ale jiné tělo !)
- část potřebná pro GraphQL pojmenovat --*user*GQL--
- udělat databázi CouchDB a k ní přistupovat pomocí GraphQL (tam budou ty resolvery s rozdílnýma tělíčkama by četli naši DB)
- vytvoření mutací do GQL pro vytváření dat do databáze
- primárně operace *Create*, *Read* , *Update* !!
- testování programu
- výsledky testů
- .ipnb příběh (dokumentace)

# GraphQL-w-[CouchDB](https://github.com/apache/couchdb)

####Zadání
>Prostřednictvím GraphQL zpřístupněte CouchDB pro ukládání (CRUD) dat uživatel, skupina, typ skupiny, role uživatele ve skupině, typ role.

###Časová osa

- [x] časová osa (29.03.2022)
- [x] návrh programu ()
- [x] Vytvořeni CouchDB (02.04.2022) (listening on: localhost:31111/_utils)
- [ ] tvorba programu ()
    - [ ] prvni ukol tvorby ()
    - [ ] druhy ukol .... ()
    - [ ] treti ..... ()
- [ ] testování programu ()
- [ ] projektový den (7.4.2022)
- [ ] projektový den alfa verze (5.5.2022)
- [ ] projektový den beta verze (8.6.2022)
- [ ] uzavření projektu (23.6.2022)

