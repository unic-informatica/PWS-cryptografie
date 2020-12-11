'Als eerst moet er een plek komen waar de tekst die gecodeerd moet worden, ingevuld kan worden. Deze tekst wordt mySecret genoemd.
set x = Wscript.CreateObject("Wscript.Shell")
mySecret = inputbox("enter text to be encoded")
'Om het lastiger te maken de tekst te oncijferen wordt de tekst eerst omgedraaid voordat het wordt gecodeerd.
MySectret = strReverse(mySecret)
'Om te kunnen weten wat de gecodeerde tekst is wordt er een nieuw tabblad geopend met de gecordeerde tekst.
x.Run "%windir%\notepad"
'Geef het programma even tijd om de tekst te coderen.
wscript.sleep 1000
x.sendkeys encode(mySecret)
'Hier wordt een functie aangemaakt die elke letter van de tekst met vijf letter van het alfabet wordt opgeschoven.
Function encode(s)
Function encode(s)
For i = 1 To Len(s)
newtxt = Mid(s, i, 1)
newtxt = Chr(Asc(newtxt)+5)
coded = coded & newtxt
Next
encode = coded
End Function
