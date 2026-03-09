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
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

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
      const element = printRef.current;

      const canvas = await html2canvas(element, {
        scale: 2, // Higher resolution for better text clarity
        useCORS: true,
        logging: false,
        backgroundColor: state.darkMode ? '#1f2937' : '#ffffff', // Match ResumePreview background
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
      });

      const imgWidth = 210; // A4 width in mm
      const pageHeight = 297; // A4 height in mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save('resume.pdf');
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Please try again.');
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
          width: '794px' // Standard A4 width in pixels at 96 DPI
        }}
      >
        <div ref={printRef}>
          <ResumePreview sections={selectedSections} />
        </div>
      </div>
    </div>
  );
};

export default ResumeBuilder;
