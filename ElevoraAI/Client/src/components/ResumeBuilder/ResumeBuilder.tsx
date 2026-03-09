import React, { useState } from 'react';
import { useGlobalState } from '../../contexts/GlobalContext';
import { Download, Save, Edit, Eye } from 'lucide-react';
import PersonalInfoForm from './PersonalInfoForm';
import ExperienceForm from './ExperienceForm';
import EducationForm from './EducationForm';
import ProjectsForm from './ProjectsForm';
import SkillsForm from './SkillsForm';
import ResumePreview from './ResumePreview';
import ATSScanner from './ATSScannerNew';
import html2pdf from 'html2pdf.js';

const ResumeBuilder: React.FC = () => {
  const { state, dispatch } = useGlobalState();
  const [activeSection, setActiveSection] = useState('personal');
  const [showPreview, setShowPreview] = useState(false);
  const previewRef = React.useRef<HTMLDivElement>(null);
  const printRef = React.useRef<HTMLDivElement>(null);
  const [selectedSections] = useState({
    personal: true,
    experience: true,
    education: true,
    projects: true,
    skills: true,
  });

  const sections = [
    { id: 'personal', label: 'Personal Info', icon: Edit },
    { id: 'experience', label: 'Experience', icon: Edit },
    { id: 'education', label: 'Education', icon: Edit },
    { id: 'projects', label: 'Projects', icon: Edit },
    { id: 'skills', label: 'Skills', icon: Edit },
  ];

  const initializeResume = () => {
    if (!state.resume) {
      const defaultResume = {
        id: '1',
        personalInfo: {
          name: '',
          email: '',
          phone: '',
          location: '',
          linkedin: '',
          github: '',
        },
        summary: '',
        experience: [],
        education: [],
        projects: [],
        skills: {
          technical: [],
          soft: [],
        },
      };
      dispatch({ type: 'UPDATE_RESUME', payload: defaultResume });
    }
  };

  React.useEffect(() => {
    initializeResume();
  }, []);

  const renderActiveSection = () => {
    if (!state.resume) return null;
    switch (activeSection) {
      case 'personal':
        return <PersonalInfoForm />;
      case 'experience':
        return <ExperienceForm />;
      case 'education':
        return <EducationForm />;
      case 'projects':
        return <ProjectsForm />;
      case 'skills':
        return <SkillsForm />;
      default:
        return <PersonalInfoForm />;
    }
  };

  const downloadResume = async () => {
    if (!state.resume) {
      alert('No resume data found.');
      return;
    }

    if (!printRef.current) return;

    try {
      await document.fonts.ready;
      const element = printRef.current;
      element.classList.add("pdf-mode");

      const opt = {
        margin: [10, 0, 10, 0] as [number, number, number, number],
        filename: 'resume.pdf',
        image: { type: 'jpeg' as const, quality: 0.98 },
        html2canvas: { scale: 3, useCORS: true, letterRendering: true, backgroundColor: state.darkMode ? '#1f2937' : '#ffffff' },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' as const },
        enableLinks: true,
        pagebreak: { mode: ['css', 'legacy'] }
      };

      await html2pdf().set(opt).from(element).save();
      element.classList.remove("pdf-mode");
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Please try again.');
      if (printRef.current) {
        printRef.current.classList.remove("pdf-mode");
      }
    }
  };

  const saveResume = () => {
    alert('Resume saved successfully!');
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${state.darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className={`text-4xl font-extrabold tracking-tight ${state.darkMode ? 'text-white' : 'text-gray-900'} mb-3 transition-colors`}>
            Resume Builder
          </h1>
          <p className={`text-lg ${state.darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Create an ATS-friendly resume that gets you noticed
          </p>
        </div>

        {/* Action Buttons */}
        <div className="mb-10 flex flex-wrap gap-4">
          <button onClick={() => setShowPreview(!showPreview)} className="flex items-center space-x-2 px-4 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-xl shadow-sm transition-all">
            <Eye className="w-4 h-4" />
            <span>{showPreview ? 'Hide Preview' : 'Preview Resume'}</span>
          </button>
          <button onClick={saveResume} className="flex items-center space-x-2 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl shadow-sm transition-all">
            <Save className="w-4 h-4" />
            <span>Save Resume</span>
          </button>
          <button onClick={downloadResume} className="flex items-center space-x-2 px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-xl shadow-sm transition-all">
            <Download className="w-4 h-4" />
            <span>Download PDF</span>
          </button>
        </div>

        {showPreview ? (
          <div ref={previewRef}>
            <ResumePreview sections={selectedSections} />
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
              {/* Left Nav */}
              <div className="lg:col-span-1">
                <div className={`${state.darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl p-6 border shadow-sm`}>
                  <h3 className={`text-lg font-semibold mb-4 ${state.darkMode ? 'text-white' : 'text-gray-900'}`}>
                    Resume Sections
                  </h3>
                  <div className="space-y-2">
                    {sections.map(section => {
                      const Icon = section.icon;
                      return (
                        <button
                          key={section.id}
                          onClick={() => setActiveSection(section.id)}
                          className={`w-full p-3 rounded-lg border text-left transition-all ${activeSection === section.id
                            ? 'bg-blue-500 text-white border-blue-500'
                            : state.darkMode
                              ? 'border-gray-700 hover:border-gray-600 text-gray-300'
                              : 'border-gray-200 hover:border-gray-300 text-gray-900'
                            }`}
                        >
                          <div className="flex items-center space-x-3">
                            <Icon className="w-5 h-5" />
                            <span className="font-medium">{section.label}</span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Form Content */}
              <div className="lg:col-span-3">
                <div className={`${state.darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} rounded-xl p-6 border shadow-sm`}>
                  <div ref={previewRef}>{renderActiveSection()}</div>
                </div>
              </div>
            </div>

            {/* ATS Scanner UI */}
            <div className="mt-10">
              <ATSScanner />
            </div>
          </>
        )}
      </div>

      {/* Hidden container for PDF generation */}
      <div
        style={{
          position: 'absolute',
          top: '-10000px',
          left: '-10000px',
          width: '794px', // Standard A4 width in pixels at 96 DPI
          pageBreakAfter: 'auto'
        }}
      >
        <div className="pdf-container" ref={printRef} style={{ pageBreakAfter: 'auto' }}>
          <style>
            {`
              .pdf-mode svg {
                vertical-align: middle !important;
                transform: translateY(2px) !important;
              }
              .pdf-mode .contact-item {
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
              }
              .pdf-mode .skill-badge {
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                height: 24px !important;
                padding: 0 10px !important;
                border-radius: 6px !important;
                box-sizing: border-box !important;
              }
              .pdf-mode .skill-badge span {
                display: inline-block !important;
                position: relative !important;
                top: -1.5px !important;
                line-height: 1 !important;
              }
              .pdf-mode .skills-container {
                display: block !important;
              }
            `}
          </style>
          <ResumePreview sections={selectedSections} />
        </div>
      </div>
    </div>
  );
};

export default ResumeBuilder;
