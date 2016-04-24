<h2>Homie device firmware</h2>
<table border="1">
<thead>
<tr>
  <td>firmware</td><td>version</td><td>filename</td>
</tr>
</thead>
%for firmware in sorted(fw):
<tr>
<td>{{firmware}}</td>
%for item in ['version', 'filename']:
  %if item in fw[firmware]:
    <td>{{fw[firmware][item]}}</td>
  %else:
    <td></td>
  %end
%end
</tr>
%end
</table>
