import type { Language } from '../Types';

export const languages: Language[] = [
  {
    id: 'python',
    name: 'Python',
    version: '3.11',
    extension: 'py',
    aceMode: 'python',
    monacoLanguage: 'python'
  },
  {
    id: 'javascript',
    name: 'JavaScript',
    version: 'Node.js 18',
    extension: 'js',
    aceMode: 'javascript',
    monacoLanguage: 'javascript'
  },
  {
    id: 'java',
    name: 'Java',
    version: '17',
    extension: 'java',
    aceMode: 'java',
    monacoLanguage: 'java'
  },
  {
    id: 'cpp',
    name: 'C++',
    version: 'GCC 11',
    extension: 'cpp',
    aceMode: 'c_cpp',
    monacoLanguage: 'cpp'
  },
  {
    id: 'c',
    name: 'C',
    version: 'GCC 11',
    extension: 'c',
    aceMode: 'c_cpp',
    monacoLanguage: 'c'
  },
  {
    id: 'sql',
    name: 'SQL',
    version: 'MySQL 8.0',
    extension: 'sql',
    aceMode: 'sql',
    monacoLanguage: 'sql'
  },
  {
    id: 'html',
    name: 'HTML',
    version: 'HTML5',
    extension: 'html',
    aceMode: 'html',
    monacoLanguage: 'html'
  },
  {
    id: 'css',
    name: 'CSS',
    version: 'CSS3',
    extension: 'css',
    aceMode: 'css',
    monacoLanguage: 'css'
  },
  {
    id: 'react',
    name: 'React',
    version: '18.2',
    extension: 'jsx',
    aceMode: 'jsx',
    monacoLanguage: 'javascript'
  }
];