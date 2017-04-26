%include('header.tpl')
<form action="/resultado" method="post">
	<label>Liga: </label>
	<select name "liga">
		<option selected value="0">Elija una liga</option>
		<option value="1">Liga Santander</option>
		<option value="2">Liga Adelante</option>
	</select>
	</br>
    <label>Jornada: </label>
    <INPUT type="text" name="jornada" size="2">
    </br>
    <INPUT type="submit" value="Consultar">
</form>
%include('foot.tpl')
