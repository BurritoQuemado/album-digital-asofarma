from random import randint
from django.http import HttpResponse
from cards.models import Department, Card, Rarity


def populate_database(self):
    departments = [
        ["Finanzas", "ROMERO GUTIERREZ ADRIANA", "Dentro de este equipo se encuentran 17 colaboradores, quienes se enfocan en realizar distintas tareas administrativas, legales, y financieras con el objetivo de tener un orden y control monetario en nuestra compañía, para que de esta manera CWT alcance  los resultados propuestos a fin el año. \nUn logro importante dentro del área, fue un excelente manejo del flujo del efectivo y control de presupuesto durante 2017.    "],
        ["IT", "GARCIA DIAZ CARLOS MANUEL", "Esta área se encuentra liderada por Charly, quien ha permanecido en CWT desde el 2000.\nDurante 2017 el equipo de IT hizo posible activar nuestro BCP y mitigar los contratiempos que el terremoto de Septiembre ocasionó en México, instalándonos a nueva oficina temporal. \nAsí mismo Charly se encargó de la migración que se realizada del sistema de TMA a Nevada, EUA durante 2017.\nActualmente Charly y su equipo tienen el reto de mudar e instalar a todos los empleados en Latitud nuestra nueva oficina de CWT México para mediados del 2018."],
        ["Dirección General", "VERA PRENDES GERARDO", "Gerardo es el capitán del equipo, que, auxiliado por todas y cada una de las distintas áreas de la organización tiene la responsabilidad de guiar y ejecutar  las estrategias y planes, para llegar a los objetivos establecidos en México, desde su llegada hace dos años  todo el equipo ha adoptado cambios muy positivos, siempre guiados por  los valores corporativos fundamentales y enfocado en  las nuevas tendencias del mercado que recaen en nuestra estrategia digital 3.0.\nEn los último años Gerardo ha permitido que la organización  cumpla con los objetivos globales  y se mantenga la alineación del equipo. Él trabaja diariamente comprometido y motivado,  confiando en cada una de las personas que conforman esta gran organización. "],
        ["Implementaciones", "7 personas", "El equipo que se encarga de ejecutar el proceso operativo, el cual puede ser para nuevos clientes, fusión de clientes o separación de los mismos. El área es intermediaria entre el proceso de ventas y la asignación del Program Manager. El equipo tiene 7 personas quienes son las responsables del mismo, y se encargan de ejecutar el proceso y comenzar instruyendo a nuestros clientes para mantener la mejor atención con los mismos. \n"],
        ["Marketing", "MEDELLIN FARIAS RENE ", "René es el líder de Marketing de productos para la región de habla hispana. A partir de su llegada se han estandarizado procesos relevantes en la imagen de CWT México, así como propuesto ideas y estrategias que han permitido reposicionar a CWT México. Rene ha participado en la organización de varios eventos tanto externos como internos, quien nos ha representado como embajador de marca. Su área está en constante movimiento y él es el responsable para que la imagen, mensajes clave, productos y estrategia de marca de México se encuentre alineada para distinguirnos con nuestros clientes. "],
        ["Meeting & Events", "OLVERA DIAZ AMALIA, CEBALLOS ESTRADA RICARDO", "M&E es una de las dos  divisiones del negocio y  es la parte creativa de la organización. M&E son los encargados de convertir las ideas en resultados tangibles. El área se encarga de planear, organizar y ejecutar eventos, convenciones, viajes de incentivo, etc. para nuestros clientes y demostrar el lado innovador de la organización.\nEl área de M&E operaciones está liderada por dos elementos clave: Amalia, quién  guiada en su experiencia, es la encargada de toda la operación y ejecución de eventos y convenciones.\n Ricardo, quien se enfoca en la prospección, búsqueda  y diversificación de nuevos clientes para M&E."],
        ["Program Management", "PALMA CORTES ALBERTO", "Alberto y su equipo tienen la responsabilidad de mantener la relación 1:1 con el Cliente.  Program Management es el encargado de escuchar las sugerencias y necesidades que el cliente tiene respecto a los servicios que ofrecemos, para de esta manera mantenerlo satisfecho y en sintonía con todas las áreas que integran a la organización.\nEl objetivo del PM es apoyar a nuestros Clientes en la optimización de sus programas de viaje mediante el análisis de su política, compartiendo mejores prácticas e implementando nuestra tecnología y servicios de excelencia. \nDurante el  2017 PM mantuvo una relación sobresaliente con 200 + clientes y obtuvo un porcentaje de retención  de 99.8% para México. \n"],
        ["Recursos Humanos", "GOMEZ PEÑA  LUCIANA", "Recursos Humanos se preocupa por el bienestar de la gente analizando nuestro talento interno, proporcionando programas de formación a la medida, atrayendo y reteniendo talentos, desarrollando al personal y analizando nuestros programas y políticas de compensación para que tengamos el mejor equipo. \nAdemás, acompañamos la estrategia de negocio con certificaciones y programas que consiguen el alcance de los objetivos. Todo esto en un marco de comunicación efectiva con campañas que mantengan informado a todos nuestros jugadores.\nLu, junto con su staff global de Compensaciones, Talent Aquisition y el Shared Service de Recursos Humanos, están para brindar ayuda y apoyo!\n"],
        ["Supplier Management", "BORTOLIN  LEONARDO ROBERTO", "Leo se encarga de representar a CWT con nuestros proveedores preferenciales. Leo es el responsable de que internamente el equipo  Comercial y de Traveler sevices conozcan cuales son nuestros primary suppliers para que la negociaciones con éstos sean las óptimas. \n Leo desarrolla y ejecuta el cumplimiento de los porcentajes que tienen que ver con el revenue de suppliers y se enfocan en la fidelización que CWT tiene con éstos, llegando a los números establecidos. Para mantener al personal motivado y con nuestros suppliers preferenciales en su top of mind, Leo internamente realiza eventos para todos los empleados, así como distintas dinámicas al o largo del año."],
        ["Traveler Services", "DUNO CARRILLO ELISEO JESUS, SOSA MELENDEZ BERTHA ESPERANZA", "Traveler Services (TS) es uno de los motores dentro de la organización. TS está orientado a ofrecer una experiencia excepcional a nuestros clientes. \nDebido a la experiencia del equipo y el servicio personalizado que ofrecen, permiten que CWT sea un referente sobresaliente dentro del mercado nacional, apoyando a nuestros clientes y el crecimiento de nuestro negocio.\nEliseo D es responsable de TS en la región de LATAM y su principal función es liderar la operación, dirigiendo la ejecución de estrategias y la implementación de las diversas herramientas tecnológicas que nos permitan ser los mejores en lo que hacemos. \nPor su parte Bertha S cuenta con la experiencia para acompañar de cerca al equipo, viviendo nuestros valores y desarrollando nuestro potencial para lograr el éxito.\n"],
        ["Ventas", "ACEVES LOPEZ GABRIELA, RANGEL AGUILERA ATZIRI", "El equipo de ventas para Business Travel (BT)  tiene un gran reto año con año que es llegar a la meta comercial. En 2017 se cerraron  más de 30+ clientes y se sobrepasó el objetivo de ventas, alcanzando $130MUSD. 2018 no es la excepción, y se tendrá que llegar al número planteado para cumplir con los objetivos anuales.\nLo pilares de nuestro equipo de ventas son:\nGabriela, quien es la encargada de las cuentas GPS. Gaby reporta a CWT Américas y las principales cuentas que ella busca, tienen con requisitos especiales para ser clasificadas en este rubro (volumen, número de países que participan, TRX)\nA su vez Atziri, quien nos representa en México en  BT, en 2017  obtuvo un reconocimiento por ser una de las vendedoras más comprometidas a nivel global en CWT durante 2017."]
    ]

    rarity = ['special', 'low', 'medium', 'high']

    cards = [
        # 1
        ["special", "badge", "Finanzas", "badge", "2018-05-23", True],
        ["low", "MONDRAGON MONDRAGON MARIA GUADALUPE", "Finanzas", "SUPERVISOR CONTABLE", "2015-03-17", False],
        ["low", "ONOFRE ZAMUDIO ALMA GUADALUPE", "Finanzas", "GERENTE DE ADMINISTRACION Y FINANZAS", "2008-09-29", False],
        ["low", "ROSALES RAMIREZ EMMA ROSA", "Finanzas", "JEFE DE CUENTAS POR PAGAR", "2014-10-03", False],
        ["special", "ROMERO GUTIERREZ ADRIANA LORENA", "Finanzas", "DIRECTOR DE ADMON. Y FINANZAS ", "2015-06-22", False],
        [None, "ACEVEDO JAIMES CLAUDIA ANGELICA", "Finanzas", "ANALISTA DE COBRANZA", "2017-08-16", False],
        [None, "BLANCO CORTES JORGE ALBERTO", "Finanzas", "CAJERO", "2003-10-16", False],
        [None, "CATARINO RAMIREZ ESTELA", "Finanzas", "ANALISTA CONTABLE", "2016-09-13", False],
        [None, "CRUZ LOPEZ GUILLERMO", "Finanzas", "AUXILIAR CUENTAS POR COBRAR", "1993-01-04", False],
        [None, "FLORES CASADO HUGO", "Finanzas", "CONTRALOR", "2016-05-11", False],
        [None, "IBARRA BLANCAS JOSE ALBERTO", "Finanzas", "AUXILIAR SERVICIOS GENERALES", "2017-11-13", False],
        [None, "JIMENEZ CABRERA MAGALI LORENA", "Finanzas", "AUXILIAR CUENTAS POR PAGAR", "2013-06-24", False],
        [None, "LORENZO REYES AMANDA", "Finanzas", "JEFE DE ADMON EN EFECTIVO ", "2011-04-26", False],
        [None, "MONTALVO ROMERO MARIA DEL CARMEN", "Finanzas", "JEFE CUENTAS POR COBRAR", "2008-08-05", False],
        [None, "NOLASCO VILLANUEVA JUAN MIGUEL", "Finanzas", "CAJERO", "2003-06-01", False],
        [None, "RIVERA PIÑA ARMANDO", "Finanzas", "ANALISTA DE COBRANZA", "2017-08-16", False],
        [None, "VILLANUEVA ORTEGA MARIA PAOLA", "Finanzas", "AUXILIAR CUENTAS POR PAGAR", "2017-06-05", False],
        # 2
        ["special", "badge", "IT", "badge", "2018-05-23", True],
        ["special", "GARCIA DIAZ CARLOS MANUEL", "IT", "GERENTE DE IT", "2000-08-21", False],
        # 3
        ["special", "badge", "Dirección General", "badge", "2018-05-23", True],
        ["low", "TORRES VAZQUEZ ANDREA", "Dirección General", "ASISTENTE EJECUTIVA", "2016-05-16", False],
        ["special", "VERA PRENDES GERARDO", "Dirección General", "DIRECTOR GENERAL", "2016-03-01", False],
        # 4
        ["special", "badge", "Implementaciones", "badge", "2018-05-23", True],
        ["low", "CRUZ OLGUIN MONICA", "Implementaciones", "GERENTE DE IMPLEMENTACIONES", "1999-06-28", False],
        ["low", "ELIZONDO AYALA GLORIA YUDITH", "Implementaciones", "GERENTE DE IMPLEMENTACIONES", "2012-01-05", False],
        ["low", "GOMEZ SANCHEZ SONIA", "Implementaciones", "GERENTE DE IMPLEMENTACIONES", "2015-02-23", False],
        ["low", "LEYVA CRUZ EDER URIEL", "Implementaciones", "GERENTE DE IMPLEMENTACIONES", "2008-08-18", False],
        ["low", "MORENO GONZALEZ ARGELIA", "Implementaciones", "GERENTE DE IMPLEMENTACIONES", "2014-02-17", False],
        [None, "ALPUIN RAMOS ILSE GABRIELA", "Implementaciones", "ASESOR DE TRAVELER SERVICES", "2014-06-02", False],
        [None, "DE JESUS MOSCO GRACIELA ELVIRA", "Implementaciones", "ONLINE IMPLEMENTATION SPECIALIST", "2018-04-1", False],
        [None, "MONSALVO RODRIGUEZ KAREM", "Implementaciones", "ONLINE IMPLEMENTATION SPECIALIST", "2017-05-02", False],
        [None, "PEREZ CONTRERAS ESMERALDA JANETTH", "Implementaciones", "ASESOR DE TRAVELER SERVICES", "2013-07-08", False],
        [None, "QUEVEDO SEQUI ALEJANDRO ENRIQUE", "Implementaciones", "PRODUCT DELIVERY MANAGER", "2015-08-03", False],
        # 5
        ["special", "badge", "Marketing", "badge", "2018-05-23", True],
        ["low", "MEDELLIN FARIAS RENE RAMIRO", "Marketing", "MARKETING PRODUCT MANAGER", "2017-05-16", False],
        # 6
        ["special", "badge", "Meeting & Events", "badge", "2018-05-23", True],
        ["low", "AGUILAR HERNANDEZ ITZEL", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2012-04-09", False],
        ["low", "ALVARADO MONDRAGON JORGE FERNANDO", "Meeting & Events", "SUPERVISOR SERVICIOS AEREOS M&E ", "2013-02-25", False],
        ["low", "CEBALLOS ESTRADA RICARDO", "Meeting & Events", "GERENTE COMERCIAL", "2017-08-07", False],
        ["low", "DEL OLMO DIAZ ISSIS HEIDI", "Meeting & Events", "EJECUTIVO COMERCIAL M&E", "2013-09-17", False],
        ["low", "DEL POZO PORTILLO XOCHITL", "Meeting & Events", "GERENTE DE ESTRATEGIA DE EVENTOS", "2013-10-01", False],
        ["low", "FLORES OJEDA TOBIAS", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2004-10-04", False],
        ["low", "GARCIA BECERRA ARIZBETH LILIANA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2014-09-22", False],
        ["low", "GUZMAN MAYORAL LUIS GONZALO", "Meeting & Events", "EJECUTIVO COMERCIAL M&E", "2018-01-02", False],
        ["special", "OLVERA DIAZ AMALIA", "Meeting & Events", "GERENTE DE OPERACIONES M&E", "2007-11-01", False],
        [None, "CABRERA LOPEZ JUAN CARLOS", "Meeting & Events", "RSVP COORDINADOR AEREO", "2016-06-01", False],
        [None, "CABRERA MORALES CONSUELO", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2017-07-03", False],
        [None, "CAHUANTZI MELENDEZ MAXIMILIANO", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2017-05-16", False],
        [None, "CARCAMO REYES MARIA DEL CARMEN", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2016-02-26", False],
        [None, "CASILLAS RAMOS GERARDO", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2018-04-2", False],
        [None, "CASTILLO CHRISTY ADRIANA GABRIELA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2016-09-26", False],
        [None, "CONTRERAS PERCASTRE ALEJANDRO", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2018-04-2", False],
        [None, "CORPUS PACHECO NORMA", "Meeting & Events", "COORDINADOR ADMINISTRATIVO", "2016-09-01", False],
        [None, "DEL VALLE DUARTE MARIANA", "Meeting & Events", "RSVP COORDINADOR AEREO", "2016-02-02", False],
        [None, "FLORES LOPEZ HARUMI SAYURI", "Meeting & Events", "RSVP COORDINADOR AEREO", "2016-12-26", False],
        [None, "GARCIA MANCILLA ERIKA GUADALUPE", "Meeting & Events", "AUXILIAR ADMINISTRATIVO", "2018-01-16", False],
        [None, "GOMEZ ESTRADA GLORIA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2017-02-16", False],
        [None, "GOMEZ HURTADO JORGE ALEXIS", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2016-10-24", False],
        [None, "GONZALEZ DUEÑAS JUAN MANUEL", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2018-04-1", False],
        [None, "GONZALEZ PALOMARES PAULINA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2018-02-06", False],
        [None, "GONZALEZ RAMIREZ MARIA ANDREA", "Meeting & Events", "AUXILIAR ADMINISTRATIVO", "2014-01-13", False],
        [None, "HERNANDEZ REYES ALEJANDRA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2017-07-03", False],
        [None, "HERNANDEZ RODRIGUEZ ESMERALDA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2014-01-13", False],
        [None, "HERNANDEZ TORRES JUAN MANUEL", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2017-09-18", False],
        [None, "MARQUEZ AGUILAR DAVID", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2018-02-06", False],
        [None, "MARTAGON CASTRO NELY LESLY", "Meeting & Events", "SUPERVISOR SERVICIOS AEREOS M&E ", "2014-01-13", False],
        [None, "ORTIZ MONTEON ITZEL MONSERRAT", "Meeting & Events", "SUPERVISOR SERVICIOS TERRESTRES M&E ", "2011-10-11", False],
        [None, "PECH BORROMEO JESUS ARTURO", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2014-06-02", False],
        [None, "RODRIGUEZ GARCIA GABRIELA", "Meeting & Events", "COORDINADOR SERVICIOS TERRESTRES M&E", "2016-12-01", False],
        [None, "RODRIGUEZ HERRERA BLANCA ROSA", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2016-02-22", False],
        [None, "TOLENTINO MARTINEZ NANCY JANET", "Meeting & Events", "AUXILIAR ADMINISTRATIVO", "2017-03-21", False],
        [None, "VELAZCO VELASCO GUILLERMO ARTURO", "Meeting & Events", "COORDINADOR SERVICIOS AEREOS M&E", "2016-10-05", False],
        [None, "VILLANUEVA ORTEGA MIRIAM DEYANIRA", "Meeting & Events", "AUXILIAR ADMINISTRATIVO", "2016-03-29", False],
        # 7
        ["special", "badge", "Program Management", "badge", "2018-05-23", True],
        ["low", "GUZMAN GUZMAN KENIA PATRICIA", "Program Management", "ASISTENTE DIRECCION", "2017-01-02", False],
        ["low", "MARTINEZ MENDOZA MARIA DE LOURDES", "Program Management", "SUPERVISOR", "1998-05-18", False],
        ["low", "ORTEGA OTAÑEZ IRACEMA", "Program Management", "PROGRAM MANAGER REGIONAL", "2015-11-10", False],
        ["low", "PARRALES PELAYO MARIANA", "Program Management", "PROGRAM MANAGER REGIONAL", "2012-12-03", False],
        ["low", "RINCON BARRERA SONIA PIEDAD", "Program Management", "SMB PROGRAM SERVICE CENTER SUPERVISOR", "2004-11-22", False],
        ["low", "TELLO ARROYAVE OSCAR DANIEL", "Program Management", "ENTERPRISE PROGRAM MANAGER", "2004-02-09", False],
        ["low", "VAQUERO LUNA ANA LILIA", "Program Management", "PROGRAM MANAGER ", "2004-09-13", False],
        ["low", "VAZQUEZ LOPEZ VERONICA", "Program Management", "CORPORATE PROGRAM MANAGER", "1995-03-06", False],
        ["special", "PALMA CORTES ALBERTO", "Program Management", "DIRECTOR DE PROGRAM MANAGER", "2016-02-02", False],
        [None, "ABREU RIVERA MAYRA", "Program Management", "SMB PROGRAM SERVICE CENTER SUPERVISOR", "2018-04-1", False],
        [None, "CABALLERO CASTILLO JAIME", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2012-05-29", False],
        [None, "CAMPOS ESPEJEL CLAUDIA", "Program Management", "PROGRAM MANAGER ", "2010-04-16", False],
        [None, "CHAVEZ DAVILA VIRGINIA", "Program Management", "PROGRAM MANAGER ", "2013-06-24", False],
        [None, "GARCIA LIMA DANIELA FERNANDA", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2018-03-16", False],
        [None, "GARCIA PEÑA RAUL", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2004-08-02", False],
        [None, "HERNANDEZ TORRES DAVID", "Program Management", "PROGRAM MANAGER", "2018-04-1", False],
        [None, "HURTADO SALAS PAULA", "Program Management", "PROGRAM MANAGER ", "2017-12-04", False],
        [None, "JOAN IVAN GARRIDO PATIÑO ", "Program Management", "PROGRAM MANAGEMENT", "2018-04-2", False],
        [None, "LOPEZ CORPUS LIZET MADAY", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2018-04-1", False],
        [None, "MACALPIN MARTINEZ HORACIO", "Program Management", "PROGRAM MANAGER ", "2016-12-26", False],
        [None, "MARTINEZ HERNANDEZ AARON ALVAR", "Program Management", "PROGRAM MANAGER JR", "2017-06-05", False],
        [None, "MORALES VIZCAYA STEPHANIE MARGARITA", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2014-04-02", False],
        [None, "PELAEZ CARMONA ALBERTO", "Program Management", "ANALISTA INFORMACION Y ESTADISTICA", "2017-09-18", False],
        # 8
        ["special", "badge", "Recursos Humanos", "badge", "2018-05-23", True],
        ["special", "GOMEZ PEÑA LUCIANA", "Recursos Humanos", "GERENTE SR. RECURSOS HUMANOS", "2016-11-01", False],
        # 9
        ["special", "badge", "Supplier Management", "badge", "2018-05-23", True],
        ["special", "BORTOLIN LEONARDO ROBERTO", "Supplier Management", "GERENTE DE SUPPLIER MANAGEMENT", "2017-05-22", False],
        # 10
        ["special", "badge", "Traveler Services", "badge", "2018-05-23", True],
        ["low", "BARROSO HERNANDEZ MARIA ANTONIETA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2004-11-08", False],
        ["low", "COLIN SERVIN SOCORRO DALIA", "Traveler Services", "SUPERVISOR", "2001-04-02", False],
        ["low", "FRANCOELIA VERONICA", "Traveler Services", "SUPERVISOR", "2003-02-24", False],
        ["low", "GARCIAROBERTO", "Traveler Services", "COORDINADOR ANALISTA RELACION", "1992-03-19", False],
        ["low", "HERNANDEZ TORRES ISRAEL", "Traveler Services", "SUPERVISOR", "2012-05-14", False],
        ["low", "HERRERA TORRES DIANA", "Traveler Services", "BUSINESS ANALYST", "2012-04-09", False],
        ["low", "IBARRA SANTIAGO OSCAR ALEJANDRO", "Traveler Services", "JEFE DE EQUIPO", "2012-08-27", False],
        ["low", "JUAREZ MARTINEZ CRISTOPHER ISAAC", "Traveler Services", "JEFE DE EQUIPO", "2006-05-02", False],
        ["low", "LOPEZ CONTRERAS CIRO", "Traveler Services", "JEFE DE EQUIPO", "2002-03-11", False],
        ["low", "RATNAYAKA GONZALEZ NEIL AMARASIRI", "Traveler Services", "SUPERVISOR", "2008-07-14", False],
        ["low", "ROSAS BARRERA DIANA EVA", "Traveler Services", "SUPERVISOR", "2003-12-09", False],
        ["special", "DUNO CARRILLO ELISEO JESUS", "Traveler Services", "VICEPRESIDENTE TRAVELER SERVICES LATAM ", "2014-10-06", False],
        ["special", "SOSA MELENDEZ BERTHA ESPERANZA", "Traveler Services", "DIRECTOR TRAVELER SERVICES", "1996-07-11", False],
        [None, "AGUILAR SANCHEZ CARLOS ALBERTO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-09-01", False],
        [None, "ALATORRE VAZQUEZ ANABELL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2005-01-03", False],
        [None, "ALCALA LUNA CARLOTA MARIA EUGENIA", "Traveler Services", "JEFE DE EQUIPO", "2001-02-01", False],
        [None, "AMEZQUITA GUILLEN SILVIA", "Traveler Services", "JEFE DE EQUIPO", "2012-04-16", False],
        [None, "ARAGON MARTINEZ LESLIE ARGELIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-08-01", False],
        [None, "BAEZ PEÑA JESUS", "Traveler Services", "JEFE DE EQUIPO", "1997-11-01", False],
        [None, "BARRERA TORRES JACQUELINE", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-04", False],
        [None, "BENITEZ MEDINA LOURDES CONCEPCION", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1999-05-16", False],
        [None, "CHAGOYA MENDOZA ANA ISABEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2011-12-19", False],
        [None, "CISNEROS RAMIREZ DANIELA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-30", False],
        [None, "COLINA RASCON ALEJANDRO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-07-25", False],
        [None, "CORTES RIVERA CATALINA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-23", False],
        [None, "CRUZ LLANOS KARLA FABIOLA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-01-08", False],
        [None, "CUEVAS OLIVARES MIGUEL EDUARDO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-08-01", False],
        [None, "DAVILA REYES MAYRA ANGELICA", "Traveler Services", "JEFE DE EQUIPO", "2000-04-03", False],
        [None, "DE LA CRUZ MEDINA JUAN ANTONIO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-10-06", False],
        [None, "DIAZ JIMENEZ MARIA ELENA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1996-06-24", False],
        [None, "DIEGO MARTINEZ JULIO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-07-25", False],
        [None, "ESPINOZA GARCIA LAURA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-10-31", False],
        [None, "ESTRADA GONZALEZ MYRYAM ALHELI", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-09", False],
        [None, "FRAUSTO HERNANDEZ TANIA BERENICE", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-08-15", False],
        [None, "GALVAN SOSA HUMBERTO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-05-19", False],
        [None, "GARAY BARRERA MARIANA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-04-21", False],
        [None, "GARCIA HERNANDEZ ANTONIO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2000-01-10", False],
        [None, "GODINEZ CUEVAS ROSALBA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-05-05", False],
        [None, "GOMEZ HERNANDEZ ANA LAURA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-04-21", False],
        [None, "GOMEZ VAZQUEZ MARTHA LUCIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-08-15", False],
        [None, "GRAJALES OSORIO LEONARDO JOAQUIN", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2013-11-11", False],
        [None, "HERNANDEZ PEREZ MARIA DEL ROSARIO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-08-22", False],
        [None, "HERNANDEZ VERDUGO EVELIA", "Traveler Services", "JEFE DE EQUIPO", "2004-06-16", False],
        [None, "HERRERIAS SALGADO CARLOS DE JESUS", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-09", False],
        [None, "JIMENEZ CORTEZ JUAN CARLOS", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-05-14", False],
        [None, "KIM GOMEZ ADRIAN HUMBERTO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-01-08", False],
        [None, "LOPEZ AGUIRRE RICARDO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-06-12", False],
        [None, "LOPEZ DAVALOS KARINA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-01-08", False],
        [None, "LUQUE GODINEZ DANIEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-05-14", False],
        [None, "MALDONADO SOTELO JULIO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-09-01", False],
        [None, "MARISCAL SUAREZ GUILLERMO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-04-03", False],
        [None, "MARTINEZ REYNA ANDREA ELIZABETH", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-04", False],
        [None, "MARTINEZ SIERRA HUMBERTO", "Traveler Services", "ENTRENADOR", "1993-04-01", False],
        [None, "MARTINEZ TORRES ROSARIO DEL CARMEN A", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2007-10-22", False],
        [None, "MATA TRISTAN LILIA PATRICIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-06-13", False],
        [None, "MEDINA GOVEA JORGE MANUEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-04-14", False],
        [None, "MENDEZ ALMARAZ CLAUDIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-08-22", False],
        [None, "MENDOZA RAMIREZ TERESA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2005-05-25", False],
        [None, "MILLAN OJEDA AISLINN YVONNE", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-06-15", False],
        [None, "MIRIEL MENDEZ IZCHEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-16", False],
        [None, "MONTERO RODAL JUAN GUALBERTO", "Traveler Services", "JEFE DE EQUIPO", "2015-05-04", False],
        [None, "MONTES LOPEZ ALMA LETICIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2000-08-25", False],
        [None, "MORA ROMERO TANIA MONSERRAT", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-02-04", False],
        [None, "MORENO CHAVEZ CASANDRA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-06-08", False],
        [None, "MORENO SEGUNDO ANA LAURA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-10-31", False],
        [None, "MUNOZ SIFUENTES FRANCISCO JAVIER", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-04-05", False],
        [None, "NAJERA HERNANDEZ ANA ISABEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1997-09-17", False],
        [None, "NAVA LOPEZ DOLORES", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2004-03-22", False],
        [None, "NAVARRO RODRIGUEZ LORENA ELIZABETH", "Traveler Services", "JEFE DE EQUIPO", "2005-01-10", False],
        [None, "OVIEDO BARRON KARINA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-04-28", False],
        [None, "OVIEDO PALACIOS RAUL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-07-16", False],
        [None, "PADILLA AGUILAR LUIS JAVIER", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-04", False],
        [None, "PEREZ HERRERA JESSICA CONCEPCION", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2013-07-16", False],
        [None, "PUENTE VARGAS JUAN CARLOS", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-23", False],
        [None, "RAMIREZ MARTINEZ DIMPNA DEL CARMEN", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2016-10-03", False],
        [None, "RAMIREZ SAAVEDRA MARIA DEL CARMEN", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-05-21", False],
        [None, "ROMERO PACHECO ESPERANZA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1998-10-05", False],
        [None, "ROMERO PEREZ YOLANDA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2000-12-13", False],
        [None, "SAAVEDRA FLORES NANCY", "Traveler Services", "JEFE DE EQUIPO", "2006-11-21", False],
        [None, "SALGADO PEREZ GUADALUPE GABRIELA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-07-07", False],
        [None, "SANCHEZ CARRILLO ERICK ALBERTO", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2012-04-23", False],
        [None, "SANCHEZ FERREIRA JUAN CARLOS", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-04", False],
        [None, "SANCHEZ HERNANDEZ MARIA GUADALUPE", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2017-07-06", False],
        [None, "SANCHEZ ROMERO SERGIO DANIEL", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1999-09-13", False],
        [None, "TAPIA GONZALEZ EDGAR EULISES", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-04", False],
        [None, "TORRES OCAÑA MARTIN DE JESUS", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2004-02-13", False],
        [None, "ULLOA VILLARREAL NORMA OLIMPIA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "1998-12-03", False],
        [None, "VARGAS CORTES ISAI", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2014-04-21", False],
        [None, "VEGA SANCHEZ CAROLINA", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2015-05-25", False],
        [None, "VELAZCO SILVA JOSE CUTBERTO", "Traveler Services", "JEFE DE EQUIPO", "2006-02-07", False],
        [None, "VERDUZCO ALVAREZ MARTIN", "Traveler Services", "EJECUTIVO DE RESERVACIONES", "2013-06-25", False],
        # 11
        ["special", "badge", "Ventas", "badge", "2018-05-23", True],
        ["low", "ACEVES LOPEZ GABRIELA ROSALBA", "Ventas", "DIRECTOR DE VENTAS REGIONAL", "2014-02-24", False],
        ["special", "RANGEL AGUILERA ATZIRI AMEYALLY", "Ventas", "DIRECTOR DE VENTAS", "2016-11-14", False],
        [None, "CRUZ MEJIA CHRISTIAN", "Ventas", "EJECUTIVO DE VENTAS", "2018-01-02", False],
        [None, "RUIZ CRUZ GLADIS ANAID", "Ventas", "EJECUTIVO DE VENTAS", "2017-01-02", False],
        [None, "SANTILLAN MENDEZ KARLA VANESSA", "Ventas", "PROPOSAL MANAGER SPECIALIST ", "2003-06-01", False, 1]
    ]

    # fill departments
    for i in range(len(departments)):
        Department.objects.update_or_create(
            name=departments[i][0],
            description=departments[i][2],
            head=departments[i][1]
        )

    # fill rarity type
    for i in range(len(rarity)):
        Rarity.objects.update_or_create(description=rarity[i])

    # fill users
    # for i in range(len(cards)):
    #     department = Department.objects.get(name=cards[i][2])
    #     rarity = Rarity.objects.get(description=cards[i][0]) if cards[i][0] is not None else Rarity.objects.get(id=randint(3, 4))
    #     Card.objects.update_or_create(
    #         name=cards[i][1],
    #         fk_department=department,
    #         description=cards[i][3],
    #         active=True,
    #         arrival_date=cards[i][4],
    #         order_card=i,
    #         fk_rarity=rarity,
    #         wave=randint(1, 2)
    #     )

    return HttpResponse('Seed done')
