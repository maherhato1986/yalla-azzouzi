const express = require('express');
const request = require('request');
const app = express();

app.get('/stream', (req, res) => {
  const targetUrl = 'https://s1.streaming-on.online/b-1/';

  req.pipe(
    request({
      url: targetUrl,
      headers: {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://yalla-azzouzi.live'
      }
    })
  ).pipe(res);
});

app.listen(3000, () => {
  console.log('Proxy running on port 3000');
});
