<!DOCTYPE html>
<html>
<head>
  <title>Homie device - {{device}}</title>
  <meta http-equiv="refresh" content="60" />

  <link rel="stylesheet" href="/styles.css">
  </head>
<body>
<h2>Homie device details</h2>

<p>
[<a href="/">Homie device inventory</a>] [<a href="/log">Log</a>] [<a class="delete" data-delete-url="/device/{{device}}" href="#">Delete</a>]
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

<h3>Sensor data for device {{device}}</h3>
<table border="1">
<thead>
<tr>
  <th>key</th><th>value</th>
</tr>
</thead>
%for item in sensor:
<tr>
  <td class="detailkey">{{item}}</td>
  <td class="detailvalue">{{ sensor[item] }}</td>
</tr>
%end
</table>
<script type="application/javascript">
$('.delete').bind('click', function (e){
  e.preventDefault();
  if (confirm("Are you sure to delete the file?")) {
    $.ajax({
      url: $(this).data('delete-url'),
      type: 'DELETE',
      async: true
    })
    .done(function() {
      alert('Deleted device');
      window.location.href = '/';
    })
    .fail(function(e) {
      alert('Error: ' + e.statusText);
    })
  }
  return false;
})
</script>
</body>
</html>
