No midi support yet
monome 256 not supported yet
currently, only arduinomes are supported
osc system messages are not all supported (see MonomeOscInterpreter.py)

A great thank you to the team behind simpleOSC from which I took many ideas and some code (in OscIn.py)

dependencies: pySerial, simpleOSC(0.2.7)

À faire:
- option pour dire si c'est un monome ou un arduinome-> set baudrate et tout dans SerialDevice (voir sources originales) [PAS NÉCESSAIRE SI DÉTECTION AUTO]
- mettre GPL

implémenter ce qui manque (dont détection automatique de l'OS, du type de device et du port à ouvrir pour accéder au device)

-------------------
Idées:
-Client ligne de texte
-Prog GUI à part dans le style de Bidule/Reaktor

----------------------------
À faire:
-implémenter les bundles
-se débarrasser de simpleOSC
-chaque module devrait avoir une doc qui vient avec pour dire les paramètres à passer au constructeur. cette doc est accessible par le CLI (structurée pr etre lue par le GUI?)
-diagramme CLI et AbstractModule(avec les liens d'héritage nécessaires)
-message de patienter pour la fermeture de l'application (implémenté par le client)

-------------------------
À tester:
-tout ce qui est OSC
-tester plusieurs in/out

-------------
Prochaine version:
-OscToMidiConverter extends MonomeOscOut (et meme chose pour MonomeOscIn pour led?)
-MonomeOscInterpreter -> handle sys messages (single monome) ( _oscController.send() pour avertir les applications d'un changemente de prefix par exemple, voir code c++)

---------
Guide: 
-tjrs caller setActive() après construction sur tous modules
-ne pas oublier de définir le messageSize du device
-première ligne des fichiers dans le dossier modules doit être "#import 1" pour dire si on peut en faire des objets par le GUI/CLI. Les #import 1 doivent implémenter AbstractModule
-les modules doivent avoir def __init__ sur une ligne seulement
-les fichiers de modules ne peuvent pas commencer par _GUI car cela servira à l'implémentation du GUI
-les modules doivent remplir leur liste self.runnables et self.sets pour dire quelles méthodes peuvent être exécutées par le client
-les modules qui implémentent SerialDevice doivent ajouter setDevice(string device) et getDevice() à leur runnables[]
