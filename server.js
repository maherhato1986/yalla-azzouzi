import express from "express";
import fetch from "node-fetch";
import fs from "fs";

const app = express();
const API_KEY = process.env.API_FOOTBALL_KEY;

app.get("/api/matches/today", async (req, res) => {
  const today = new Date().toISOString().split("T")[0];

  const r = await fetch(
    `https://v3.football.api-sports.io/fixtures?date=${today}`,
    {
      headers: {
        "x-apisports-key": API_KEY
      }
    }
  );

  const data = await r.json();

  const matches = data.response.map(m => ({
    id: m.fixture.id,
    league: m.league.name,
    home: m.teams.home.name,
    away: m.teams.away.name,
    time: m.fixture.date,
    streams: [] // روابط البث تُضاف لاحقًا
  }));

  res.json(matches);
});

app.listen(3000, () => console.log("API running on :3000"));
