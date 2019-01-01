<!DOCTYPE html>
<html>
<head>
  <title>Homie devices</title>
  <meta http-equiv="refresh" content="60" />

  <link rel="stylesheet" href="{{base_url}}/styles.css">
  <script type="text/javascript" src="{{base_url}}/jquery.min.js"></script>
  <!-- https://github.com/lastdates/pBar -->
  <script type="text/javascript" src="{{base_url}}/jquery.pBar.min.js"></script>
</head>
<body>
<h2>Homie device inventory</h2>

<p>
[<a href="{{base_url}}/firmware">Homie device firmware</a>] [<a href="{{base_url}}/log">Log</a>]
</p>

<h3>Registered devices</h3>
<table border="1">
<thead>
<tr>
  <th>online</th><th>signal</th><th>device</th><th>ipaddress</th><th>uptime</th><th>fwname</th><th>fwversion</th><th>name</th>
</tr>
</thead>
%for device in sorted(db):
<tr>
   <td class="online"><img src="{{base_url}}/{{db[device].get('state', 'false')}}.png"
   		      alt="{{db[device].get('state', 'false')}}" /></td>

%if db[device].get('state', 'false') == 'ready':
   <td class="signal"><div class="pBar" data-from="0" data-to="{{ db[device].get('signal', 0) }}"></div></td>
%else:
   <td class="signal"><div class="pBar" data-from="0" data-to="0"></div></td>
%end
   <td class="device"><a href="{{base_url}}/device/{{device}}">{{device}}</a></td>

%for item in ['localip', 'human_uptime']:
  %if item in db[device] and db[device].get('state', 'false') == 'ready':
    <td>{{db[device][item]}}</td>
  %else:
    <td></td>
  %end
%end

%for item in ['fwname', 'fwversion', 'name']:
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
<form action="{{base_url}}/update" method="post" enctype="multipart/form-data">
  <table border="0">
    <tr><td>Device:</td>
    <td><select name="device">
    	<option value="-" selected>Select device...</option>
%for device in sorted(db):
  <option value="{{device}}">{{device}} ({{db[device].get('fwname', "")}} @ {{db[device].get('fwversion', "")}})</option>
%end
    </select></td></tr>
    <tr><td>Firmware:</td>
    <td><select name="firmware">
    	<option value="-" selected>Select firmware...</option>
%for firmware in sorted(fw):
  <option value="{{fw[firmware]['firmware']}}@{{fw[firmware]['version']}}">{{fw[firmware]['firmware']}} @ {{fw[firmware]['version']}}</option>
%end
    </select></td></tr>
    <tr><td>Schedule:</td><td><input type="submit" value="GO!"></td></tr>
  </table>
</form>


</body>
</html>
