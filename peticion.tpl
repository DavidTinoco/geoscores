%include('header.tpl')
<form action="/localizados" method="post">
	<label>Liga: </label>
	<select name "liga">
		<option selected value="0">Elija una liga</option>
		<option value="1">Liga Santander</option>
		<option value="2">Liga Adelante</option>
	</select>
    <label>Jornada: </label>
    <INPUT type="number" min='1' max='42' name="jornada" size="2" required/><br>
    <INPUT type="submit" value="Consultar">
</form>
%include('foot.tpl')
