/**
 * Utility function to extract keywords from resume text
 * Provides enhanced extraction of both single words and multi-word phrases
 * 
 * @param {string} text - The text content of the resume
 * @returns {Object} - Object containing extracted words, phrases and sections
 */
function extractKeywords(text) {
  if (!text) return { words: [], phrases: [], sections: {} };
  
  // Extract single words
  const words = text.toLowerCase().match(/\b(\w+)\b/g);
  const uniqueWords = words ? [...new Set(words)] : [];
  
  // Extract multi-word phrases (like "machine learning" or "rest api")
  const phraseRegex = /\b(cloud computing|machine learning|deep learning|artificial intelligence|data science|big data|rest api|user experience|user interface|responsive design|web development|mobile development|full stack|front end|back end|devops|continuous integration|continuous deployment|test driven development|agile methodology|version control|source control)\b/gi;
  const phrases = [];
  let match;
  while ((match = phraseRegex.exec(text.toLowerCase())) !== null) {
    phrases.push(match[0]);
  }
  
  // Try to identify sections in the resume
  const sections = {
    summary: extractSection(text, 'summary', ['summary', 'profile', 'objective', 'about']),
    skills: extractSection(text, 'skills', ['skills', 'technical skills', 'core competencies', 'technologies']),
    experience: extractSection(text, 'experience', ['experience', 'work experience', 'employment history', 'work history']),
    education: extractSection(text, 'education', ['education', 'academic background', 'qualifications']),
    projects: extractSection(text, 'projects', ['projects', 'portfolio', 'personal projects']),
    certificates: extractSection(text, 'certificates', ['certificates', 'certifications', 'licenses']),
  };
  
  return { 
    words: uniqueWords, 
    phrases: phrases,
    sections: sections
  };
}

/**
 * Helper function to extract a specific section from resume text
 */
function extractSection(text, sectionName, sectionHeaders) {
  const lowerText = text.toLowerCase();
  
  // Check if any of the section headers exist in the text
  const foundHeader = sectionHeaders.find(header => lowerText.includes(header));
  
  if (!foundHeader) {
    return { found: false, content: null };
  }
  
  // Try to extract the section content (simplified approach)
  const headerIndex = lowerText.indexOf(foundHeader);
  if (headerIndex === -1) return { found: false, content: null };
  
  // Find the start of the section (after the header)
  const startIndex = headerIndex + foundHeader.length;
  
  // Get the next 500 characters as a rough estimation of the section
  // In a real implementation, this would be more sophisticated
  const sectionContent = text.substring(startIndex, startIndex + 500);
  
  return {
    found: true,
    content: sectionContent
  };
}

export default extractKeywords;
