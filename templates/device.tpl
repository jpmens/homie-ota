<!DOCTYPE html>
<html>
<head>
  <title>Homie device - {{device}}</title>
  <meta http-equiv="refresh" content="60" />
  <script type="text/javascript" src="{{base_url}}/jquery.min.js"></script>
  <link rel="stylesheet" href="{{base_url}}/styles.css">
  </head>
<body>
<h2>Homie device details</h2>

<p>
[<a href="{{base_url}}/">Homie device inventory</a>] [<a href="{{base_url}}/log">Log</a>] [<a class="delete" data-delete-url="{{base_url}}/device/{{device}}" href="#">Delete</a>]
</p>

<h3>Details for device {{device}}</h3>
<table border="1">
<thead>
<tr>
  <th>key</th><th>value</th>
</tr>
</thead>
%for item in sorted(data):
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
%for key in sorted(sensor):
<tr>
  <td class="detailkey">{{key}}</td>
  <td class="detailvalue">{{ sensor[key] }}</td>
</tr>
%end
</table>
<script type="application/javascript">
$('.delete').bind('click', function (e){
  e.preventDefault();
  if (confirm("Are you sure to delete this device?")) {
    $.ajax({
      url: $(this).data('delete-url'),
      type: 'DELETE',
      async: true
    })
    .done(function() {
      alert('Deleted device');
      window.location.href = '{{base_url}}/';
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
