<h2>Homie device firmware</h2>
<table border="1">
<thead>
<tr>
  <td>firmware</td><td>filename</td><td>version</td>
</tr>
</thead>
%for path in sorted(fw):
<tr>
%for item in ['firmware', 'filename', 'version']:
  %if item in fw[path]:
    <td>{{fw[path][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>
