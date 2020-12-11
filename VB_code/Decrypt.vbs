'Als eerst moet er een plek komen waar de tekst die gedecodeerd moet worden, ingevuld kan worden. Deze tekst wordt mySecret genoemd.
set x = Wscript.CreateObject("Wscript.Shell")
mySecret = inputbox("enter text to be dencoded")
'Om de tekst te kunnen decoderen moet de tekst eerst omgedraaid worden, omdat dit ook gedaan is bij het coderen.
MySectret = strReverse(mySecret)
'Om te kunnen weten wat de gedecodeerde tekst is wordt er een nieuw tabblad geopend met de gedecordere tekst.
x.Run "%windir%\notepad"
'Geef het programma even tijd om de tekst te decoderen.
wscript.sleep 1000
x.sendkeys encode(mySecret)
'Hier wordt een functie aangemaakt die elke letter van de tekst met vijf letter van het alfabet wordt terug gedraaid
Function encode(s)
For i = 1 To Len(s)
newtxt = Mid(s, i, 1)
newtxt = Chr(Asc(newtxt)-5)
coded = coded & newtxt
Next
encode = coded
End Function
