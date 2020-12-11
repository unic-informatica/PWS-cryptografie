set x = Wscript.CreateObject("Wscript.Shell")
mySecret = inputbox("enter text to be encoded")
MySectret = strReverse(mySecret)
x.Run "%windir%\notepad"
wscript.sleep 1000
x.sendkeys encode(mySecret)
 
Function encode(s)
For i = 1 To Len(s)
newtxt = Mid(s, i, 1)
newtxt = Chr(Asc(newtxt)+5)
coded = coded & newtxt
Next
encode = coded
End Function
