%include('header.tpl')
<h3> Clasificación Liga Santander </h3>
<form action="/clasificacion/ligasantander" method="post">
    <label>Jornada: </label>
    <INPUT type="number" min='1' max='38' name="jornada" size="2" required/><br>
    <INPUT type="submit" value="Consultar">
</form>
<div class="article">
	<h3> Jornada {{jornada}}</h3>
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