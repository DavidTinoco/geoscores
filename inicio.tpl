%include('header.tpl')
<h3> Bienvendido a GeoScores </h3>
<p>
	Tu web para mantenerte al día de la clasifiación y resultados de las principales ligas españolas
</p>
<div class = "match">
	<div class = "container">
		<div class="match-table">
% for l,v,f,h,m in zip(doc.xpath("//local"),doc.xpath("//visitor"),doc.xpath("//competition_name"),doc.xpath("//hour"),doc.xpath("//minute")):
<!--Partido -->
			<div class = "table-rows">
				<div class="table-hedding">
					<h3>{{f.text[1:]}}</h3>
				</div>
				<div class="table-row">
					<div class="t-match">
						<div class="col-md-4 table-address">
							<div class="list-hedding">
								<h4>Partido</h4>
							</div>
							<h5>{{l.text[1:]}} vs {{v.text[1:]}}</h5>
						</div>	
						<div class="col-md-4 table-country">
							<div class="list-hedding">
								<h4>Hora</h4>
							</div>
							<h5>{{h.text[1:]}}:{{m.text[1:]}}</h5>
						</div>
						<div class="clearfix"> </div>
					</div>
				</div>
			</div>
<!--Partido -->
%end
		</div>
	</div>
</div>
%include('foot.tpl')