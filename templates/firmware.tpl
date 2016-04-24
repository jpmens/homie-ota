<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  </head>
<body>
<h2>Homie device firmware</h2>

<p>
[<a href="/">Homie device inventory</a>] [<a href="/log">Logfile</a>]
</p>

<h3>Existing Firmware</h3>
<table border="1">
<thead>
<tr>
  <th>firmware</th><th>version</th><th>filename</th><th>size</th>
</tr>
</thead>
%for path in sorted(fw):
<tr>
%for item in ['firmware', 'version', 'filename', 'size']:
  %if item in fw[path]:
    <td>{{fw[path][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>

<br>

<h3>Firmware upload</h3>
<form action="/upload" method="post" enctype="multipart/form-data">
  <table border="0">
    <tr><td>Select autodetectable binary sketch:</td><td><input type="file" name="upload"></td></tr>
    <tr><td>Upload:</td><td><input type="submit" value="GO!"></td></tr>
  </table>
</form>

</body>
</html>
