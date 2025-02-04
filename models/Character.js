const mongoose = require("mongoose");

const CharacterSchema = new mongoose.Schema({
  name: String,
  element: String,
  rarity: Number,
  weaponType: String,
  description: String,
});

module.exports = mongoose.model("Character", CharacterSchema);
