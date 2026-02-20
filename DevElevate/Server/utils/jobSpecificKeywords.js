/**
 * Job-specific keywords for different roles
 * These are specialized keywords that are important for specific job titles
 */
const jobSpecificKeywords = {
  // Frontend Developer Keywords
  'frontend': [
    "react", "angular", "vue", "javascript", "typescript", "html", "css", "sass",
    "less", "bootstrap", "tailwind", "material-ui", "styled-components", "redux",
    "context api", "hooks", "responsive design", "web accessibility", "seo", "webpack",
    "babel", "vite", "parcel", "browser compatibility", "cross-browser", "dom",
    "event handling", "web performance", "animation", "svg", "canvas", "progressive enhancement"
  ],
  
  // Backend Developer Keywords
  'backend': [
    "node.js", "express", "nest.js", "python", "django", "flask", "java", "spring boot",
    "php", "laravel", "ruby", "rails", "go", "rust", "api design", "rest", "graphql",
    "websockets", "microservices", "authentication", "authorization", "oauth", "jwt",
    "database design", "sql", "postgresql", "mysql", "mongodb", "redis", "orm",
    "caching", "message queues", "rabbitmq", "kafka", "websocket"
  ],
  
  // Full Stack Developer Keywords
  'fullstack': [
    "javascript", "typescript", "react", "node.js", "express", "mongodb", "sql",
    "full-stack architecture", "frontend", "backend", "api integration", "deployment",
    "ci/cd", "devops", "testing", "user authentication", "responsive design",
    "performance optimization", "git", "github", "agile", "scrum"
  ],

  // Data Scientist Keywords
  'data scientist': [
    "python", "r", "sql", "machine learning", "deep learning", "neural networks",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "data visualization",
    "matplotlib", "seaborn", "tableau", "power bi", "statistical analysis",
    "hypothesis testing", "regression", "classification", "clustering", "nlp",
    "computer vision", "feature engineering", "data cleaning", "big data",
    "hadoop", "spark", "data mining", "a/b testing"
  ],
  
  // DevOps Engineer Keywords
  'devops': [
    "docker", "kubernetes", "jenkins", "github actions", "gitlab ci", "aws", "azure",
    "gcp", "terraform", "ansible", "chef", "puppet", "infrastructure as code",
    "ci/cd", "monitoring", "prometheus", "grafana", "elk stack", "logging",
    "security", "networking", "linux", "shell scripting", "automation",
    "performance tuning", "cloud architecture", "scalability", "reliability"
  ],
  
  // Mobile Developer Keywords
  'mobile': [
    "react native", "flutter", "swift", "kotlin", "java", "objective-c", "ios",
    "android", "mobile ui", "responsive design", "app store", "google play",
    "push notifications", "offline functionality", "mobile performance", "geolocation",
    "camera integration", "biometrics", "mobile security", "app optimization",
    "cross-platform development", "native apis", "mobile testing", "app lifecycle"
  ],
  
  // UX/UI Designer Keywords
  'designer': [
    "user experience", "user interface", "wireframing", "prototyping", "figma",
    "sketch", "adobe xd", "photoshop", "illustrator", "usability testing",
    "information architecture", "accessibility", "responsive design", "design systems",
    "visual design", "interaction design", "typography", "color theory", "user research",
    "user journeys", "personas", "a/b testing", "material design", "design thinking"
  ],
  
  // Product Manager Keywords
  'product': [
    "product strategy", "roadmapping", "user stories", "requirements gathering",
    "market research", "competitive analysis", "product lifecycle", "agile",
    "scrum", "sprint planning", "backlog prioritization", "stakeholder management",
    "analytics", "kpis", "metrics", "conversion optimization", "user feedback",
    "feature prioritization", "mvp", "product-market fit", "go-to-market strategy"
  ],
  
  // QA/Test Engineer Keywords
  'qa': [
    "test automation", "selenium", "cypress", "jest", "mocha", "manual testing",
    "test cases", "test plans", "regression testing", "functional testing",
    "integration testing", "performance testing", "load testing", "security testing",
    "api testing", "ui testing", "bug tracking", "jira", "continuous testing",
    "test-driven development", "behavior-driven development", "quality assurance"
  ]
};

export default jobSpecificKeywords;
