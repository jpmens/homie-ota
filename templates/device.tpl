<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/styles.css">
  </head>
<body>
<h2>Homie device details</h2>

<p>
[<a href="/">Homie device inventory</a>] [<a href="/log">Log</a>]
</p>

<h3>Details for device {{device}}</h3>
<table border="1">
<thead>
<tr>
  <th>key</th><th>value</th>
</tr>
</thead>
%for item in data:
<tr>
  <td class="detailkey">{{item}}</td>
  <td class="detailvalue">{{ data[item] }}</td>
</tr>
%end
</table>

</body>
</html>
