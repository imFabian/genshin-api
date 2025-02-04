require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware (debe ir antes de las rutas)
app.use(express.json());
app.use(cors());

// Conexión a MongoDB
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("Conectado a MongoDB"))
  .catch((err) => console.error("Error de conexión", err));

// Importar rutas
const characterRoutes = require("./routes/characterRoutes");
app.use("/api/characters", characterRoutes);

// Ruta de prueba
app.get("/", (req, res) => {
  res.send("Genshin Impact API funcionando!");
});

// Iniciar servidor
app.listen(PORT, () =>
  console.log(`Servidor escuchando en el puerto ${PORT}`)
);
