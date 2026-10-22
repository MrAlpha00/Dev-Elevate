import axios from "axios";
import dotenv from "dotenv";
import Quiz from "../model/Quiz.js";
import QuizAttempt from "../model/QuizAttempt.js";
dotenv.config();

// Existing getAIReply function...
export const getAIReply = async (req, res) => {
  const { message, category } = req.body;
  if (!message) return res.status(400).json({ error: "No input provided" });
  try {
    let prompt = message;
    if (category && category.toLowerCase() === "quiz") {
      prompt = `You are Study Buddy, an AI mentor specializing in DSA quizzes.\nGenerate 6 deep-level MCQ (multiple choice questions) based on the topic: \"${message}\".\nMake sure the questions test strong understanding, not just definitions.\nEach question should have 4 options and clearly mark the correct answer.\nFormat:\n1. Question text\nA) Option A\nB) Option B\nC) Option C\nD) Option D\n✅ Correct Answer: X\nOnly provide the quiz — no explanation or extra text.`;
    }
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/${process.env.GEMINI_MODEL || "gemini-3.5-flash-lite"}:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        contents: [
          {
            role: "user",
            parts: [{ text: prompt }],
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const aiText =
      response.data?.candidates?.[0]?.content?.parts?.[0]?.text ||
      "No reply received";
    console.log("[Gemini Response]", { aiText });
    res.status(200).json({ reply: aiText });
  } catch (error) {
    let status = error.response?.status;
    let errorMsg = error.response?.data || error.message;
    console.error("Gemini API error:", errorMsg);
    if (status === 429) {
      return res.status(429).json({
        error: "Gemini API rate limit exceeded. Please try again later.",
      });
    }
    res.status(500).json({ error: "AI service is unavailable" });
  }
};

// NEW FUNCTION: Generate AI Quiz
export const generateAIQuiz = async (req, res) => {
  try {
    const { topic, difficulty, type, questionCount } = req.body;
    const userId = req.user.id;

    if (!topic || !difficulty || !type || !questionCount) {
      return res.status(400).json({ 
        message: "Missing required fields: topic, difficulty, type, questionCount" 
      });
    }

    // Build prompt based on quiz type
    let prompt = "";
    
    if (type === "MCQ") {
      prompt = `Generate ${questionCount} multiple choice questions about "${topic}" at ${difficulty} difficulty level.

IMPORTANT: Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, no extra text):
{
  "questions": [
    {
      "questionText": "Question here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctAnswer": "Option A"
    }
  ]
}

Requirements:
- Generate exactly ${questionCount} questions
- Each question must have exactly 4 options
- Questions should be challenging and test deep understanding
- correctAnswer must be one of the options exactly as written
- Return ONLY the JSON object, nothing else`;
    } else if (type === "Code") {
      prompt = `Generate ${questionCount} coding problems about "${topic}" at ${difficulty} difficulty level.

IMPORTANT: Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks, no extra text):
{
  "questions": [
    {
      "questionText": "Problem statement with requirements",
      "expectedOutput": "Expected output or solution approach"
    }
  ]
}

Requirements:
- Generate exactly ${questionCount} coding problems
- Each problem should include clear input/output requirements
- Problems should be at ${difficulty} level
- Include expectedOutput for validation
- Return ONLY the JSON object, nothing else`;
    }

    // Call Gemini API
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/${process.env.GEMINI_MODEL || "gemini-3.5-flash-lite"}:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        contents: [
          {
            role: "user",
            parts: [{ text: prompt }],
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const aiText = response.data?.candidates?.[0]?.content?.parts?.[0]?.text;
    
    if (!aiText) {
      return res.status(500).json({ message: "Failed to generate quiz content" });
    }

    // Parse the AI response
    let parsedQuestions;
    try {
      // Remove markdown code blocks if present
      const cleanedText = aiText
        .replace(/```json\n?/g, '')
        .replace(/```\n?/g, '')
        .trim();
      
      parsedQuestions = JSON.parse(cleanedText);
    } catch (parseError) {
      console.error("Error parsing AI response:", parseError);
      console.log("AI Response:", aiText);
      return res.status(500).json({ 
        message: "Failed to parse AI generated questions",
        debug: aiText 
      });
    }

    // Validate and format questions
    const questions = parsedQuestions.questions.map(q => {
      if (type === "MCQ") {
        return {
          questionText: q.questionText,
          options: q.options,
          correctAnswer: q.correctAnswer
        };
      } else {
        return {
          questionText: q.questionText,
          expectedOutput: q.expectedOutput
        };
      }
    });

    // Create quiz in database
    const quiz = new Quiz({
      title: `${topic} - ${difficulty} (AI Generated)`,
      topic,
      difficulty,
      type,
      questions,
      createdBy: userId,
      isAIGenerated: true
    });

    await quiz.save();

    // Automatically create an attempt entry so it shows in user's AI generated section
    const quizAttempt = new QuizAttempt({
      userId,
      quizId: quiz._id,
      answers: [], // Empty initially
      score: 0,
      totalQuestions: questions.length,
      timeTaken: 0,
      isGenerated: true, // Flag to show it's just generated, not actually attempted
      createdAt: new Date()
    });

    await quizAttempt.save();

    res.status(201).json({ 
      message: "AI Quiz generated successfully", 
      quiz: {
        _id: quiz._id,
        title: quiz.title,
        topic: quiz.topic,
        difficulty: quiz.difficulty,
        type: quiz.type,
        questionCount: questions.length,
        isAIGenerated: true
      }
    });

  } catch (error) {
    console.error("Error generating AI quiz:", error);
    
    if (error.response?.status === 429) {
      return res.status(429).json({
        message: "AI service rate limit exceeded. Please try again later.",
      });
    }
    
    res.status(500).json({ 
      message: "Failed to generate AI quiz",
      error: error.message 
    });
  }
};

// Add this to your existing aiController.js file

// NEW FUNCTION: Generate AI Notes
export const generateAINote = async (req, res) => {
  try {
    const { prompt } = req.body;
    const userId = req.user?.id || req.user?._id;

    if (!userId) {
      return res.status(401).json({
        success: false,
        message: "Authentication required",
      });
    }

    if (!prompt || !prompt.trim()) {
      return res.status(400).json({
        success: false,
        message: "Prompt is required",
      });
    }

    console.log("Generating AI note for prompt:", prompt);

    // Build comprehensive prompt for note generation
    const fullPrompt = `You are an expert educational content creator and study guide writer. Generate comprehensive, well-structured study notes on the following topic. 

Topic: ${prompt}

Requirements:
1. Use clear Markdown formatting with proper headings (# ## ###)
2. Include an introduction/overview section
3. Break down key concepts with explanations
4. Add relevant examples where applicable
5. Use bullet points and numbered lists for clarity
6. Include code examples if the topic is technical (use proper code blocks with language specification)
7. Add a summary section at the end
8. Make the content educational, detailed, and easy to understand
9. Aim for comprehensive coverage - not too brief

Format the entire response in clean Markdown. Make it suitable for students to study from.`;

    // Call Gemini API
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/${process.env.GEMINI_MODEL || "gemini-3.5-flash-lite"}:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        contents: [
          {
            role: "user",
            parts: [{ text: fullPrompt }],
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const generatedContent = response.data?.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!generatedContent) {
      return res.status(500).json({
        success: false,
        message: "Failed to generate note content",
      });
    }

    // Generate title from prompt (capitalize first letter of each word)
    const title = prompt
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');

    const finalTitle = title.length > 60 
      ? title.substring(0, 60) + "..." 
      : title;

    // Extract potential tags from prompt
    const commonWords = [
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
      'for', 'of', 'with', 'by', 'from', 'about', 'how', 'what', 'why',
      'explain', 'describe', 'create', 'make', 'write', 'notes'
    ];
    
    const words = prompt
      .toLowerCase()
      .replace(/[^\w\s]/g, '') // Remove punctuation
      .split(/\s+/)
      .filter(word => word.length > 3 && !commonWords.includes(word))
      .slice(0, 5);

    // Add "AI" tag
    const tags = ['AI-Generated', ...words];

    console.log("✅ AI note generated successfully");

    return res.status(200).json({
      success: true,
      content: generatedContent,
      title: finalTitle,
      tags: tags,
      message: "Note generated successfully",
    });

  } catch (error) {
    console.error("❌ AI note generation error:", error);
    
    if (error.response?.status === 429) {
      return res.status(429).json({
        success: false,
        message: "AI service rate limit exceeded. Please try again later.",
      });
    }

    return res.status(500).json({
      success: false,
      message: "Failed to generate note",
      error: error.message,
    });
  }
};

// NEW FUNCTION: Generate AI Project Recommendations
export const generateProjectRecommendations = async (req, res) => {
  const apiKey = process.env.GEMINI_API_KEY?.trim();
  if (!apiKey) {
    return res.status(500).json({
      success: false,
      message: "Gemini API key is not configured. Set GEMINI_API_KEY in the environment.",
    });
  }

  try {
    const { preferences, excludeTitles = [] } = req.body || {};

    const techStack =
      Array.isArray(preferences?.techStack) && preferences.techStack.length > 0
        ? preferences.techStack.join(", ")
        : "Full-Stack Web Development";
    const careerFocus = preferences?.careerFocus?.trim() || "Full Stack Development";
    const skillLevel = ["Beginner", "Intermediate", "Advanced"].includes(preferences?.skillLevel)
      ? preferences.skillLevel
      : "Intermediate";
    const interestAreas =
      Array.isArray(preferences?.interestArea) && preferences.interestArea.length > 0
        ? preferences.interestArea.join(", ")
        : "Productivity, Web Applications";

    let excludeClause = "";
    if (Array.isArray(excludeTitles) && excludeTitles.length > 0) {
      const sanitizedExcludes = excludeTitles
        .filter((t) => typeof t === "string" && t.trim())
        .map((t) => t.trim())
        .slice(0, 15);
      if (sanitizedExcludes.length > 0) {
        excludeClause = `\nDO NOT suggest any of these existing or saved projects (provide completely fresh ideas):\n- ${sanitizedExcludes.join("\n- ")}\n`;
      }
    }

    const prompt = `You are a senior tech mentor and software architect. Generate 3 to 4 distinct, highly practical, and portfolio-worthy project ideas personalized for this developer.

Developer Profile:
- Target Career Focus: ${careerFocus}
- Current Skill Level: ${skillLevel}
- Known / Preferred Technologies: ${techStack}
- Domain Interest Areas: ${interestAreas}
${excludeClause}

Requirements for each project:
1. Title: Creative, unique, realistic project name.
2. Description: 2-3 engaging sentences explaining what problem it solves and what makes it impressive.
3. Difficulty: Must be exactly "${skillLevel}" or appropriate for this level.
4. Estimated Time: Realistic duration like "2-3 weeks" or "3-4 weeks".
5. Tech Stack: Array of 3 to 6 modern tools/libraries relevant to user's preferences.
6. Key Features: Array of 4 to 6 concrete, implementable feature bullet points.
7. Tags: Array of 3 to 5 hashtag strings (e.g. ["#fullstack", "#react", "#automation"]).
8. Starter Tutorials: Array of 2 relevant learning topics/tutorials.
9. GitHub Boilerplates: Array of 1-2 recommended boilerplate/starter search hints or repos.

IMPORTANT: Return ONLY a valid JSON array of objects with this exact structure (no markdown, no backticks, no extra text):
[
  {
    "title": "Project Title",
    "description": "2-3 sentence description.",
    "difficulty": "${skillLevel}",
    "estimatedTime": "2-3 weeks",
    "techStack": ["React", "Node.js", "MongoDB"],
    "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
    "tags": ["#tag1", "#tag2", "#tag3"],
    "starterTutorials": ["Tutorial Topic 1", "Tutorial Topic 2"],
    "githubBoilerplates": ["https://github.com/example/starter-repo"]
  }
]`;

    const model = process.env.GEMINI_MODEL || "gemini-3.5-flash-lite";
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
      {
        contents: [
          {
            role: "user",
            parts: [{ text: prompt }],
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const aiText = response.data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!aiText) {
      return res.status(502).json({
        success: false,
        message: "AI did not return any project recommendations. Please try again.",
      });
    }

    let cleanedText = aiText.trim();
    cleanedText = cleanedText
      .replace(/^```(?:json)?\s*/i, "")
      .replace(/\s*```$/, "")
      .trim();

    const jsonMatch = cleanedText.match(/\[[\s\S]*\]/);
    if (jsonMatch) {
      cleanedText = jsonMatch[0];
    }

    let parsedProjects;
    try {
      parsedProjects = JSON.parse(cleanedText);
    } catch (parseErr) {
      console.error("Failed to parse Gemini project recommendations JSON:", parseErr.message);
      return res.status(502).json({
        success: false,
        message: "Failed to parse AI project recommendations. Please try again.",
      });
    }

    if (!Array.isArray(parsedProjects) || parsedProjects.length === 0) {
      return res.status(502).json({
        success: false,
        message: "Invalid AI response structure for project recommendations.",
      });
    }

    const validatedProjects = parsedProjects.map((p, idx) => ({
      id: `ai-proj-${Date.now()}-${idx}-${Math.random().toString(36).substring(2, 7)}`,
      title: String(p.title || `Project Idea ${idx + 1}`).trim(),
      description: String(p.description || "A personalized development project.").trim(),
      difficulty: ["Beginner", "Intermediate", "Advanced"].includes(p.difficulty)
        ? p.difficulty
        : skillLevel,
      estimatedTime: String(p.estimatedTime || "2-3 weeks").trim(),
      techStack:
        Array.isArray(p.techStack) && p.techStack.length > 0
          ? p.techStack.map(String)
          : ["JavaScript", "React"],
      features:
        Array.isArray(p.features) && p.features.length > 0
          ? p.features.map(String)
          : ["Core application logic", "Responsive UI", "Data persistence"],
      tags:
        Array.isArray(p.tags) && p.tags.length > 0
          ? p.tags.map((t) => (String(t).startsWith("#") ? String(t) : `#${String(t)}`))
          : ["#project", "#portfolio"],
      starterTutorials: Array.isArray(p.starterTutorials) ? p.starterTutorials.map(String) : [],
      githubBoilerplates: Array.isArray(p.githubBoilerplates) ? p.githubBoilerplates.map(String) : [],
    }));

    return res.status(200).json({
      success: true,
      projects: validatedProjects,
    });
  } catch (error) {
    const status = error.response?.status;
    const rawErrorMsg = error.response?.data?.error?.message || error.message;
    const safeMsg = String(rawErrorMsg).replace(/key=[^&\s]+/gi, "key=[REDACTED]");
    console.error("Project recommendations generation error:", safeMsg);

    if (status === 429) {
      return res.status(429).json({
        success: false,
        message: "AI rate limit exceeded. Please wait a moment and try again.",
      });
    }

    return res.status(status && status >= 400 && status < 600 ? status : 500).json({
      success: false,
      message: "Failed to generate project recommendations. Please try again later.",
    });
  }
};