<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Security</title>
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/core.css">
  <link rel="stylesheet" href="static/css/surveillance.css">
</head>
<body>

  <ul class="nav">
    <li class="nav-item"><a href="dashboard">DASHBOARD</a></li>
    <li class="nav-item"><a href="logs">LOGS</a></li>
    <li class="nav-item"><a href="surveillance">SURVEILLANCE</a></li>
    <li class="nav-item"><a href="logout">LOG OUT</a></li>
  </ul>

  <div class="content">
    <div class="camera">
      <h1>Camera Feed</h1>
      <img id="camera-feed" src="/static/img/bean.gif" alt="">
    </div>
    <div class="floor-plan">
      <ul class="rooms">
        <h1>Room Camera Layout</h1>
        % for room in rooms:
          <ul class="room"><h2>{{room.name.title()}}</h2>
          %  for camera in room.cameras:
            <li class="sensor"><pre>Camera ID #{{camera.id}}</pre><button class={{str(camera.online).lower()}} >Online: {{str(camera.online).lower()}}</button><button class="feed" onclick="cameraFeed()">Show Feed</button></li>
          % end

          % if not room.cameras:
            <li>> No Cameras registered</li>
          % end
          </ul>
        % end
      </ul>
    </div>
  </div>

  <script>
    function cameraFeed() {
      let images = ["/static/img/camera1.gif", "/static/img/camera2.gif", "/static/img/camera3.gif", "/static/img/bean.gif"];
      let img = document.getElementById("camera-feed");
      img.src = images[Math.floor(Math.random() * images.length)];
      console.log(img.src);
    }
  </script>

</body>
</html>
