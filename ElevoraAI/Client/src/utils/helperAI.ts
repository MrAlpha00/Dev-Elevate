// src/utils/gemini.ts

export const generateGeminiResponse = async (
  message: string,
  selectedCategory: string
): Promise<string> => {
  try {
    const prompt =
      selectedCategory.toLowerCase() === "quiz"
        ? `
You are Study Buddy, an AI mentor specializing in DSA quizzes.

Generate **6 deep-level MCQ (multiple choice questions)** based on the topic: "${message}".  
Make sure the questions test strong understanding, not just definitions.  
Each question should have 4 options and clearly mark the **correct answer**.

Format:
1. Question text  
   A) Option A  
   B) Option B  
   C) Option C  
   D) Option D  
   ✅ Correct Answer: X

Only provide the quiz — no explanation or extra text.
        `
        : `
You are Study Buddy, an AI mentor who gives concise, clear, and structured answers for ${selectedCategory} questions.

Respond using Markdown with the following format:

## 📌 Summary  
Brief 1-line summary of the concept.

## Key Concepts
- Important point 1
- Important point 2

## 💡 Example

\`\`\`ts
// Relevant code or example here
\`\`\`

## ✅ Conclusion  
Wrap up with a useful tip or reminder.

User: ${message}
`;

    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${
        import.meta.env.VITE_GEMINI_API_KEY
      }`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          contents: [
            {
              role: "user",
              parts: [{ text: prompt }],
            },
          ],
        }),
      }
    );

    const data = await res.json();

    const responseText =
      data.candidates?.[0]?.content?.parts?.[0]?.text || "No response";

    return responseText;
  } catch (error) {
    console.error("Error fetching Gemini response:", error);
    return "Something went wrong. Please try again.";
  }
};

// Utility functions for the new features
export const formatDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

export const getPriorityColor = (priority: string): string => {
  switch (priority) {
    case 'urgent':
      return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300';
    case 'high':
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-300';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300';
    case 'low':
      return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300';
  }
};

export const getStatusColor = (status: string): string => {
  switch (status) {
    case 'todo':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300';
    case 'in-progress':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300';
    case 'done':
      return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-300';
  }
};
