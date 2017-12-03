# Bevezetés

Mindenképpen webes felületet szerettem volna a programhoz. Először a technológia választás volt a feladat, ahol az új dotnet core mellett döntöttem backenden és Angular frontendet használtam. A dotnet űj feltörekvő technológiának tűnik, aminek a megtanulását hosszű távon kifizetődőnek találtam. Az Angular pedig már bevált technológia, mert az AngularJS gondolkodását örökölte, de a performancián sokat javítottak.

# Project felépítése

A projektet egy mappában hoztam létre, mert két külön részből áll a program. Először úgy gondoltam, hogy Visual Studio-t fogunk minden programrész megírására, de később ez változott, így külön szerkezetbe került a webes felület.

# Fejlesztés menete, problémák

Először a dotnet backendet hoztam létre. Itt beállítottam a fordításhoz szükséges beállításokat.

Az írók listázásához létrehoztam a végpontot. Itt problémát jelentett az adat mappa beállítása, erre a dotnet appsettings.json fájljába létrehoztam ehhez egy bejegyzést, és azt betöltöttem a program indulásakor. A beállításokat egy osztályon kereszül dependency injectionhöz hozzáadva értem el a végpontok kódjából. Az adatok tárolásához a repository mintát használtam, ezzel most ismerkedtem meg. Egy repository tárolja a szükséges adatokat és egy közös interfészt nyújt hozzá. A dependency injectionnel jól működik együtt, mert az interfész implementációja bármikor lecserélhető, így a függés kisebb a kód részei között. Ha a dependency injectionben csak interfészket adunk meg, akkor kikényszeríti az ilyen használatot. Az első modellt is létrehoztam az írókhoz. Ez csak formális, enélkül is megoldható lett volna probléma, de hosszú távon nyitottabb a program a fejlesztésre.

A következő lépés a frontend létrehozása. Ezt  közös mappába raktam a dotnet programmal. A forráskód elkülönül, mert a projektet angular-cli használatával generáltam, és külön mappát hoz létre a forráskódnak. A frontend kód kimeneti mappáját a wwwroot-ra állítottam, így ha a backend szolgál ki is el tudja küldeni a fájlokat. Ehhez be kellett állítani a dotnet build-hez a frontend kód előállítását is.

Ha a frontendet akartam fejleszteni, akkor proxy beállításokkal el tudtam érni a backendet. Ehhez az angular-cli által beépített proxyt használtam. Így ha a backend és a frontend is watch módban futott, akkor is elértem az oldalt, és minden módosításra újra fordult a kód releváns része, majd frissült a weboldal.

Az előző minta szerint létrehoztam az írók listázásához az irományaik listázását is, majd azok adatait is elküldte a szerver. Ehhez JSON formátumot használtam.

A frontend kód ezután már megkapta a megfelelő adatokat az írások vizualizálásához. Ezt először egy sebesség felméréssel kezdtem. Az svg és a canvas technológiák között kellett választanom. A saját gépemen az svg gyorsabban rajzolt ki adott számú vonalat, mint a canvas, így az svg mellett döntöttem. A kirajzolás így is túlságosan lassú volt, mert minden adat kiírásához újra betöltötte a backendről az adatokat a frontend. Ezt az RxJS share függvényével oldottam meg, ami a további kérések között megosztja a lekérdezés eredményét.

Az írások sokszor kicsinek tűntek, ezt a nagyítás funkció implementálása oldotta meg. Ennek ellenére még mindig nehéz volt a vonalakra rákattintani. Az ötlet az lett, hogy egy vastagabb átlátszó vonalat is rajzolok az előzőre, amire már könnyebb rákattintani. A problémát megoldotta, de újat vetett fel, hogy a kirajzolás kétszer lassabb is lett.

A vonalak sebességét az svg path alkalmazásával tudtam gyorsítani. Ígya a böngészőnek csak egy vonalat kellett kirajzolni, ami hosszű és bonyolult vonalaknál sokat számított. Körökkel jelültem a vonalak elejét és végét, ezt a path-ból ki kellett emelni, mert már nem volt ismert a kezdő és a végpont.

A keret már működött, már csak a módosításokat kellett a vonalakon kezelni és a frissített verziót elküldeni a backendnek. Ehhez egy service-t hoztam létre a frontenden, hogy egy helyre kerüljenek az összetartozó kódrészletek.

A következő írásra léptetés nehéz feladat volt, mert az írok között is működnie kellett. Erre a megoldás az írók és irományok cache-elése volt. A tárból fel tudja a program olvasni a következő irományt, ha nincs ilyen a következő írót. Ez a megoldás azt a problémát vetette fel, hogy a kijelölések az egyes irományok között megmaradtak, mert csak a sorszámukat mentettem el a kijelölésnek.

A gyorsgombok hozzáadása a gyorsabb kezeléshez egyszerű volt az angular2-hotkeys modullal.

Végül a program design-ja készült el, ami nagyon letisztult, és az adatokra koncentrál, pár egyszerű animációval. Minden a gyors használhatóság igényei szerint készült.

A program használata során észre vettük, hogy a speciális karakterek az XML fájlból nem jól vannak visszakódolva. Ezt a backend már visszakódolta, de a bemeneti fájl készítői kétszer kódolták. A backendhez lett adva még egy visszakódolás, mert a JSON-ben nincs értelme tovább küldeni a speciális karaktereket.