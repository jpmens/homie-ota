<h2>Homie device firmware</h2>
<h3>Existing Firmware</h3>
<table border="1">
<thead>
<tr>
  <td>firmware</td><td>version</td><td>filename</td>
</tr>
</thead>
%for path in sorted(fw):
<tr>
%for item in ['firmware', 'version', 'filename']:
  %if item in fw[path]:
    <td>{{fw[path][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>

<br/>

<h3>Firmware upload</h3>
<form action="/upload" method="post" enctype="multipart/form-data">
  Firmware: <input type="text" name="firmware">
  <br/><br/>
  Version (x.x.x): <input type="text" name="version">
  <br/><br/>
  Select File: <input type="file" name="upload">
  <br/><br/>
  <input type="submit" value="Upload" />
</form>
