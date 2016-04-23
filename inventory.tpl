<h2>Homie device inventory</h2>
<table border="1">
<thead>
<tr>
	<td>Device</td><td>Online</td><td>IP</td><td>Uptime</td><td>Signal</td><td>fwname</td><td>fwversion</td><td>name</td>
</tr>
</thead>
%for device in db:
<tr>
<td>{{device}}</td>
%for item in ['online', 'localip', 'uptime', 'signal', 'fwname', 'fwversion', 'name']:
  <td>{{ db[device][item] }}</td>
%end
</tr>
%end
</table>
