import express from "express";
import axios from "axios";

const router = express.Router();

router.post("/", async (req, res) => {
  const apiKey = process.env.ONLINECOMPILER_API_KEY?.trim();
  if (!apiKey) {
    return res.status(500).json({
      error: "Compiler service is not configured. Set ONLINECOMPILER_API_KEY in the environment.",
    });
  }

  let { source_code, language_id, stdin, is_base64 } = req.body;
  if (is_base64 && typeof source_code === "string") {
    source_code = Buffer.from(source_code, "base64").toString("utf-8");
  }

  try {
    const submission = await axios.post(
      "https://api.onlinecompiler.io/api/judge0/submissions?base64_encoded=false&wait=true",
      {
        source_code,
        language_id,
        stdin,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "X-Auth-Token": apiKey,
        },
      }
    );
    const result = submission.data;
    return res.json(result);
  } catch (error) {
    const status = error.response?.status || 500;
    const errorDetail =
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      "Execution failed";

    console.error("Compiler API error:", {
      status,
      message:
        typeof errorDetail === "string"
          ? errorDetail.replace(/token=[^&\s]+|bearer\s+\S+/gi, "[REDACTED]")
          : "Compiler execution failed",
    });

    if (error.response?.data) {
      if (typeof error.response.data === "object") {
        return res.status(status).json(error.response.data);
      }
      return res.status(status).json({ error: String(error.response.data) });
    }

    return res
      .status(status)
      .json({ error: "Compiler service is currently unavailable. Please try again." });
  }
});

export default router;
