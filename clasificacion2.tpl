%include('header.tpl')
<h3> Clasificación Liga 1|2|3 </h3>
<form action="/clasificacion/liga123" method="post">
    <label>Jornada: </label>
    <INPUT type="number" min='1' max='42' name="jornada" size="2" required/><br>
    <INPUT type="submit" value="Consultar">
</form>
<div class="copyright">
	<h2> Jornada {{jornada}}</h2>
</div>
<table>
	<tr>
		<td>Pts.</td>
		<td>Equipo</td>
		<td>Puntos</td>
	</tr>
	%for i,j,n in zip(doc.xpath("//team"), doc.xpath("//points"),xrange(50)):
	<tr>
		<td>{{n+1}}</td>
		<td>{{i.text[1:]}}</td>
		<td>{{j.text[1:]}}</td>
	</tr>
	%end
</table>
%include('foot.tpl')