require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

// Conexión a MongoDB
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("✅ Conectado a MongoDB"))
  .catch((err) => console.error("❌ Error de conexión a MongoDB:", err));

// Middleware
app.use(express.json());
app.use(cors());

// Modelos dinámicos para las colecciones
const collections = [
  "characters",
  "weapons",
  "artifacts",
  "materials",
  "enemies",
  "events",
  "banners",
];
const models = {};

collections.forEach((col) => {
  models[col] = mongoose.model(
    col,
    new mongoose.Schema({}, { strict: false }),
    col
  );
});

// Rutas dinámicas para cada colección
collections.forEach((col) => {
  app.get(`/api/${col}`, async (req, res) => {
    try {
      const data = await models[col].find();
      res.json({ success: true, count: data.length, data });
    } catch (err) {
      res
        .status(500)
        .json({ success: false, error: "Error al obtener datos de " + col });
    }
  });
});

// Ruta de prueba
app.get("/", (req, res) => {
  res.json({ success: true, message: "Genshin Impact API funcionando!" });
});

// Ruta para ver el uso de memoria del servidor
app.get("/api/memory", (req, res) => {
  const memoryUsage = process.memoryUsage();
  res.json({
    success: true,
    memory: {
      rss: `${(memoryUsage.rss / 1024 / 1024).toFixed(2)} MB`,
      heapTotal: `${(memoryUsage.heapTotal / 1024 / 1024).toFixed(2)} MB`,
      heapUsed: `${(memoryUsage.heapUsed / 1024 / 1024).toFixed(2)} MB`,
      external: `${(memoryUsage.external / 1024 / 1024).toFixed(2)} MB`,
    },
  });
});

// Iniciar servidor
app.listen(PORT, () =>
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`)
);
