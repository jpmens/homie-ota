<h2>Homie device inventory</h2>

<a href="/firmware">Homie device firmware</a>

<h3>Registered devices</h3>
<table border="1">
<thead>
<tr>
  <td>device</td><td>name</td><td>online</td><td>ipaddress</td><td>uptime</td><td>signal</td><td>fwname</td><td>fwversion</td>
</tr>
</thead>
%for device in sorted(db):
<tr>
<td>{{device}}</td>
%for item in ['name', 'online', 'localip', 'uptime', 'signal', 'fwname', 'fwversion']:
  %if item in db[device]:
    <td>{{db[device][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>

<h3>Schedule OTA update</h3>
<form action="/update" method="post" enctype="multipart/form-data">
  <table border="0">
    <tr><td>Device:</td>
<td><select name="device">
%for device in sorted(db):
  <option value="{{device}}">{{device}} ({{db[device]['fwname']}} v{{db[device]['fwversion']}})</option>
%end
</select></td></tr>
    <tr><td>Version (x.x.x):</td><td><input type="text" name="version"></td></tr>
    <tr><td>Schedule:</td><td><input type="submit" value="GO!"></td></tr>
  </table>
</form>



