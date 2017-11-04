import logging
from queue import Queue
from threading import Thread
from telegram import Bot , MessageEntity , chat , message
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters ,BaseFilter ,filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '337200725:AAFbDoHN6Do7nZyW7F3X2EEYcLKh358gWDA'

curse_list = ["Kir", "Kos" , "Jende" ,  "Chende" , "Ghahbe" ,  "Gahbe" , "Gahba" ,  "Binamos",
              "Binamus", "Bi namos", "Be ga"  , "Bega" , "Gaidam" ,  "Gayidam" ,  "Gaedam"  ,"Gaydam" , "Gaidamet"
              ,"Gayidamet" ,"Gaydamet" ,  "Gaedamet" ,"Gaidamesh" ,  "Gaedamesh" ,  "Gaydamesh" ,  "Gayidamesh" ,
              "Gaid" ,
              "Gaed" ,  "Gayid" , "Gaidan" ,  "Gayidan" ,  "Gaidesh", "Gaedan" ,  "Gayidesh" ,  "Gaydesh" ,  "Gaidesh",
              "Gaedesh" ,  "Gaedim " , "Gaidim" ,  "Gayidim" ,  "Gaydim" , "Gaidimet" , "Gaedemet" , "Gayidemet",
              "Gaydemet" ,
              "Gaesh" , "Gayesh" ,  "Gaiesh" ,  "Gaidi" , "Gaedi" ,  "Gaydi" ,  "Gayidi" , "Begai"  , "Begayi",
              "Begae"  , "Begay"
               , "Sepokht"  , "Sepookht" ,  "Sepukht" ,  "Sepokhtam" ,  "Sepookhtam" ,  "Sepukhtam" ,
              "Sepokhti", "Sepookhti" ,
              "Sepukhti" ,  "Sepokhtamet" ,"Sepookhtamet" , "Sepukhtamet" ,  "Sepokhtimet" ,  "Sepokhtemet" ,
              "Sepookhtimet" ,
              "Sepookhtemet" , "Sepukhtimet" ,  "Sepukhtemet" ,  "Sepokhtamesh" ,  "Sepookhtamesh" , "Sepukhtamesh" ,
              "Sepokhtimesh",
              "Sepokhtemesh" , "Sepookhtimesh" ,  "Sepookhtemesh" , "Sepukhtimesh" , "Sepukhtemesh" , "Sepokhtesh" ,
              "Sepookhtesh" ,
              "Sepukhtesh" ,  "Sepokhtand" , "Sepookhtand" ,  "Sepoukhtand" , "Kharkose" ,  "Khar kose" , "Kharkosde" ,
              "Khar kosde" ,
              "Kosde"  ,"Kosdi" ,  "Koste" , "Kosi" ,  "Madargahbe" , "Madar gahbe" , "Madarghahbe" , "Madar ghahbe" ,
              "Madarjende" ,
              "Madar jende" ,  "Binamos" ,  "Binamus" , "Binamoos" , "Benamos" , "Benamoos"  ,"Benamus" ,"bynamoos" ,
              "Bynamos" , "Bynamus" ,
              "namos" , "namus"  ,"namoos" , "namos" , "namoos" , "namus" ,  "namos" ,
              "kosde" , "kose" , "Kharkose" , "Kos" , "Koos" , "Bisharaf" , "Bysharaf" , "Besharaf" ,
              "Be sharaf" , "Dayos" , "Daus" , "Daios" , "Dayoos", "Koskesh", "Kosmaghz" ,"Kosmagz" ,
              "Avazi" , "Avazy" , "Lashi" , "Lashy" , "Lashe" , "Lashee" , "Kos sher" , "Kosher"  ,"Kossher" ,
              "Koslis" , "Koslys",
              "Zerzer" , "Zer" , "Kon" , "Koon" , "Kun" , "Kony" , "Koony" , "Kuny" , "Koni" , "Kooni" ,
              "Kuni" , "Kondeh" ,
              "Konde" , "Koonde" , "Koondeh" , "Kunde" , "Kundeh" ,
              "Konpare" , "Kunpare" ,
              "Koonpare" , "Kongoshad" , "Koongoshad" , "Kungoshad" ,
              "Konam" , "Koonam" , "Kunam" ,
              "Konet" , "Koonet" , "Kunet" , "Konesh" , "Koonesh" , "Kunesh" , "Konemon" , "Konemun" , "Konemoon" ,
              "Kunemon" , "Kunemoon" ,
              "Kunemun" , "Koonemon", "Koonemoon" , "Koonemun" , "Konesh" , "Koonesh" , "Kunesh" , "Koneshon" ,
              "Koneshoon" , "Koneshun" ,
              "Kuneshon" , "Kuneshoon" , "Kuneshun" , "Kooneshon" , "Kooneshoon" , "Kooneshun" , "Konemon" ,
              "Konemoon" , "Konemun" , "Koonemon" ,
              "Koonemoon" , "Koonemun" , "Kunemon" ,  "Kunemoon" , "Kunemun" , "Koneshon" , "Koneshoon" , "Koneshun" ,
              "Kuneshon" , "Kuneshoon" ,
              "Kuneshun" , "Kooneshon" , "Kooneshun" , "Kooneshoon" , "Koneshan" , "Kuneshan" , "Kooneshan" , "Tokhmi",
              "tokhmam" ,
              "tokhmet" , "Betokhmam" , "Betokhmet" , "Khaye" , "Khaie" , "Khayemal" , "Khaiemal" ,

              "Khayelis" , "Khayelys" , "Khayeles" , "Khaielis" , "Khaielys" , "Khaielys" ,
              "Kiram" , "Kyram" , "Keram" , "Kiret" , "Keret" , "Kyret" ,
              "Kiresh" ,
              "Kyresh" , "Keresh" , "Kiremon"  ,"Kiremoon" , "Kiremun" , "Kyremon" , "Kyremoon" , "Kyremun" ,
              "Keremon" , "Keremoon" ,
              "Keremun" ,"Guzidi" , "Guzydy" , "Guzidy" , "Guzedy" , "Guzedi" , "Gozid" , "Gozed" , "Gozyd", "Guzid",
              "Guzed" ,
              "Guzyd" ,"Goozid" , "Goozed" , "Goozyd" , "Gozidim" , "Goozidim", "Goozydym" , "Goozedim" , "Goozydem" ,
              "Gozydym" ,
              "Gozidem", "Guzidim", "Guzedym", "Guzydym", "Guzedem", "Gozidin", "Gozedin", "Gozydyn", "Goziden",
              "Gozidyn", "Goozidin",
              "Goozedin" , "Goozydyn", "Gooziden", "Goozidyn", "Guzidin", "Guzedin", "Guzydyn", "Guziden", "Guzidyn",
              "Gozidand",
              "Gozydand", "Gozedand", "Goozidand", "Goozedand" ,"Goozydand", "Guzidand", "Guzydand", "Guzedand",
              "Gozidan", "Gozedan",
              "Gozydan", "Goozidan", "Goozydan", "Goozedan", "Guzidan", "Guzydan", "Guzedan", "Gozo", "Gozoo",
              "Gozu", "Goozo", "Goozu",
              "Goozoo", "Guzu", "Guzoo" ,"Guzo", "Gooz" ,"Goz" ,"Guz" ,"Goh", "Gooh", "Goh nakhor","Gohnakhor",
              "Gohmaghz",
              "Gohmagz", "Goh" ,"Gohi", "Gohy", "Gohe", "Sexy", "Seksy", "3xy", "Seksy", "Pv",
              "Pivi", "Peve", "Pi vi",
              "Pe ve", "Pi ve", "Sikil", "Sikyl", "Sikel", "Sekil", "Sekyl", "Sekel", "Sykil", "Sykel", "Sykyl",
              "Sikajam", "Sekajam",
              "Sykajam", "Sikiram", "Sikyram", "Sikeram", "Sykyram", "Sykiram", "Sykeram", "Sekiram", "Sekeram",
              "Sekyram", "Sikisan",
              "Sikysan", "Sikesan", "Sykysan", "Sykisan", "Sykesan", "Sekesan", "Sekysan", "Sekesan", "Sikajakh",
              "Sykajakh", "Sekajamh",
              "Sikirokh" ,"Sykyrokh", "Sekirokh", "Sekerokh", "Sikirookh", "Sykyrookh", "Sekirookh", "Sekerookh",
              "Sikirukh" ,"Sykyrukh",
              "Sekirukh", "Sekerukh", "Sikisiz", "Sikysyz", "Sekesiz", "Sekisiz", "Sekysyz", "Sykisiz", "Kysesiz",
              "Kykisez", "Sikisuz",
              "Kikisooz", "Sikisoz", "Sikilar", "Sikylar", "Sikelar", "Sykilar", "Sykylar", "Sykelar", "Sekelar",
              "Sekilar", "Sekylar",
              "Sikimajan", "Sikymajan", "Sikemajan", "Sykemajan","Sik", "Sykimajan", "Sykymajan", "Sekimajan",
              "Sekymajan", "Sekemajan", "Sihmiram",
              "Syhmiram", "Sehmiram", "Sihmeram", "Syhmeram", "Sehmeram", "Sihmyram", "Sehmyram", "Syhmyram",
              "Sikamasan", "Sykamasan",
              "Sekamasan", "Sikimajan", "Sikymajan", "Sikemajan", "Sykimajan", "Sykemajan", "Sykymajan",
              "Sekimajan", "Sekymajan",
              "Sekemajan", "Nanasighahba", "Nanasigahba", "Nanasygahba", "Nanasyghahba", "Nanasegahba",
              "Nanaseghahba","Amjekh",
              "Delekh", "Delikh", "Asgih",
              "Asgyh", "Asgeh", "Eshah", "Gamaz", "Ghamaz","Bia pv" , "Fuck", "Fuckin", "Fucking" , "Asshole", "Ass",
              "Fucked", "Fucker", "Shit",
              "Kir","kiir", "kiiir", "kiiiir", "kiiiiir", "kiiiiiir", "kiiiiiiir", "kiiiiiiiir", "kiiiiiiiiir",
              "kiiiiiiiiiir", "kiiiiiiiiiiir", "kiiiiiiiiiiiir", "kiiiiiiiiiiiiir", "kiiiiiiiiiiiiiir",
              "kiiiiiiiiiiiiiiir", "kiiiiiiiiiiiiiiiir", "kiiiiiiiiiiiiiiiiir", "kiiiiiiiiiiiiiiiiiir",
              "kiiiiiiiiiiiiiiiiiiir", "kiiiiiiiiiiiiiiiiiiiir","Kiri", "kiiri", "kiiiri", "kiiiiri", "kiiiiiri",
              "kiiiiiiri", "kiiiiiiiri",
              "kiiiiiiiiri", "kiiiiiiiiiri", "kiiiiiiiiiiri", "kiiiiiiiiiiiri", "kiiiiiiiiiiiiri", "kiiiiiiiiiiiiiri",
              "kiiiiiiiiiiiiiiiri", "kiiiiiiiiiiiiiiiiri", "kiiiiiiiiiiiiiiiiiri", "kiiiiiiiiiiiiiiiiiiri",
              "kiiiiiiiiiiiiiiiiiiiri", "kiiiiiiiiiiiiiiiiiiiiri","Kiri", "kirii", "kiriii", "kiriiii", "kiriiiii",
              "kiriiiiii", "kiriiiiiii",
              "kiriiiiiiii", "kiriiiiiiiii", "kiriiiiiiiiii", "kiriiiiiiiiiii", "kiriiiiiiiiiiii", "kiriiiiiiiiiiiii",
              "kiriiiiiiiiiiiiiii", "kiriiiiiiiiiiiiiiii", "kiriiiiiiiiiiiiiiiii", "kiriiiiiiiiiiiiiiiiii",
              "kiriiiiiiiiiiiiiiiiiii", "kiriiiiiiiiiiiiiiiiiiii",
              "Kiram", "kiiram", "kiiiram", "kiiiiram", "kiiiiiram", "kiiiiiiram", "kiiiiiiiram", "kiiiiiiiiram",
              "kiiiiiiiiiram", "kiiiiiiiiiiram", "kiiiiiiiiiiiram", "kiiiiiiiiiiiiram", "kiiiiiiiiiiiiiram",
              "kiiiiiiiiiiiiiiram", "kiiiiiiiiiiiiiiiram", "kiiiiiiiiiiiiiiiiram", "kiiiiiiiiiiiiiiiiiram",
              "kiiiiiiiiiiiiiiiiiiram", "kiiiiiiiiiiiiiiiiiiiram", "kiiiiiiiiiiiiiiiiiiiiram",
              "Ga", "gaa", "gaaa", "gaaaa", "gaaaaa", "gaaaaaa", "gaaaaaaa", "gaaaaaaaa", "gaaaaaaaaa", "gaaaaaaaaaa",
              "gaaaaaaaaaaa", "gaaaaaaaaaaaa", "gaaaaaaaaaaaaa", "gaaaaaaaaaaaaaa", "gaaaaaaaaaaaaaaa",
              "gaaaaaaaaaaaaaaaa", "gaaaaaaaaaaaaaaaaa", "gaaaaaaaaaaaaaaaaaa", "gaaaaaaaaaaaaaaaaaaa",
              "gaaaaaaaaaaaaaaaaaaaa",
              "Bega", "gegaa", "begaaa", "begaaaa", "begaaaaa", "begaaaaaa", "begaaaaaaa", "begaaaaaaaa",
              "begaaaaaaaaa", "begaaaaaaaaaa", "begaaaaaaaaaaa", "begaaaaaaaaaaaa", "begaaaaaaaaaaaaa",
              "begaaaaaaaaaaaaaa", "begaaaaaaaaaaaaaaa", "begaaaaaaaaaaaaaaaa", "begaaaaaaaaaaaaaaaaa",
              "begaaaaaaaaaaaaaaaaaa", "begaaaaaaaaaaaaaaaaaaa", "begaaaaaaaaaaaaaaaaaaaa",
              "Begai", "begaai", "begaaai", "begaaaai", "begaaaaai", "begaaaaaai", "begaaaaaaai", "begaaaaaaaai",
              "begaaaaaaaaai", "begaaaaaaaaaai", "begaaaaaaaaaaai", "begaaaaaaaaaaaai", "begaaaaaaaaaaaaai",
              "begaaaaaaaaaaaaaai", "begaaaaaaaaaaaaaaai", "begaaaaaaaaaaaaaaaai", "begaaaaaaaaaaaaaaaaai",
              "begaaaaaaaaaaaaaaaaaai", "begaaaaaaaaaaaaaaaaaaai", "begaaaaaaaaaaaaaaaaaaaai",
              "Begai", "begaii", "begaiii", "begaiiii", "begaiiiii", "begaiiiiii", "begaiiiiiii", "begaiiiiiiii",
              "begaiiiiiiiii", "begaiiiiiiiiii", "begaiiiiiiiiiii", "begaiiiiiiiiiiii", "begaiiiiiiiiiiiii",
              "begaiiiiiiiiiiiiii", "begaiiiiiiiiiiiiiii", "begaiiiiiiiiiiiiiiiii", "begaiiiiiiiiiiiiiiiiii",
              "begaiiiiiiiiiiiiiiiiiii", "begaiiiiiiiiiiiiiiiiiiii","Gaid", "gaaid", "gaaaid", "gaaaaid", "gaaaaaid",
              "gaaaaaaid", "gaaaaaaaid", "gaaaaaaaaid", "gaaaaaaaaaid", "gaaaaaaaaaaid", "gaaaaaaaaaaaid",
              "gaaaaaaaaaaaaid",
              "gaaaaaaaaaaaaaid", "gaaaaaaaaaaaaaaid", "gaaaaaaaaaaaaaaaid", "gaaaaaaaaaaaaaaaaid",
              "gaaaaaaaaaaaaaaaaaid",
              "gaaaaaaaaaaaaaaaaaaid", "gaaaaaaaaaaaaaaaaaaaid", "gaaaaaaaaaaaaaaaaaaaaid","Gaidam",
              "gaaidam", "gaaaidam",
              "gaaaaidam", "gaaaaaidam", "gaaaaaaidam", "gaaaaaaaidam", "gaaaaaaaaidam", "gaaaaaaaaaidam",
              "gaaaaaaaaaaidam",
              "gaaaaaaaaaaaidam", "gaaaaaaaaaaaaidam", "gaaaaaaaaaaaaaidam", "gaaaaaaaaaaaaaaidam",
              "gaaaaaaaaaaaaaaaidam",
              "gaaaaaaaaaaaaaaaaidam", "gaaaaaaaaaaaaaaaaaidam", "gaidaaaaaaaaaaaaaaaaaaidam",
              "gaaaaaaaaaaaaaaaaaaaidam",
              "gaaaaaaaaaaaaaaaaaaaaidam","Gaidesh", "gaaidesh", "gaaaidesh", "gaaaaidesh", "gaaaaaidesh",
              "gaaaaaaidesh",
              "gaaaaaaaidesh", "gaaaaaaaaidesh", "gaaaaaaaaaidesh", "gaaaaaaaaaaidesh", "gaaaaaaaaaaaidesh",
              "gaaaaaaaaaaaaidesh",
              "gaaaaaaaaaaaaaidesh", "gaaaaaaaaaaaaaaidesh", "gaaaaaaaaaaaaaaaidesh", "gaaaaaaaaaaaaaaaaidesh",
              "gaaaaaaaaaaaaaaaaaidesh",
              "gaaaaaaaaaaaaaaaaaaidesh", "gaaaaaaaaaaaaaaaaaaaidesh", "gaaaaaaaaaaaaaaaaaaaaidesh","gaidish",
              "gaidiish",
              "gaidiiish", "gaidiiiish", "gaidiiiiisg", "gaidiiiiiish", "gaidiiiiiiish", "gaidiiiiiiiish",
              "gaiiiiiiiii",
              "gaidiiiiiiiiiish", "gaidiiiiiiiiiiish", "gaidiiiiiiiiiiiish", "gaidiiiiiiiiiiiiish",
              "gaidiiiiiiiiiiiiiish",
              "gaidiiiiiiiiiiiiiiish", "gaidiiiiiiiiiiiiiiiish", "gaidiiiiiiiiiiiiiiiish", "gaidiiiiiiiiiiiiiiiiish",
              "gaidiiiiiiiiiiiiiiiiii", "gaidiiiiiiiiiiiiiiiiiiish", "gaidiiiiiiiiiiiiiiiiiiiish","Gaidamet",
              "gaaidamet", "gaaaidamet", "gaaaaidamet", "gaaaaaidamet", "gaaaaaaidamet", "gaaaaaaaidamet",
              "gaaaaaaaaidamet",
              "gaaaaaaaaaidamet", "gaaaaaaaaaaidamet", "gaaaaaaaaaaaidamet", "gaaaaaaaaaaaaidamet",
              "gaaaaaaaaaaaaaidamet",
              "gaaaaaaaaaaaaaaidamet", "gaaaaaaaaaaaaaaaidamet", "gaaaaaaaaaaaaaaaaidamet", "gaaaaaaaaaaaaaaaaaidamet",
              "gaaaaaaaaaaaaaaaaaaidamet", "gaaaaaaaaaaaaaaaaaaaidamet", "gaaaaaaaaaaaaaaaaaaaaidamet","Begamon",
              "begaamon", "begaaamon", "begaaaamon", "begaaaaamon", "begaaaaaamon", "begaaaaaaamon", "begaaaaaaaamon",
              "begaaaaaaaaamon", "begaaaaaaaaaamon", "begaaaaaaaaaamon", "begaaaaaaaaaaamon", "begaaaaaaaaaaaamon",
              "begaaaaaaaaaaaaamon", "begaaaaaaaaaaaaaamon", "begaaaaaaaaaaaaaaamon", "begaaaaaaaaaaaaaaaamon",
              "begaaaaaaaaaaaaaaaaamon", "begaaaaaaaaaaaaaaaaaamon", "begaaaaaaaaaaaaaaaaaaamon",
              "begaaaaaaaaaaaaaaaaaaaamon","Begamoon", "begamooon", "begamoooon", "begamooooon",
              "begamoooooo", "begamooooooon", "begamoooooooon", "begamooooooooon","begamoooooooooon",
              "begamooooooooooon", "begamoooooooooooon", "begamooooooooooooon", "begamoooooooooooooon",
              "begamooooooooooooooon",
              "begamoooooooooooooooon", "begamooooooooooooooooon", "begamooooooooooooooooon",
              "begamooooooooooooooooooon",
              "begamoooooooooooooooooooon","Gaidamesh", "gaaidamesh", "gaaaidamesh", "gaaaaidamesh", "gaaaaaidamesh",
              "gaaaaaaidamesh",
              "gaaaaaaaidamesh", "gaaaaaaaaidamesh", "gaaaaaaaaaidamesh", "gaaaaaaaaaaidamesh", "gaaaaaaaaaaaidamesh",
              "gaaaaaaaaaaaaidamesh", "gaaaaaaaaaaaaaidamesh", "gaaaaaaaaaaaaaaidamesh", "gaaaaaaaaaaaaaaaidamesh",
              "gaaaaaaaaaaaaaaaaidamesh", "gaaaaaaaaaaaaaaaaaidamesh", "gaaaaaaaaaaaaaaaaaaidamesh",
              "gaaaaaaaaaaaaaaaaaaaidamesh",
              "gaaaaaaaaaaaaaaaaaaaaidamesh","بگای", "بگایی", "بگاییی", "بگایییی", "بگاییییی", "بگایییییی",
              "بگاییییییی", "بگایییییییی",
              "بگاییییییییی", "بگایییییییییی", "بگاییییییییییی", "بگایییییییییییی", "بگاییییییییییییی",
              "بگایییییییییییییی",
              "بگایییییییییییییییی", "بگایییییییییییییییییی", "بگایییییییییییییییییی", "بگاییییییییییییییییییی",
              "بگایییییییییییییییییییی","بگامون", "بگاموون", "بگامووون", "بگاموووون", "بگامووووون",
              "بگاموووووون", "بگامووووووو",
              "بگاموووووووون", "بگامووووووووون", "بگاموووووووووون", "بگامووووووووووون", "بگاموووووووووووون",
              "بگامووووووووووووون",
              "بگاموووووووووووووون", "بگامووووووووووووووون", "بگاموووووووووووووووون", "بگامووووووووووووووووون",
              "بگاموووووووووووووووووون",
              "بگامووووووووووووووووووون", "بگاموووووووووووووووووووون" ,"کییر", "کیییر", "کییییر", "کیییییر",
              "کییییییر", "کیییییییر",
              " کییییییییر", "کیییییییییر","کییییییییییر", "کیییییییییییر", "کییییییییییییر", " کیییییییییییییر" ,
              "کییییییییییییییر",
              "کیییییییییییییییر", "کیییییییییییییییییر", " کییییییییییییییییییر", " کیییییییییییییییییییر",
              " کییییییییییییییییییییر",
              "کییری" ,"کیییری", "کییییری", "کیییییری", "کییییییری", "کیییییییری", " کییییییییری", "کیییییییییری",
              "کییییییییییری",
              "کیییییییییییری", "کییییییییییییری", " کیییییییییییییری", "کییییییییییییییری", "کیییییییییییییییری",
              "کیییییییییییییییییری",
              " کییییییییییییییییییری", " کیییییییییییییییییییری", " کییییییییییییییییییییری","کییرم", "کیییرم",
              "کییییرم", "کیییییرم",
              "کییییییرم", "کیییییییرم", " کییییییییرم", "کیییییییییرم", "کییییییییییرم", "کیییییییییییرم",
              "کییییییییییییرم", " کیییییییییییییرم",
              "کییییییییییییییرم", "کیییییییییییییییرم", "کیییییییییییییییییرم", " کییییییییییییییییییرم",
              " کیییییییییییییییییییرم",
              " کییییییییییییییییییییرم","گا", "گاا", "گااا", "گاااا", "گااااا", "گاااااا", "گاااااااا",
              "گااااااااا", "گاااااااااا",
              "گااااااااااا", "گاااااااااااا", "گااااااااااااا", "گاااااااااااااا", "گااااااااااااااا",
              "گاااااااااااااااا",
              "گااااااااااااااااا", "گاااااااااااااااااا", "گااااااااااااااااااا", "گاااااااااااااااااااا","به گا",
              "به گاا",
              "به گااا", "به گاااا", "به گااااا", "به گاااااا", "به گاااااااا", "به گااااااااا", "به گاااااااااا",
              "به گااااااااااا",
              "به گاااااااااااا", "به گااااااااااااا", "به گاااااااااااااا", "به گااااااااااااااا",
              "به گاااااااااااااااا",
              "به گااااااااااااااااا", "به گاااااااااااااااااا", "به گااااااااااااااااااا",
              "به گاااااااااااااااااااا","بگا", "بگاا",
              "بگااا", "بگاااا", "بگااااا", "بگاااااا", "بگاااااااا", "بگااااااااا", "بگاااااااااا",
              "بگااااااااااا", "بگاااااااااااا",
              "بگااااااااااااا", "بگاااااااااااااا", "بگااااااااااااااا", "بگاااااااااااااااا", "بگااااااااااااااااا",
              "بگاااااااااااااااااا",
              "بگااااااااااااااااااا", "بگاااااااااااااااااااا","بگایی", "بگاایی", "بگااایی", "بگاااایی",
              "بگااااایی", "بگاااااایی",
              "بگاااااااایی", "بگااااااااایی", "بگاااااااااایی", "بگااااااااااایی", "بگاااااااااااایی",
              "بگااااااااااااایی",
              "بگاااااااااااااایی", "بگااااااااااااااایی", "بگاااااااااااااااایی", "بگااااااااااااااااایی",
              "بگاااااااااااااااااایی",
              "بگااااااااااااااااااایی", "بگاااااااااااااااااااایی","بگامون", "بگاامون", "بگااامون",
              "بگاااامون", "بگااااامون",
              "بگاااااامون", "بگاااااااامون", "بگااااااااامون", "بگاااااااااامون", "بگااااااااااامون",
              "بگاااااااااااامون",
              "بگااااااااااااامون", "بگاااااااااااااامون", "بگااااااااااااااامون",
              "بگاااااااااااااااامون", "بگااااااااااااااااامون",
              "بگاااااااااااااااااامون", "بگااااااااااااااااااامون", "بگاااااااااااااااااااامون",
              "گایید", "گاایید", "گااایید",
              "گاااایید", "گااااایید", "گاااااایید", "گاااااااایید", "گااااااااایید", "گاااااااااایید",
              "گااااااااااایید",
              "گاااااااااااایید", "گااااااااااااایید", "گاااااااااااااایید", "گااااااااااااااایید",
              "گاااااااااااااااایید",
              "گااااااااااااااااایید", "گاااااااااااااااااایید", "گااااااااااااااااااایید",
              "گاااااااااااااااااااایید","گائید",
              "گاائید", "گااائید", "گاااائید", "گااااائید", "گاااااائید", "گاااااااائید",
              "گااااااااائید", "گاااااااااائید",
              "گااااااااااائید", "گاااااااااااائید", "گااااااااااااائید", "گاااااااااااااائید", "گااااااااااااااائید",
              "گاااااااااااااااائید", "گااااااااااااااااائید", "گاااااااااااااااااائید", "گااااااااااااااااااائید",
              "گاااااااااااااااااااائید","گاییدم", "گااییدم", "گاااییدم", "گااااییدم", "گاااااییدم",
              "گااااااییدم", "گااااااااییدم",
              "گاااااااااییدم", "گااااااااااییدم", "گاااااااااااییدم", "گااااااااااااییدم",
              "گاااااااااااااییدم", "گااااااااااااااییدم",
              "گاااااااااااااااییدم", "گااااااااااااااااییدم", "گاااااااااااااااااییدم",
              "گااااااااااااااااااییدم", "گاااااااااااااااااااییدم",
              "گااااااااااااااااااااییدم","گائیدم", "گاائیدم", "گااائیدم", "گاااائیدم", "گااااائیدم", "گاااااائیدم",
              "گاااااااائیدم",
              "گااااااااائیدم", "گاااااااااائیدم", "گااااااااااائیدم", "گاااااااااااائیدم", "گااااااااااااائیدم",
              "گاااااااااااااائیدم",
              "گااااااااااااااائیدم", "گاااااااااااااااائیدم", "گااااااااااااااااائیدم", "گاااااااااااااااااائیدم",
              "گااااااااااااااااااائیدم",
              "گاااااااااااااااااااائیدم","گاییدش", "گااییدش", "گاااییدش", "گااااییدش", "گاااااییدش", "گااااااییدش",
              "گااااااااییدش",
              "گاااااااااییدش", "گااااااااااییدش", "گاااااااااااییدش", "گااااااااااااییدش", "گاااااااااااااییدش",
              "گااااااااااااااییدش",
              "گاااااااااااااااییدش", "گااااااااااااااااییدش", "گاااااااااااااااااییدش", "گااااااااااااااااااییدش",
              "گاااااااااااااااااااییدش",
              "گااااااااااااااااااااییدش","گائیدش", "گاائیدش", "گااائیدش", "گاااائیدش", "گااااائیدش", "گاااااائیدش",
              "گاااااااائیدش",
              "گااااااااائیدش", "گاااااااااائیدش", "گااااااااااائیدش", "گاااااااااااائیدش", "گااااااااااااائیدش",
              "گاااااااااااااائیدش",
              "گااااااااااااااائیدش", "گاااااااااااااااائیدش", "گااااااااااااااااائیدش", "گاااااااااااااااااائیدش",
              "گااااااااااااااااااائیدش", "گاااااااااااااااااااائیدش",
              "گاییدیش", "گااییدیش", "گاااییدیش", "گااااییدیش", "گاااااییدیش", "گااااااییدیش", "گااااااااییدیش",
              "گاااااااااییدیش",
              "گااااااااااییدیش", "گاااااااااااییدیش", "گااااااااااااییدیش", "گاااااااااااااییدیش",
              "گااااااااااااااییدیش",
              "گاااااااااااااااییدیش", "گااااااااااااااااییدیش", "گاااااااااااااااااییدیش",
              "گااااااااااااااااااییدیش",
              "گاااااااااااااااااااییدیش","گااااااااااااااااااااییدیش","گائیدیش", "گاائیدیش",
              "گااائیدیش", "گاااائیدیش",
              "گااااائیدیش", "گاااااائیدیش", "گاااااااائیدیش", "گااااااااائیدیش", "گاااااااااائیدیش",
              "گااااااااااائیدیش",
              "گاااااااااااائیدیش", "گااااااااااااائیدیش", "گاااااااااااااائیدیش", "گااااااااااااااائیدیش",
              "گاااااااااااااااائیدیش",
              "گااااااااااااااااائیدیش", "گاااااااااااااااااائیدیش", "گااااااااااااااااااائیدیش",
              "گاااااااااااااااااااائیدیش",
              "گاییدمت", "گااییدمت", "گاااییدمت", "گااااییدمت", "گاااااییدمت", "گااااااییدمت",
              "گااااااااییدمت", "گاااااااااییدمت",
              "گااااااااااییدمت", "گاااااااااااییدمت", "گااااااااااااییدمت","گاااااااااااااییدمت",
              "گااااااااااااااییدمت",
              "گاااااااااااااااییدمت", "گااااااااااااااااییدمت", "گاااااااااااااااااییدمت", "گااااااااااااااااااییدمت",
              "گاااااااااااااااااااییدمت", "گااااااااااااااااااااییدمت","گائیدمت", "گاائیدمت", "گااائیدمت",
              "گاااائیدمت", "گااااائیدمت",
              "گاااااائیدمت", "گاااااااائیدمت", "گااااااااائیدمت", "گاااااااااائیدمت", "گااااااااااائیدمت",
              "گاااااااااااائیدمت",
              "گااااااااااااائیدمت", "گاااااااااااااائیدمت", "گااااااااااااااائیدمت", "گاااااااااااااااائیدمت",
              "گااااااااااااااااائیدمت",
              "گاااااااااااااااااائیدمت", "گااااااااااااااااااائیدمت", "گاااااااااااااااااااائیدمت",
              "گاییدمش", "گااییدمش",
              "گاااییدمش", "گااااییدمش", "گاااااییدمش","گااااااییدمش", "گااااااااییدمش", "گاااااااااییدمش",
              "گااااااااااییدمش",
              "گاااااااااااییدمش", "گااااااااااااییدمش", "گاااااااااااااییدمش", "گااااااااااااااییدمش",
              "گاااااااااااااااییدمش",
              "گااااااااااااااااییدمش", "گاااااااااااااااااییدمش", "گااااااااااااااااااییدمش",
              "گاااااااااااااااااااییدمش",
              "گااااااااااااااااااااییدمش","گائیدمش", "گاائیدمش", "گااائیدمش", "گاااائیدمش",
              "گااااائیدمش", "گاااااائیدمش",
              "گاااااااائیدمش", "گااااااااائیدمش", "گاااااااااائیدمش", "گااااااااااائیدمش",
              "گاااااااااااائیدمش", "گااااااااااااائیدمش",
              "گاااااااااااااائیدمش", "گااااااااااااااائیدمش", "گاااااااااااااااائیدمش", "گااااااااااااااااائیدمش",
              "گاااااااااااااااااائیدمش", "گااااااااااااااااااائیدمش", "گاااااااااااااااااااائیدمش",
              "قههبه", "قههههبه", "قهههههبه",
              "قههههههبه", "قهههههههه", "قههههههههه", "قهههههههههبه", "قههههههههههبه", "قهههههههههههبه",
              "قههههههههههههبه",
              "قهههههههههههههبه", "قهههههههههههههبه","گههبه", "گههههبه", "گهههههبه", "گههههههبه", "گهههههههه",
              "گههههههههه",
              "گهههههههههبه", "گههههههههههبه", "گهههههههههههبه", "گههههههههههههبه", "گهههههههههههههبه",
              "گهههههههههههههبه","بییناموس",
              "بیییناموس", "بییییناموس", "بیییییناموس", "بییییییناموس", "بیییییییناموس", "بییییییییناموس",
              "بیییییییییناموس",
              "بیییییییییناموس", "بیییییییییییناموس", "بیییییییییییناموس", "بییییییییییییناموس","بییناموووس",
              "بییینامووس",
              "بیییینامووووس", "بیییییناموووووس", "بیییییینامووووووس", "بییییییینامووووووس", "بیییییییینامووووووس",
              "بیییییییییناموووووووس",
              "بییییییییینامووووووووس", "بیییییییییییناموووووووووس", "بیییییییییییناموووووووووووس",
              "بیییییییییییینامووووووووووووووس",
              "گائیدیم","گاییدش","گائیدش","گائدمت", "گائدمش","گائیدمت","گائید","گائیدم","گائیدن","گاییدن",
              "گایید","گاییدمش","گاییدمت",
              "گاییدم","بگا","گا","بیناموس","گهبه","قهبه","چنده","حنده","جنده","کس","کیر","سپوختند","سپوختش",
              "سپوختیمش","سپوختمش",
              "سپوختیمت","سپوختمت","سپوختی","سپوختم","سپوخت","خوار_کسته","خار_کسته","خار_کسه","خوار_کسده",
              "خار_کسده","بیناموس","پی وی"
              "بی ناموس","بی_ناموس","مادرجنده","مادرقهبه","کسته","کسده","خوارکسده","خارکسده","خوارکسه","خارکسه",
              "مادر*قهبه","مادر_قهبه",
              "مادر*جنده","مادر_جنده","مادرقهبه","مادر قهبه","مادرجنده","کسشر","کس لیس","کسشعر","کس شعر","مادر جنده",
              "لاشی","عوضی","کس مغز",
              "کس کش","کسکش","دیوس","بیشرف","بی شرف","زر*زر","زر_زر","زر زر","کونشان","کونشون","کونمون","کونش",
              "کونت","کونم","کون گشاد",
              "کونده","کونی","کون","تخمت","تخمم","تخمی","خایه*مال","خایه_مال","خایه لیس","خایه مال","خایه","دودول",
              "کیرکلفت","کیری",
              "کیرشون","کیرشان","کیرمان","کیرمون","کیرش","کیرت","کیرم","گورومساق","گورومساخ","قورومساق",
              "جیندا","قهبه","جنده",
              "سیکتر","سیکتیر","کنمش","کنمت","میکنمش","میکنمت","ریدمان","ریدند","ریدن","ریدید","ریدین",
              "ریدیم","رید","ریدی","ریدم",
              "شاشو","شاشیدند","شاشیدن","شاشیدیم","شاشید","شاشیدی","شاشیدم","گوزو","گوزیدند","گوزیدن",
              "گوزیدید","گوزیدین","گوزیدیم",
              "گوزید","گوزیدی","گوزیدم","گوز","گوهی","گوهمغز","گهمغز","گه","گوه","سسکی","سکسی","پیوی","پی وی",
              "سیکمسن","سیهمیرم",
              "سیکیمجن","سیکیلر","سیکیسیز","سیکیروخ","سیکجاخ","سیکیسن","سیکیرم","سیکجام","سیکیل","سیهدیر","سیه",
              "سیک","سیکیمجان",
              "گاماز","جندا","اسگیح","اسگیه","دلغ","دلاغ","دلاخ","دلخ","آمجخ","ننسی قهبه","گوتورن","گوت","بگائی",
              "بگایی","گائدی",
              "گائیدی","گایدی","گاییدی","گائش","گایش","گایدمت","گائدمت","گائیدیمت","گایدیم","گاییدیم","کوس","فاک"]


#print(curse_list)
def start(bot, update):
    update.message.reply_text('به خاطر انتخاب این بوت برای استفاده ممنونیم '
                              'برای استفاده از امکانات بوت کافی است بوت رو به گروه اضافه کنید. '
                              '\n'
                              'به یاد داشته باشید که برای عملکرد صحیح بوت باید ادمین گروه باشد!')


def help(bot, update):
    update.message.reply_text('بوت در صورت ادمین بودن پیام های حاوی کلمات مستهجن و لینک ها(در صورت ارسال توسط اعضای عادی) را حذف خواهد کرد!')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def delete(bot, update):
    for admin in Bot.get_chat_administrators(bot,update.message.chat['id']):
        if update.message.from_user['id'] == admin.user['id']:
            return

    Bot.delete_message(bot,chat_id = update.message.chat['id'], message_id = update.message['message_id'])

def boolean_test(curse_list,string):
    for word in curse_list:
        if string.find(word):
            return True
    return False

curse_list_not_ordinary=["بی شرف","پی وی","pi vi","pe ve","pi ve","pe vi"]


def delete_curse(bot , update):
    main_text1  =update.message.text.replace("!", " ")
    main_text2  =main_text1.replace("@", " ")
    main_text3  =main_text2.replace("#", " ")
    main_text4  =main_text3.replace("$", " ")
    main_text5  =main_text4.replace("%", " ")
    main_text6  =main_text5.replace("^", " ")
    main_text7  =main_text6.replace("&", " ")
    main_text8  =main_text7.replace("*", " ")
    main_text9  =main_text8.replace("?", " ")
    main_text10 =main_text9.replace("-", " ")
    main_text11 =main_text10.replace("_", " ")
    main_text   =main_text11.replace("   ", " ")
    for word in main_text.split():
        if ((word.strip() in curse_list) or (uncapitalize(word.strip())in curse_list)or (word.title().strip() in curse_list)or(word.upper().strip() in curse_list)):
            Bot.delete_message(bot, chat_id=update.message.chat['id'], message_id=update.message['message_id'])
        if boolean_test(curse_list_not_ordinary,main_text):
            Bot.delete_message(bot, chat_id=update.message.chat['id'], message_id=update.message['message_id'])

def uncapitalize(s):
    if len(s) > 0:
        s = s[0].lower() + s[1:].upper()
    return s

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def get_admins(bot , update):
    return Bot.get_chat_administrators(bot, chat_id = update.message.chat['id'])


# Write your handlers here


def setup(webhook_url=None):



    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)

    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))


        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler((Filters.entity('url')|Filters.entity('mention')), delete))
        dp.add_handler(MessageHandler((Filters.text),delete_curse))
        print(Bot.get_chat_administrators(bot,'-1001111360377')[0])


        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()