require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors({ origin: "*", methods: ["GET", "POST"] }));
app.use(bodyParser.json());

// Connect to MongoDB
const mongoURI = "mongodb+srv://bogeprathmesh:secure12345@cluster0.iwmcgzx.mongodb.net/eventDB?retryWrites=true&w=majority&appName=Cluster0";
mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("✅ MongoDB Connected"))
    .catch(err => console.error("❌ MongoDB Connection Error:", err));

// Define Schema and Model (Fixed)
const FormDataSchema = new mongoose.Schema({
    name: String,
    email: String,
    mobile: String,
    experience: String
});

const FormData = mongoose.model("FormData", FormDataSchema);

// Handle form submission (Fixed)
app.post("/submit", async (req, res) => {
    try {
        const { name, email, mobile, experience } = req.body;
        const newEntry = new FormData({ name, email, mobile, experience });
        await newEntry.save();
        res.status(200).json({ message: "✅ Form submitted successfully!" });
    } catch (error) {
        console.error("Submission Error:", error);
        res.status(500).json({ message: "❌ Error submitting form", error });
    }
});

// Start server
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
