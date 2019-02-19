<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Security</title>
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/core.css">
</head>
<body>


  <ul class="nav">
    <li class="nav-item"><a href="dashboard">DASHBOARD</a></li>
    <li class="nav-item"><a href="logs">LOGS</a></li>
    <li class="nav-item"><a href="surveillance">SURVEILLANCE</a></li>
    <li class="nav-item"><a href="logout">LOG OUT</a></li>
  </ul>

  <div class="content">
      <div class="floor-plan">
        <ul class="rooms">
          <h1>Room Sensor Layout</h1>
          % for room in rooms:
            <ul class="room"><h2>{{room.name.title()}}</h2>
            %  for sensor in room.sensors:
              <li class="sensor"><pre>{{sensor.name}}</pre><button class={{sensor.online}}>Online: {{sensor.online}}</button></li>
            % end

            % if not room.sensors:
              <li> No Sensors registered</li>
            % end
            </ul>
          % end
        </ul>
      </div>
  </div>


</body>
</html>
