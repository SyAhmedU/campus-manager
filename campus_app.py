import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Campus Command Center", page_icon="🏫", layout="wide")

# --- HIDE STREAMLIT UI ---
# This hides the default Streamlit menus so your React app looks native
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }
        iframe {
            height: 100vh !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- THE REACT APPLICATION ---
# This is your exact HTML/React code, wrapped for Python
react_app = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Director Command Center + Gemini AI</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        /* Custom Scrollbar for cleaner look */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        
        .animate-fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Loading Spinner */
        .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #6366f1; border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="bg-slate-100 text-slate-900 font-sans">
    <div id="root"></div>

    <script type="text/babel">
        // --- Self-Contained Icons ---
        const Icons = {
            LayoutDashboard: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>,
            CheckSquare: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>,
            Building2: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>,
            BarChart3: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>,
            Users: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
            Bell: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>,
            Search: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>,
            Plus: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>,
            Trash2: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>,
            AlertCircle: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>,
            FileText: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>,
            ChevronRight: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>,
            Menu: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>,
            X: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>,
            Download: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>,
            Shield: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>,
            Wrench: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>,
            Briefcase: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>,
            Settings: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.09a2 2 0 0 1-1-1.74v-.47a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>,
            Sparkles: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
        };

        const { useState, useEffect, useMemo } = React;

        // --- GEMINI API UTILS ---
        
        async function callGemini(prompt, apiKey) {
            if (!apiKey) throw new Error("API Key Missing");
            
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt }] }]
                })
            });
            
            if (!response.ok) throw new Error("API Call Failed");
            const data = await response.json();
            return data.candidates[0].content.parts[0].text;
        }

        // --- Data Generators & State Management ---
        
        const generateInitialTasks = () => [
            { id: 't1', title: 'Review Q2 Lab Safety Protocols', category: 'Compliance', status: 'todo', priority: 'high', assignee: 'Dr. Smith' },
            { id: 't2', title: 'Coordinate Guest Lecture: Dr. Al-Fayed', category: 'Events', status: 'in-progress', priority: 'medium', assignee: 'Admin Team' },
            { id: 't4', title: 'Update HVAC Maintenance Schedule', category: 'Facilities', status: 'done', priority: 'low', assignee: 'Maint. Dept' },
            { id: 't6', title: 'Inspect Fire Safety Equipment', category: 'Compliance', status: 'review', priority: 'high', assignee: 'Safety Officer' },
            { id: 't7', title: 'Approve Weekend Cleaning Roster', category: 'Facilities', status: 'todo', priority: 'medium', assignee: 'Self' },
        ];

        const generateInitialFacilities = () => [
            { id: 'f1', name: 'Lecture Hall A', capacity: 150, status: 'Occupied', nextFree: '14:00' },
            { id: 'f2', name: 'Behav. Science Lab', capacity: 20, status: 'Available', nextFree: 'Now' },
            { id: 'f3', name: 'Conference Room B', capacity: 12, status: 'Maintenance', nextFree: 'Tomorrow' },
            { id: 'f4', name: 'Student Lounge', capacity: 50, status: 'Available', nextFree: 'Now' },
            { id: 'f5', name: 'Admin Block', capacity: 40, status: 'Occupied', nextFree: '16:00' },
        ];

        const generateInitialStaff = () => [
            { id: 's1', name: 'James Wilson', role: 'Head of Security', department: 'Security', status: 'On Duty', contact: '555-0101' },
            { id: 's2', name: 'Sarah Chen', role: 'Facilities Manager', department: 'Maintenance', status: 'On Duty', contact: '555-0102' },
            { id: 's3', name: 'Mike Ross', role: 'Janitorial Lead', department: 'Cleaning', status: 'Break', contact: '555-0103' },
            { id: 's4', name: 'Elena Rodriguez', role: 'Admin Coordinator', department: 'Admin', status: 'Off Duty', contact: '555-0104' },
        ];

        // --- UI Components ---
        
        const SidebarItem = ({ icon: Icon, label, active, onClick }) => (
            <button
                onClick={onClick}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${
                active 
                    ? 'bg-blue-600 text-white shadow-md' 
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }`}
            >
                <Icon size={20} />
                <span className="font-medium">{label}</span>
            </button>
        );

        const StatCard = ({ title, value, change, icon: Icon, trend }) => (
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-between h-32">
                <div className="flex justify-between items-start">
                    <div>
                        <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{title}</p>
                        <h3 className="text-2xl font-bold text-slate-800 mt-1">{value}</h3>
                    </div>
                    <div className={`p-2 rounded-lg ${trend === 'up' ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'}`}>
                        <Icon size={20} />
                    </div>
                </div>
                <div className="flex items-center text-sm">
                    <span className={change.startsWith('+') ? 'text-green-600 font-semibold' : 'text-red-500 font-semibold'}>
                        {change}
                    </span>
                    <span className="text-slate-400 ml-2">vs last month</span>
                </div>
            </div>
        );

        const SimpleBarChart = ({ data, color = 'bg-blue-500' }) => {
            const max = Math.max(...data.map(d => d.value)) || 10;
            return (
                <div className="flex items-end justify-between h-48 space-x-2 pt-4">
                {data.map((d, i) => (
                    <div key={i} className="flex flex-col items-center flex-1 group cursor-pointer">
                    <div className="relative w-full flex justify-center">
                        <div className="absolute bottom-0 text-xs text-white bg-slate-800 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity mb-2 z-10 w-max pointer-events-none">
                            {d.value}
                        </div>
                        <div 
                            className={`w-full max-w-[40px] rounded-t-sm transition-all duration-500 ${color} opacity-80 group-hover:opacity-100`}
                            style={{ height: `${(d.value / max) * 160}px` }}
                        ></div>
                    </div>
                    <span className="text-xs text-slate-500 mt-2 font-medium">{d.label}</span>
                    </div>
                ))}
                </div>
            );
        };

        const KanbanColumn = ({ title, status, tasks, onMoveTask, onDeleteTask }) => {
            return (
                <div className="flex-1 min-w-[280px] bg-slate-50 rounded-xl p-4 flex flex-col h-full border border-slate-200">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-slate-700">{title}</h3>
                        <span className="bg-slate-200 text-slate-600 text-xs px-2 py-1 rounded-full">{tasks.length}</span>
                    </div>
                    <div className="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
                        {tasks.map(task => (
                        <div key={task.id} className="bg-white p-4 rounded-lg shadow-sm border border-slate-100 cursor-move hover:shadow-md transition-shadow group relative">
                            <div className="flex justify-between items-start mb-2">
                                <span className={`text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wide ${
                                    task.priority === 'high' ? 'bg-red-100 text-red-600' : 
                                    task.priority === 'medium' ? 'bg-orange-100 text-orange-600' : 'bg-green-100 text-green-600'
                                }`}>
                                    {task.priority}
                                </span>
                                <button 
                                    onClick={(e) => { e.stopPropagation(); onDeleteTask(task.id); }}
                                    className="text-slate-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                    <Icons.Trash2 size={16} />
                                </button>
                            </div>
                            <h4 className="text-sm font-medium text-slate-800 mb-1 leading-snug">{task.title}</h4>
                            <p className="text-xs text-slate-500 mb-3">{task.category}</p>
                            <div className="flex justify-between items-center pt-2 border-t border-slate-50">
                                <div className="flex -space-x-2">
                                    <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center text-[10px] text-white font-bold border-2 border-white">
                                    {task.assignee.charAt(0)}
                                    </div>
                                </div>
                                <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    {status !== 'todo' && (
                                    <button onClick={() => onMoveTask(task.id, 'prev')} className="p-1 hover:bg-slate-100 rounded">
                                        <Icons.ChevronRight size={14} className="rotate-180" />
                                    </button>
                                    )}
                                    {status !== 'done' && (
                                    <button onClick={() => onMoveTask(task.id, 'next')} className="p-1 hover:bg-slate-100 rounded">
                                        <Icons.ChevronRight size={14} />
                                    </button>
                                    )}
                                </div>
                            </div>
                        </div>
                        ))}
                    </div>
                </div>
            );
        };

        // --- Main App Logic ---
        
        function CampusManagerApp() {
            const [activeTab, setActiveTab] = useState('dashboard');
            const [isSidebarOpen, setIsSidebarOpen] = useState(true);
            const [currentTime, setCurrentTime] = useState(new Date());
            const [searchQuery, setSearchQuery] = useState('');
            const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
            const [isSettingsOpen, setIsSettingsOpen] = useState(false);
            const [aiLoading, setAiLoading] = useState(false);
            const [aiReport, setAiReport] = useState(null);
            
            // Persistence Hooks
            const usePersistentState = (key, defaultValue) => {
                const [state, setState] = useState(() => {
                try {
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : defaultValue();
                } catch (e) {
                    return defaultValue();
                }
                });
                useEffect(() => {
                localStorage.setItem(key, JSON.stringify(state));
                }, [key, state]);
                return [state, setState];
            };

            const [tasks, setTasks] = usePersistentState('cm_tasks', generateInitialTasks);
            const [facilities, setFacilities] = usePersistentState('cm_facilities', generateInitialFacilities);
            const [staff, setStaff] = usePersistentState('cm_staff', generateInitialStaff);
            const [apiKey, setApiKey] = usePersistentState('cm_api_key', () => '');

            const [newTask, setNewTask] = useState({ title: '', category: 'Admin', priority: 'medium', assignee: 'Self' });

            useEffect(() => {
                const timer = setInterval(() => setCurrentTime(new Date()), 60000);
                return () => clearInterval(timer);
            }, []);

            // -- AI Handlers --

            const handleSmartTaskDraft = async () => {
                if (!apiKey) return alert("Please set your Gemini API Key in Settings first.");
                if (!newTask.title) return alert("Please type a rough task idea first.");
                
                setAiLoading(true);
                try {
                    const prompt = `Convert this rough task note into a structured JSON object for a Campus Director dashboard. 
                    Note: "${newTask.title}". 
                    Return ONLY JSON with keys: title (professional summary), category (choose: Admin, Compliance, Facilities, Events), priority (low, medium, high), assignee (suggest a role). 
                    Example output: {"title": "Repair HVAC", "category": "Facilities", "priority": "high", "assignee": "Maintenance"}`;
                    
                    const result = await callGemini(prompt, apiKey);
                    const cleanJson = result.replace(/```json/g, '').replace(/```/g, '').trim();
                    const parsed = JSON.parse(cleanJson);
                    
                    setNewTask(prev => ({ ...prev, ...parsed }));
                } catch (e) {
                    alert("AI Error: " + e.message);
                } finally {
                    setAiLoading(false);
                }
            };

            const handleGenerateReport = async () => {
                if (!apiKey) return alert("Please set your Gemini API Key in Settings first.");
                
                setAiLoading(true);
                try {
                    const completedTasks = tasks.filter(t => t.status === 'done').map(t => t.title).join(", ");
                    const pendingTasks = tasks.filter(t => t.priority === 'high' && t.status !== 'done').map(t => t.title).join(", ");
                    const statsStr = `Occupancy: ${stats.occupancy}%, Completed: ${stats.done}, Pending High Priority: ${stats.highPriority}`;
                    
                    const prompt = `Write a professional "Weekly Executive Summary" paragraph for a Campus Director based on this data. 
                    Completed Actions: ${completedTasks}. 
                    Critical Pending: ${pendingTasks}. 
                    Metrics: ${statsStr}. 
                    Tone: Formal, concise, administrative. Use Markdown formatting.`;
                    
                    const text = await callGemini(prompt, apiKey);
                    setAiReport(text);
                } catch (e) {
                    alert("AI Error: " + e.message);
                } finally {
                    setAiLoading(false);
                }
            };

            // -- Standard Handlers --

            const handleAddTask = (e) => {
                e.preventDefault();
                const task = {
                id: `t${Date.now()}`,
                ...newTask,
                status: 'todo'
                };
                setTasks([...tasks, task]);
                setIsTaskModalOpen(false);
                setNewTask({ title: '', category: 'Admin', priority: 'medium', assignee: 'Self' });
            };

            const handleDeleteTask = (id) => {
                if (window.confirm('Confirm deletion?')) {
                setTasks(tasks.filter(t => t.id !== id));
                }
            };

            const moveTask = (taskId, direction) => {
                const statusOrder = ['todo', 'in-progress', 'review', 'done'];
                setTasks(prev => prev.map(t => {
                if (t.id !== taskId) return t;
                const currentIndex = statusOrder.indexOf(t.status);
                const newIndex = direction === 'next' 
                    ? Math.min(currentIndex + 1, statusOrder.length - 1)
                    : Math.max(currentIndex - 1, 0);
                return { ...t, status: statusOrder[newIndex] };
                }));
            };

            const toggleFacilityStatus = (id) => {
                setFacilities(prev => prev.map(f => {
                if (f.id !== id) return f;
                const statuses = ['Available', 'Occupied', 'Maintenance'];
                const nextIdx = (statuses.indexOf(f.status) + 1) % 3;
                return { ...f, status: statuses[nextIdx] };
                }));
            };

            const handleExportData = () => {
                const dataStr = JSON.stringify({ tasks, stats, facilities, staff }, null, 2);
                const blob = new Blob([dataStr], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = `campus_ops_log_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };

            const filteredTasks = tasks.filter(t => 
                t.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                t.assignee.toLowerCase().includes(searchQuery.toLowerCase())
            );

            const stats = useMemo(() => {
                const total = tasks.length;
                const done = tasks.filter(t => t.status === 'done').length;
                const highPriority = tasks.filter(t => t.priority === 'high' && t.status !== 'done').length;
                const occupancy = Math.round((facilities.filter(f => f.status === 'Occupied').length / facilities.length) * 100);
                return { total, done, highPriority, occupancy };
            }, [tasks, facilities]);

            // -- Views --

            const DashboardView = () => (
                <div className="space-y-6 animate-fade-in">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <StatCard title="Active Projects" value={stats.total - stats.done} change="+12%" icon={Icons.LayoutDashboard} trend="up" />
                        <StatCard title="Task Completion" value={`${Math.round((stats.done / (stats.total || 1)) * 100)}%`} change="+5%" icon={Icons.CheckSquare} trend="up" />
                        <StatCard title="Critical Issues" value={stats.highPriority} change="-2" icon={Icons.AlertCircle} trend="down" />
                        <StatCard title="Campus Occupancy" value={`${stats.occupancy}%`} change="+8%" icon={Icons.Building2} trend="up" />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
                        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-lg font-bold text-slate-800">Weekly Task Output</h2>
                                <span className="text-xs text-slate-400 self-center">Live Data</span>
                            </div>
                            <SimpleBarChart 
                                data={[
                                    { label: 'Mon', value: 4 },
                                    { label: 'Tue', value: 7 },
                                    { label: 'Wed', value: 5 },
                                    { label: 'Thu', value: 9 },
                                    { label: 'Fri', value: 6 },
                                    { label: 'Sat', value: 2 },
                                    { label: 'Sun', value: 1 },
                                ]}
                            />
                        </div>

                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="text-lg font-bold text-slate-800">Urgent Actions</h2>
                                <button onClick={() => setIsTaskModalOpen(true)} className="text-indigo-600 hover:bg-indigo-50 p-1 rounded">
                                    <Icons.Plus size={20} />
                                </button>
                            </div>
                            <div className="space-y-4">
                                {tasks.filter(t => t.priority === 'high' && t.status !== 'done').slice(0, 3).map(task => (
                                <div key={task.id} className="flex items-start p-3 bg-red-50 rounded-lg border border-red-100">
                                    <Icons.AlertCircle size={16} className="text-red-500 mt-0.5 mr-3 flex-shrink-0" />
                                    <div>
                                    <h4 className="text-sm font-semibold text-slate-800">{task.title}</h4>
                                    <p className="text-xs text-slate-500 mt-1">Assignee: {task.assignee}</p>
                                    </div>
                                </div>
                                ))}
                                <button 
                                onClick={() => setIsTaskModalOpen(true)}
                                className="w-full py-2 border border-dashed border-slate-300 rounded-lg text-slate-500 text-sm hover:bg-slate-50 transition-colors flex items-center justify-center"
                                >
                                <Icons.Plus size={16} className="mr-2" /> Add New Action
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            );

            const TasksView = () => (
                <div className="h-[calc(100vh-140px)] overflow-x-auto pb-4">
                    <div className="flex space-x-6 h-full min-w-[1000px]">
                        {['todo', 'in-progress', 'review', 'done'].map(status => (
                        <KanbanColumn 
                            key={status}
                            title={status.replace('-', ' ').toUpperCase()} 
                            status={status} 
                            tasks={filteredTasks.filter(t => t.status === status)} 
                            onMoveTask={moveTask}
                            onDeleteTask={handleDeleteTask}
                        />
                        ))}
                    </div>
                </div>
            );

            const FacilitiesView = () => (
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                    <div className="p-4 border-b border-slate-200 flex justify-between items-center">
                        <h3 className="font-bold text-slate-700">Real-time Status Monitor</h3>
                        <span className="text-xs text-slate-500 italic">Click status to toggle</span>
                    </div>
                    <div className="grid grid-cols-5 bg-slate-50 p-4 border-b border-slate-200 font-semibold text-slate-600 text-sm">
                        <div className="col-span-2">Facility Name</div>
                        <div>Capacity</div>
                        <div>Status</div>
                        <div>Availability</div>
                    </div>
                    <div className="divide-y divide-slate-100">
                        {facilities.filter(f => f.name.toLowerCase().includes(searchQuery.toLowerCase())).map(f => (
                        <div key={f.id} className="grid grid-cols-5 p-4 items-center hover:bg-slate-50 transition-colors text-sm">
                            <div className="col-span-2 font-medium text-slate-800 flex items-center">
                                <Icons.Building2 size={16} className="text-slate-400 mr-3" />
                                {f.name}
                            </div>
                            <div className="text-slate-500">{f.capacity} Pax</div>
                            <div>
                                <button 
                                    onClick={() => toggleFacilityStatus(f.id)}
                                    className={`px-3 py-1 rounded-full text-xs font-semibold cursor-pointer select-none hover:shadow-sm transition-all ${
                                    f.status === 'Available' ? 'bg-green-100 text-green-700 hover:bg-green-200' :
                                    f.status === 'Maintenance' ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200' :
                                    'bg-red-100 text-red-700 hover:bg-red-200'
                                    }`}
                                >
                                    {f.status}
                                </button>
                            </div>
                            <div className="text-slate-500 font-mono">{f.nextFree}</div>
                        </div>
                        ))}
                    </div>
                </div>
            );

            const StaffView = () => (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {staff.filter(s => s.name.toLowerCase().includes(searchQuery.toLowerCase())).map(s => (
                        <div key={s.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-start space-x-4">
                        <div className={`p-3 rounded-full ${s.department === 'Security' ? 'bg-blue-100 text-blue-600' : s.department === 'Maintenance' ? 'bg-orange-100 text-orange-600' : 'bg-slate-100 text-slate-600'}`}>
                            {s.department === 'Security' ? <Icons.Shield size={24} /> : s.department === 'Maintenance' ? <Icons.Wrench size={24} /> : <Icons.Briefcase size={24} />}
                        </div>
                        <div className="flex-1">
                            <h4 className="font-bold text-slate-800">{s.name}</h4>
                            <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">{s.role}</p>
                            <div className="flex items-center justify-between mt-4">
                            <span className={`text-xs px-2 py-1 rounded border ${s.status === 'On Duty' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-slate-50 text-slate-500 border-slate-200'}`}>
                                {s.status}
                            </span>
                            <span className="text-sm font-mono text-slate-600">{s.contact}</span>
                            </div>
                        </div>
                        </div>
                    ))}
                </div>
            );

            const ReportsView = () => (
                <div className="space-y-6">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <div className="flex justify-between items-center mb-4">
                         <h2 className="text-lg font-bold text-slate-800">Operational Log</h2>
                         <button 
                             onClick={handleGenerateReport} 
                             disabled={aiLoading}
                             className="flex items-center space-x-2 bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-lg text-sm font-semibold hover:bg-indigo-100 transition-colors disabled:opacity-50"
                         >
                             {aiLoading ? <div className="spinner"></div> : <Icons.Sparkles size={16} />}
                             <span>Generate AI Summary</span>
                         </button>
                    </div>

                    {aiReport && (
                        <div className="mb-6 bg-indigo-50 border border-indigo-100 p-4 rounded-lg animate-fade-in">
                            <h3 className="text-xs font-bold text-indigo-500 uppercase mb-2 flex items-center">
                                <Icons.Sparkles size={12} className="mr-1" /> Gemini Executive Summary
                            </h3>
                            <div className="prose prose-sm text-slate-700" dangerouslySetInnerHTML={{ __html: marked.parse(aiReport) }}></div>
                        </div>
                    )}

                    <div className="overflow-hidden rounded-lg border border-slate-200">
                    <table className="min-w-full divide-y divide-slate-200">
                        <thead className="bg-slate-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Event Type</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Description</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                        </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-slate-200">
                        {tasks.filter(t => t.status === 'done').map(t => (
                            <tr key={t.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{new Date().toLocaleDateString()}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-800">Task Completion</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{t.title}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Verified</span>
                            </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                    </div>
                </div>
                </div>
            );

            const AnalyticsView = () => (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                        <h2 className="text-lg font-bold text-slate-800 mb-2">Staff Sentiment Analysis</h2>
                        <p className="text-xs text-slate-500 mb-6">Aggregate daily self-report scores (1-10) - I/O Metric</p>
                        <SimpleBarChart 
                            data={[
                                { label: 'Mon', value: 7.2 },
                                { label: 'Tue', value: 6.8 },
                                { label: 'Wed', value: 7.5 },
                                { label: 'Thu', value: 8.1 },
                                { label: 'Fri', value: 7.9 },
                            ]} 
                            color="bg-indigo-500"
                        />
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                        <h2 className="text-lg font-bold text-slate-800 mb-2">Workload Distribution</h2>
                        <p className="text-xs text-slate-500 mb-6">Current operational focus breakdown</p>
                        <div className="flex flex-col space-y-4 justify-center h-48">
                            {['Compliance', 'Admin', 'Facilities', 'Events'].map(cat => {
                            const count = tasks.filter(t => t.category === cat).length;
                            const pct = tasks.length ? (count / tasks.length) * 100 : 0;
                            return (
                                <div key={cat} className="w-full">
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="font-semibold text-slate-700">{cat}</span>
                                    <span className="text-slate-500">{count} tasks ({Math.round(pct)}%)</span>
                                </div>
                                <div className="w-full bg-slate-100 rounded-full h-2">
                                    <div className="bg-teal-500 h-2 rounded-full" style={{ width: `${pct}%`}}></div>
                                </div>
                                </div>
                            )
                            })}
                        </div>
                        </div>
                    </div>
                    
                    <div className="bg-slate-900 text-white p-6 rounded-xl flex justify-between items-center">
                        <div>
                        <h3 className="font-bold text-lg">Raw Data Export</h3>
                        <p className="text-slate-400 text-sm">Download full JSON dataset for external statistical analysis.</p>
                        </div>
                        <button 
                        onClick={handleExportData}
                        className="flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-medium transition-colors"
                        >
                        <Icons.Download size={18} className="mr-2" />
                        Export JSON
                        </button>
                    </div>
                </div>
            );

            // App Scaffold
            return (
                <div className="flex h-screen bg-slate-100 text-slate-900 font-sans overflow-hidden">
                    {/* Sidebar */}
                    <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-slate-900 flex-shrink-0 transition-all duration-300 flex flex-col`}>
                        <div className="h-16 flex items-center justify-center border-b border-slate-800">
                        {isSidebarOpen ? (
                            <div className="flex items-center space-x-2 text-white">
                            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center font-bold">CM</div>
                            <span className="font-bold text-xl tracking-tight">CampusMgr</span>
                            </div>
                        ) : (
                            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center font-bold text-white">CM</div>
                        )}
                        </div>

                        <div className="flex-1 px-3 py-6 space-y-2 overflow-y-auto">
                        <SidebarItem icon={Icons.LayoutDashboard} label={isSidebarOpen ? "Dashboard" : ""} active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
                        <SidebarItem icon={Icons.CheckSquare} label={isSidebarOpen ? "Task Board" : ""} active={activeTab === 'tasks'} onClick={() => setActiveTab('tasks')} />
                        <SidebarItem icon={Icons.Building2} label={isSidebarOpen ? "Facilities" : ""} active={activeTab === 'facilities'} onClick={() => setActiveTab('facilities')} />
                        <SidebarItem icon={Icons.BarChart3} label={isSidebarOpen ? "Analytics" : ""} active={activeTab === 'analytics'} onClick={() => setActiveTab('analytics')} />
                        <div className="pt-6 border-t border-slate-800 mt-6">
                            <SidebarItem icon={Icons.Users} label={isSidebarOpen ? "Staff Directory" : ""} active={activeTab === 'staff'} onClick={() => setActiveTab('staff')} />
                            <SidebarItem icon={Icons.FileText} label={isSidebarOpen ? "Reports" : ""} active={activeTab === 'reports'} onClick={() => setActiveTab('reports')} />
                        </div>
                        </div>

                        <div className="p-4 border-t border-slate-800 text-center">
                        <div className="flex items-center justify-center space-x-3 cursor-pointer hover:bg-slate-800 rounded-lg p-2 transition-colors" onClick={() => setIsSettingsOpen(true)}>
                            <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center text-white">
                            CD
                            </div>
                            {isSidebarOpen && (
                            <div className="text-left flex-1">
                                <p className="text-sm text-white font-medium">Campus Director</p>
                                <div className="flex items-center text-xs text-slate-500">
                                    <Icons.Settings size={12} className="mr-1" />
                                    <span>Settings</span>
                                </div>
                            </div>
                            )}
                        </div>
                        </div>
                    </aside>

                    {/* Main Content */}
                    <main className="flex-1 flex flex-col min-w-0">
                        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 flex-shrink-0 z-10">
                        <div className="flex items-center">
                            <button 
                            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                            className="mr-4 text-slate-500 hover:text-indigo-600 focus:outline-none"
                            >
                            <Icons.Menu size={24} />
                            </button>
                            <h1 className="text-xl font-bold text-slate-800 capitalize">{activeTab.replace('-', ' ')}</h1>
                        </div>

                        <div className="flex items-center space-x-4">
                            <div className="hidden md:flex items-center bg-slate-100 rounded-lg px-3 py-2">
                            <Icons.Search size={18} className="text-slate-400 mr-2" />
                            <input 
                                type="text" 
                                placeholder="Search resources..." 
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="bg-transparent border-none text-sm focus:ring-0 text-slate-700 w-48 focus:outline-none"
                            />
                            </div>
                            <div className="relative">
                            <button className="text-slate-500 hover:text-indigo-600 relative">
                                <Icons.Bell size={20} />
                                <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                            </button>
                            </div>
                            <div className="text-right hidden sm:block">
                            <p className="text-xs font-bold text-slate-700">{currentTime.toLocaleDateString()}</p>
                            <p className="text-xs text-slate-500">{currentTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                            </div>
                        </div>
                        </header>

                        <div className="flex-1 overflow-y-auto p-6 relative">
                        {activeTab === 'dashboard' && <DashboardView />}
                        {activeTab === 'tasks' && <TasksView />}
                        {activeTab === 'facilities' && <FacilitiesView />}
                        {activeTab === 'analytics' && <AnalyticsView />}
                        {activeTab === 'staff' && <StaffView />}
                        {activeTab === 'reports' && <ReportsView />}
                        </div>
                    </main>

                    {/* Task Modal */}
                    {isTaskModalOpen && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 m-4 animate-fade-in relative">
                            <div className="flex justify-between items-center mb-6">
                            <h3 className="text-xl font-bold text-slate-800">Add New Action</h3>
                            <button onClick={() => setIsTaskModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                                <Icons.X size={24} />
                            </button>
                            </div>
                            <form onSubmit={handleAddTask} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1 flex justify-between">
                                    <span>Task Title / Rough Note</span>
                                    <button 
                                        type="button" 
                                        onClick={handleSmartTaskDraft}
                                        disabled={aiLoading}
                                        className="text-xs flex items-center text-indigo-600 hover:text-indigo-800 disabled:opacity-50"
                                    >
                                        {aiLoading ? <div className="spinner mr-1"></div> : <Icons.Sparkles size={12} className="mr-1" />}
                                        Auto-Fill with AI
                                    </button>
                                </label>
                                <input 
                                type="text" 
                                required
                                className="w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2 border"
                                placeholder="e.g., 'fix lab door' or 'approve roster'"
                                value={newTask.title}
                                onChange={e => setNewTask({...newTask, title: e.target.value})}
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
                                <select 
                                    className="w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2 border"
                                    value={newTask.category}
                                    onChange={e => setNewTask({...newTask, category: e.target.value})}
                                >
                                    <option>Admin</option>
                                    <option>Facilities</option>
                                    <option>Compliance</option>
                                    <option>Events</option>
                                </select>
                                </div>
                                <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Priority</label>
                                <select 
                                    className="w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2 border"
                                    value={newTask.priority}
                                    onChange={e => setNewTask({...newTask, priority: e.target.value})}
                                >
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                </select>
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Assignee</label>
                                <input 
                                type="text" 
                                className="w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2 border"
                                placeholder="e.g., Maint. Team"
                                value={newTask.assignee}
                                onChange={e => setNewTask({...newTask, assignee: e.target.value})}
                                />
                            </div>
                            <div className="pt-4">
                                <button type="submit" className="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700 transition-colors">
                                Create Task
                                </button>
                            </div>
                            </form>
                        </div>
                        </div>
                    )}

                    {/* Settings Modal */}
                    {isSettingsOpen && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl shadow-xl w-full max-w-sm p-6 m-4 animate-fade-in">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-xl font-bold text-slate-800">Settings</h3>
                                <button onClick={() => setIsSettingsOpen(false)} className="text-slate-400 hover:text-slate-600">
                                    <Icons.X size={24} />
                                </button>
                            </div>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Gemini API Key</label>
                                    <input 
                                        type="password" 
                                        className="w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2 border text-sm"
                                        placeholder="Paste your API key here"
                                        value={apiKey}
                                        onChange={e => setApiKey(e.target.value)}
                                    />
                                    <p className="text-xs text-slate-500 mt-2">
                                        Key is stored locally in your browser. Used for AI Task Drafting and Reports.
                                    </p>
                                </div>
                                <button onClick={() => setIsSettingsOpen(false)} className="w-full bg-slate-800 text-white font-bold py-2 rounded-lg hover:bg-slate-700 transition-colors">
                                    Save & Close
                                </button>
                            </div>
                        </div>
                        </div>
                    )}
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<CampusManagerApp />);
    </script>
</body>
</html>
"""

# --- RENDER THE REACT APP INSIDE STREAMLIT ---
components.html(react_app, height=1000, scrolling=True)
