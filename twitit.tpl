%include('header.tpl')
<form action="/twitit" method="post">
	<p><textarea name="tweet" maxlenght="140">
		{{cuerpo}}
	</textarea></p>
</form>
%include('foot.tpl')