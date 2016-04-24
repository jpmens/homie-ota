<h2>Homie device inventory</h2>
<table border="1">
<thead>
<tr>
  <td>device</td><td>online</td><td>ipaddress</td><td>uptime</td><td>signal</td><td>fwname</td><td>fwversion</td><td>name</td>
</tr>
</thead>
%for device in sorted(db):
<tr>
<td>{{device}}</td>
%for item in ['online', 'localip', 'uptime', 'signal', 'fwname', 'fwversion', 'name']:
  %if item in db[device]:
    <td>{{db[device][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>
