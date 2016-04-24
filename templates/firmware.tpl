<h2>Homie device firmware</h2>

<a href="/">Homie device inventory</a>

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
    <tr><td>Firmware:</td><td><input type="text" name="firmware"></td></tr>
    <tr><td>Version (x.x.x):</td><td><input type="text" name="version"></td></tr>
    <tr><td>Select File:</td><td><input type="file" name="upload"></td></tr>
    <tr><td>Upload:</td><td><input type="submit" value="GO!"></td></tr>
  </table>
</form>

