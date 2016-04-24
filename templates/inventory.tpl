<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  </head>
<body>
<h2>Homie device inventory</h2>

<p>
[<a href="/firmware">Homie device firmware</a>] [<a href="/log">Logfile</a>]
</p>

<h3>Registered devices</h3>
<table border="1">
<thead>
<tr>
  <th>online</th><th>device</th><th>ipaddress</th><th>uptime</th><th>signal</th><th>fwname</th><th>fwversion</th><th>name</th>
</tr>
</thead>
%for device in sorted(db):
<tr>
<td>
    <img src="/{{db[device].get('online', 'false')}}.png" alt="{{db[device].get('online', 'false')}}" />
    </td>
<td>{{device}}</td>
%for item in ['localip', 'uptime', 'signal', 'fwname', 'fwversion', 'name']:
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



</body>
</html>
