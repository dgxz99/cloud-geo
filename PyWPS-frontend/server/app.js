// server/app.js
const express = require("express");
const cors = require("cors");
const knowledgeGraphRoutes = require("./api/knowledgeGraph");

const app = express();
app.use(cors({
    origin: "http://localhost:8081",
    methods: ["GET", "POST", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization"],
    credentials: true,
}));

app.use(express.json());
app.use("/api", knowledgeGraphRoutes);

module.exports = app;
