const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

// 📌 Connect to MongoDB Atlas
mongoose
  .connect("mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/register_user")
  .then(() => console.log("✅ MongoDB Connected Successfully"))
  .catch((err) => console.error("❌ MongoDB Connection Error:", err));

// 📌 Define User Schema (Stores Password as Plain Text)
const userSchema = new mongoose.Schema({
  username: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true } // ⚠️ Plain text password (NOT SECURE)
});

const User = mongoose.model("User", userSchema);

// 📌 Registration Route (Stores Password as Plain Text)
// 📌 Registration Route (Fix: Remove `window.location.href`)
app.post("/register", async (req, res) => {
  try {
      const { username, email, password } = req.body;

      if (!username || !email || !password) {
          return res.status(400).json({ message: "All fields are required" });
      }

      const existingUser = await User.findOne({ email });
      if (existingUser) {
          return res.status(400).json({ message: "User already exists" });
      }

      const newUser = new User({ username, email, password });
      await newUser.save();

      res.status(201).json({ message: "User registered successfully", redirect: "home.html" });
  } catch (error) {
      console.error("❌ Error registering user:", error);
      res.status(500).json({ message: "Server error" });
  }
});


// 📌 Login Route (Compares Plain Text Password)
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;
    console.log("🔍 Login attempt for:", email);

    // ✅ Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      console.log("❌ User not found.");
      return res.status(400).json({ message: "✅ Login successful" });
      window.location.href = "home.html";
    }

    // ✅ Check plain text password (Direct comparison)
    if (password !== user.password) {
      console.log("❌ Incorrect password.");
      return res.status(400).json({ message: "✅ Login successful" });
      window.location.href = "home.html";
    }

    console.log("✅ Login successful.");
    res.status(200).json({ message: "Login successful" });
    window.location.href = "home.html";
  } catch (error) {
    console.error("❌ Error:", error);
    res.status(500).json({ message: "Server error" });
  }
});

// Start Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
