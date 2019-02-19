<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Security</title>
  <link rel="stylesheet" href="static/css/normalize.css">
  <link rel="stylesheet" href="static/css/core.css">
  <link rel="stylesheet" href="static/css/logs.css">
</head>
<body>

  <ul class="nav">
    <li class="nav-item"><a href="dashboard">DASHBOARD</a></li>
    <li class="nav-item"><a href="logs">LOGS</a></li>
    <li class="nav-item"><a href="surveillance">SURVEILLANCE</a></li>
    <li class="nav-item"><a href="logout">LOG OUT</a></li>
  </ul>

  <div class="content">
      <div class="logs">
        <ul class="log-list">
        % for log in logs:
          <li>{{ log.to_string() }}</li>
        % end
        </ul>
      </div>
  </div>
</body>
</html>
