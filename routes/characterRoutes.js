const express = require("express");
const Character = require("../models/Character");

const router = express.Router();

// Obtener todos los personajes
router.get("/", async (req, res) => {
  const characters = await Character.find();
  res.json(characters);
});

// Agregar un personaje
router.post("/", async (req, res) => {
  const newCharacter = new Character(req.body);
  await newCharacter.save();
  res.json({ message: "Personaje agregado!", character: newCharacter });
});

// Obtener un personaje por ID
router.get("/:id", async (req, res) => {
  const character = await Character.findById(req.params.id);
  res.json(character);
});

// Eliminar un personaje
router.delete("/:id", async (req, res) => {
  await Character.findByIdAndDelete(req.params.id);
  res.json({ message: "Personaje eliminado" });
});

module.exports = router;
