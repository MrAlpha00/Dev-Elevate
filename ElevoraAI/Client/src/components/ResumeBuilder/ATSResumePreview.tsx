import React from 'react';
import { useGlobalState } from '../../contexts/GlobalContext';

interface ResumePreviewProps {
    sections?: {
        personal: boolean;
        experience: boolean;
        education: boolean;
        projects: boolean;
        skills: boolean;
    };
}

const ATSResumePreview: React.FC<ResumePreviewProps> = ({ sections }) => {
    const { state } = useGlobalState();

    if (!state.resume) return null;

    // Default: if no sections prop, show all
    const show = sections || {
        personal: true,
        experience: true,
        education: true,
        projects: true,
        skills: true,
    };

    return (
        <div className="max-w-4xl mx-auto bg-white text-black p-8 font-sans">
            {/* Header */}
            {show.personal && (
                <div className="border-b-2 border-black pb-4 mb-6">
                    <h1 className="text-3xl font-bold mb-2 uppercase tracking-wide">
                        {state.resume.personalInfo.name || 'Your Name'}
                    </h1>
                    <div className="text-sm space-y-1">
                        <div className="flex flex-wrap gap-2 text-gray-800">
                            {state.resume.personalInfo.email && (
                                <span>{state.resume.personalInfo.email}</span>
                            )}
                            {state.resume.personalInfo.email && state.resume.personalInfo.phone && <span>|</span>}
                            {state.resume.personalInfo.phone && (
                                <span>{state.resume.personalInfo.phone}</span>
                            )}
                            {(state.resume.personalInfo.email || state.resume.personalInfo.phone) && state.resume.personalInfo.location && <span>|</span>}
                            {state.resume.personalInfo.location && (
                                <span>{state.resume.personalInfo.location}</span>
                            )}
                        </div>
                        <div className="flex flex-wrap gap-2 text-gray-800">
                            {state.resume.personalInfo.linkedin && (
                                <a href={state.resume.personalInfo.linkedin} className="text-blue-600 hover:underline">
                                    LinkedIn
                                </a>
                            )}
                            {state.resume.personalInfo.linkedin && state.resume.personalInfo.github && <span>|</span>}
                            {state.resume.personalInfo.github && (
                                <a href={state.resume.personalInfo.github} className="text-blue-600 hover:underline">
                                    GitHub
                                </a>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Professional Summary */}
            {show.personal && state.resume.summary && (
                <div className="mb-6 break-words whitespace-pre-wrap">
                    <h2 className="text-lg font-bold uppercase border-b border-gray-300 pb-1 mb-3">Professional Summary</h2>
                    <p className="text-sm leading-relaxed text-black">{state.resume.summary}</p>
                </div>
            )}

            {/* Experience */}
            {show.experience && state.resume.experience.length > 0 && (
                <div className="mb-6">
                    <h2 className="text-lg font-bold uppercase border-b border-gray-300 pb-1 mb-3">Experience</h2>
                    {state.resume.experience.map((exp, index) => (
                        <div key={index} className="mb-4" style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}>
                            <div className="flex justify-between items-start mb-1">
                                <h3 className="font-bold text-black">{exp.position}</h3>
                                <span className="text-sm text-black">{exp.duration}</span>
                            </div>
                            <p className="text-sm italic text-gray-800 mb-2">{exp.company}</p>
                            <ul className="list-disc list-outside ml-5 text-sm space-y-1 text-black">
                                {exp.description.map((desc, descIndex) => (
                                    <li key={descIndex} className="pl-1">{desc}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            )}

            {/* Education */}
            {show.education && state.resume.education.length > 0 && (
                <div className="mb-6">
                    <h2 className="text-lg font-bold uppercase border-b border-gray-300 pb-1 mb-3">Education</h2>
                    {state.resume.education.map((edu, index) => (
                        <div key={index} className="mb-3" style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}>
                            <div className="flex justify-between items-start mb-1">
                                <h3 className="font-bold text-black">{edu.degree}</h3>
                                <span className="text-sm text-black">{edu.duration}</span>
                            </div>
                            <p className="text-sm text-black">
                                {edu.institution}
                                {edu.gpa && ` • GPA: ${edu.gpa}`}
                            </p>
                        </div>
                    ))}
                </div>
            )}

            {/* Projects */}
            {show.projects && state.resume.projects.length > 0 && (
                <div className="mb-6">
                    <h2 className="text-lg font-bold uppercase border-b border-gray-300 pb-1 mb-3">Projects</h2>
                    {state.resume.projects.map((project, index) => (
                        <div key={index} className="mb-4" style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}>
                            <div className="flex justify-between items-center mb-1">
                                <h3 className="font-bold text-black">{project.name}</h3>
                                {project.url && (
                                    <a
                                        href={project.url}
                                        className="text-blue-600 hover:underline text-sm"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        View Project
                                    </a>
                                )}
                            </div>
                            <p className="text-sm mb-1 text-black">{project.description}</p>
                            {project.technologies.length > 0 && (
                                <p className="text-xs text-gray-700">
                                    <span className="font-semibold text-black">Technologies:</span> {project.technologies.join(', ')}
                                </p>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {/* Skills */}
            {show.skills && (state.resume.skills.technical.length > 0 || state.resume.skills.soft.length > 0) && (
                <div className="mb-6">
                    <h2 className="text-lg font-bold uppercase border-b border-gray-300 pb-1 mb-3">Skills</h2>

                    {state.resume.skills.technical.length > 0 && (
                        <div className="mb-2 text-sm text-black">
                            <span className="font-bold mr-2">Technical Skills:</span>
                            <span>{state.resume.skills.technical.join(', ')}</span>
                        </div>
                    )}

                    {state.resume.skills.soft.length > 0 && (
                        <div className="text-sm text-black">
                            <span className="font-bold mr-2">Soft Skills:</span>
                            <span>{state.resume.skills.soft.join(', ')}</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ATSResumePreview;
