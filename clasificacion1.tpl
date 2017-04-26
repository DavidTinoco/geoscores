%include('header.tpl')
<h3> Clasificación Liga Santander </h3>
<h2 align="center"> Jornada Actual</h2>
<table class ="wrapper row3" align="center">
	<tr>
		<td></td>
		<td width="200">Equipo</td>
		<td>Puntos</td>
	</tr>
	%for i,j,n in zip(doc.xpath("//team"), doc.xpath("//points"),xrange(50)):
	<tr>
		<td align="right">{{n+1}}</td>
		<td align="left">{{i.text}}</td>
		<td align="right">{{j.text}}</td>
	</tr>
	%end
</table>
%include('foot.tpl')