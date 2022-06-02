### Aktualni chyby
- Při spuštění run.bat --> chyba v dockeru import module 'couchdb', ale při spuštění lokálně vše all right. (asi nejak spatne nainstalovane requirments ?)
- VYŘEŠENO: 2 knihovny v requirements nespolupracovali -> odstraněna CouchBase a ponechána couchdb
<br/>

- GQL chyba načtení schémat ---> udělat znovu schémata, modely, queries a resolvery !!!
- Částečně vyřešeno -> dodělat zbylé CRUD operace :)
- Vyřešeno, dodělat zbylé ralitionships (Role, RoleType etc...) -> Group and User are DONE
<br/>

- Dodělat UpdateUser chybovou hlasku - při nenalezeni bud vytvorit prvek se vsema potrebnema informacemi nebo napsat chybovou hlasku, ze update nejde udelat protoze prvek neexistuje !

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
- [x] tvorba programu ()
    - [x] Nainstalovani + konfigurace databaze couchDB v dockeru
    - [x] Propojeni s databazi + manipulace s ni
    - [x] Vytvoření čistého GQL pomocí FastAPI nebo jiného rozhraní
    - [x] Vytvoření schémat, modelů, queries, mutations do GQL aplikace (zatím hotovo: 2 queries, 1 mutation)
    - [x] Vytcoření relací (Group-User✔️, Role,RoleType, GroupType, ...) 
    - [x] Vytvořit zbylé CRUD operace (queries, mutace) podle možného používání
    - [x] Vytvořit Modely a Schémata pro reálnou DBS (Users✔️, Groups✔️, GroupType, ... podle předchozího projektu)
- [x] testování programu (docker databaze✔️, propojeni s databazi✔️, GQL docker✔️, query First_by_ID✔️, query allDocsFromDBS✔️, mutation createDocInDBS✔️, relations between Group/User all CRUDs✔️, debugGQLError ve funkcích✔️, mutace AddUserToGroup✔️, default Group pro users ✔️, ....)
- [x] projektový den (7.4.2022) - Konzultace, ujasnění, instalace, zavedení do dockeru, odstranění docker-requirements chyby
- [x] projektový den alfa verze (5.5.2022) - propojeni + docker, funkce na práci s dbs, kostra GQL
- [ ] projektový den beta verze (8.6.2022)
- [ ] uzavření projektu (23.6.2022)

