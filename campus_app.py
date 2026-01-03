import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Campus Command Center", page_icon="🏫", layout="wide")

# --- HIDE STREAMLIT UI ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0 !important; }
        iframe { height: 100vh !important; }
    </style>
""", unsafe_allow_html=True)

# --- THE REACT APPLICATION (v3.0 - Scheduler Fixed) ---
react_app = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Director Command Center v3</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        .animate-fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .spinner { border: 3px solid #e2e8f0; border-top: 3px solid #4f46e5; border-radius: 50%; width: 16px; height: 16px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* Table Input Styling */
        .grid-input { width: 100%; background: transparent; padding: 4px; border-radius: 4px; transition: all 0.2s; }
        .grid-input:focus { background: white; outline: 2px solid #6366f1; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .grid-input:hover { background: #f8fafc; }
    </style>
</head>
<body class="bg-slate-100 text-slate-900 font-sans">
    <div id="root"></div>

    <script type="text/babel">
        // --- ICONS ---
        const Icons = {
            LayoutDashboard: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>,
            CheckSquare: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>,
            Calendar: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>,
            Building2: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>,
            BarChart3: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>,
            Users: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
            ExternalLink: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>,
            Search: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>,
            Plus: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>,
            Trash2: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>,
            AlertCircle: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>,
            FileText: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>,
            ChevronRight: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>,
            Menu: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>,
            X: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>,
            Sparkles: (props) => <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
        };

        const { useState, useEffect, useMemo } = React;

        // --- FIXED AI UTILS ---
        async function callGemini(prompt, apiKey) {
            if (!apiKey) throw new Error("API Key Missing");
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
            });
            if (!response.ok) throw new Error("Network Error");
            const data = await response.json();
            return data.candidates?.[0]?.content?.parts?.[0]?.text || "No response";
        }

        // --- SCHEDULER DATA STRUCTURE ---
        const timeSlots = [
            { id: 1, time: '08:30 - 09:20' },
            { id: 2, time: '09:20 - 10:10' },
            { id: 3, time: '10:20 - 11:10' },
            { id: 4, time: '11:10 - 12:00' },
            { id: 5, time: '12:00 - 12:45' },
            { id: 6, time: '12:45 - 01:30' },
            { id: 7, time: '01:30 - 02:15' },
            { id: 8, time: '02:15 - 03:00' },
            { id: 9, time: '03:00 - 03:30' }
        ];

        // --- DATA & STATE ---
        const generateInitialTasks = () => [
            { id: 't1', title: 'Review Q2 Lab Safety Protocols', category: 'Compliance', status: 'todo', priority: 'high', assignee: 'Dr. Smith' },
            { id: 't2', title: 'Coordinate Guest Lecture: Dr. Al-Fayed', category: 'Events', status: 'in-progress', priority: 'medium', assignee: 'Admin Team' },
        ];

        const generateInitialFacilities = () => [
            { id: 'f1', name: 'Lecture Hall A', capacity: 150, status: 'Occupied', nextFree: '14:00' },
            { id: 'f2', name: 'Behav. Science Lab', capacity: 20, status: 'Available', nextFree: 'Now' },
        ];

        const generateInitialStaff = () => [
            { id: 's1', name: 'James Wilson', role: 'Head of Security', department: 'Security', status: 'On Duty', contact: '555-0101' },
            { id: 's2', name: 'Sarah Chen', role: 'Facilities Manager', department: 'Maintenance', status: 'On Duty', contact: '555-0102' },
        ];

        // --- APP COMPONENT ---
        function CampusManagerApp() {
            const [activeTab, setActiveTab] = useState('dashboard');
            const [isSidebarOpen, setIsSidebarOpen] = useState(true);
            const [currentTime, setCurrentTime] = useState(new Date());
            const [searchQuery, setSearchQuery] = useState('');
            const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
            const [isSettingsOpen, setIsSettingsOpen] = useState(false);
            const [aiLoading, setAiLoading] = useState(false);
            const [aiReport, setAiReport] = useState(null);
            const [saveStatus, setSaveStatus] = useState('idle');

            // Persistence
            const usePersistentState = (key, defaultValue) => {
                const [state, setState] = useState(() => {
                    try { return JSON.parse(localStorage.getItem(key)) || defaultValue(); } 
                    catch { return defaultValue(); }
                });
                useEffect(() => { localStorage.setItem(key, JSON.stringify(state)); }, [key, state]);
                return [state, setState];
            };

            const [tasks, setTasks] = usePersistentState('cm_tasks', generateInitialTasks);
            const [facilities, setFacilities] = usePersistentState('cm_facilities', generateInitialFacilities);
            const [staff, setStaff] = usePersistentState('cm_staff', generateInitialStaff);
            const [apiKey, setApiKey] = usePersistentState('cm_api_key', () => '');
            
            // Scheduler State
            const [scheduleData, setScheduleData] = usePersistentState('cm_schedule', () => ({}));
            const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
            
            const [newTask, setNewTask] = useState({ title: '', category: 'Admin', priority: 'medium', assignee: 'Self' });

            useEffect(() => {
                const timer = setInterval(() => setCurrentTime(new Date()), 60000);
                return () => clearInterval(timer);
            }, []);

            // Search Logic
            const matchesSearch = (text) => text && text.toLowerCase().includes(searchQuery.toLowerCase());
            const filteredTasks = tasks.filter(t => matchesSearch(t.title) || matchesSearch(t.assignee) || matchesSearch(t.category));
            const filteredFacilities = facilities.filter(f => matchesSearch(f.name) || matchesSearch(f.status));
            const filteredStaff = staff.filter(s => matchesSearch(s.name) || matchesSearch(s.role) || matchesSearch(s.department));

            const stats = useMemo(() => {
                const total = tasks.length;
                const done = tasks.filter(t => t.status === 'done').length;
                const highPriority = tasks.filter(t => t.priority === 'high' && t.status !== 'done').length;
                const occupancy = Math.round((facilities.filter(f => f.status === 'Occupied').length / facilities.length) * 100);
                return { total, done, highPriority, occupancy };
            }, [tasks, facilities]);

            // --- HANDLERS ---
            
            const handleSmartTaskDraft = async () => {
                if (!apiKey) return alert("⚠️ Setup Required: Please enter your Gemini API Key in Settings.");
                if (!newTask.title) return alert("⚠️ Please type a rough note first.");
                setAiLoading(true);
                try {
                    const prompt = `You are a JSON generator. Analyze task: "${newTask.title}". Return valid JSON with keys: title, category (Admin, Compliance, Facilities, Events), priority (low, medium, high), assignee. Only JSON.`;
                    const result = await callGemini(prompt, apiKey);
                    const jsonStart = result.indexOf('{');
                    const jsonEnd = result.lastIndexOf('}');
                    if (jsonStart === -1) throw new Error("Invalid AI response");
                    const parsed = JSON.parse(result.substring(jsonStart, jsonEnd + 1));
                    setNewTask(prev => ({ ...prev, ...parsed }));
                } catch (e) { alert("AI Error: " + e.message); } finally { setAiLoading(false); }
            };

            const handleGenerateReport = async () => {
                if (!apiKey) return alert("⚠️ Setup Required: Please enter your Gemini API Key in Settings.");
                setAiLoading(true);
                try {
                    const completedTasks = tasks.filter(t => t.status === 'done').map(t => t.title).join(", ");
                    const prompt = `Write a professional "Weekly Executive Summary" for a Campus Director. Metrics: ${stats.occupancy}% Occupancy, ${stats.done} Tasks Completed. Actions: ${completedTasks}. Tone: Formal. Markdown.`;
                    const text = await callGemini(prompt, apiKey);
                    setAiReport(text);
                } catch (e) { alert("AI Error: " + e.message); } finally { setAiLoading(false); }
            };

            const handleSaveSettings = () => {
                setIsSettingsOpen(false);
                setSaveStatus('saved');
                setTimeout(() => setSaveStatus('idle'), 2000);
            };

            // Scheduler Handlers
            const handleScheduleChange = (slotId, field, value) => {
                setScheduleData(prev => ({
                    ...prev,
                    [selectedDate]: {
                        ...prev[selectedDate],
                        [slotId]: {
                            ...prev[selectedDate]?.[slotId],
                            [field]: value
                        }
                    }
                }));
            };

            const getScheduleValue = (slotId, field) => {
                return scheduleData[selectedDate]?.[slotId]?.[field] || '';
            };

            // --- VIEW COMPONENTS ---
            
            const KanbanColumn = ({ title, status, tasks }) => (
                <div className="flex-1 min-w-[280px] bg-slate-50 rounded-xl p-4 flex flex-col h-full border border-slate-200">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-slate-700">{title}</h3>
                        <span className="bg-slate-200 text-slate-600 text-xs px-2 py-1 rounded-full">{tasks.length}</span>
                    </div>
                    <div className="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
                        {tasks.map(task => (
                            <div key={task.id} className="bg-white p-4 rounded-lg shadow-sm border border-slate-100 group relative">
                                <div className="flex justify-between items-start mb-2">
                                    <span className={`text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wide ${task.priority === 'high' ? 'bg-red-100 text-red-600' : task.priority === 'medium' ? 'bg-orange-100 text-orange-600' : 'bg-green-100 text-green-600'}`}>{task.priority}</span>
                                    <button onClick={(e) => { e.stopPropagation(); if(confirm('Delete?')) setTasks(tasks.filter(t=>t.id!==task.id)); }} className="text-slate-300 hover:text-red-500 opacity-0 group-hover:opacity-100"><Icons.Trash2 size={16} /></button>
                                </div>
                                <h4 className="text-sm font-medium text-slate-800 mb-1">{task.title}</h4>
                                <div className="flex justify-between items-center pt-2 mt-2 border-t border-slate-50">
                                    <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center text-[10px] text-white font-bold">{task.assignee.charAt(0)}</div>
                                    <div className="flex space-x-1 opacity-0 group-hover:opacity-100">
                                        {status !== 'todo' && <button onClick={() => { setTasks(prev => prev.map(t => t.id === task.id ? {...t, status: getPrevStatus(t.status)} : t)) }} className="p-1 hover:bg-slate-100 rounded"><Icons.ChevronRight size={14} className="rotate-180" /></button>}
                                        {status !== 'done' && <button onClick={() => { setTasks(prev => prev.map(t => t.id === task.id ? {...t, status: getNextStatus(t.status)} : t)) }} className="p-1 hover:bg-slate-100 rounded"><Icons.ChevronRight size={14} /></button>}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );
            
            const getNextStatus = (s) => { const ord = ['todo','in-progress','review','done']; return ord[Math.min(ord.indexOf(s)+1, 3)]; }
            const getPrevStatus = (s) => { const ord = ['todo','in-progress','review','done']; return ord[Math.max(ord.indexOf(s)-1, 0)]; }

            // --- MAIN RENDER ---
            return (
                <div className="flex h-screen bg-slate-100 text-slate-900 font-sans overflow-hidden">
                    {/* Sidebar */}
                    <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-slate-900 flex-shrink-0 transition-all duration-300 flex flex-col`}>
                        <div className="h-16 flex items-center justify-center border-b border-slate-800 text-white font-bold text-xl">{isSidebarOpen ? "CampusOne" : "CO"}</div>
                        <div className="flex-1 px-3 py-6 space-y-2">
                            {['dashboard','schedule','tasks','facilities','staff','reports'].map(tab => (
                                <button key={tab} onClick={() => setActiveTab(tab)} className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${activeTab === tab ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}>
                                    {tab==='dashboard' && <Icons.LayoutDashboard size={20}/>}
                                    {tab==='schedule' && <Icons.Calendar size={20}/>}
                                    {tab==='tasks' && <Icons.CheckSquare size={20}/>}
                                    {tab==='facilities' && <Icons.Building2 size={20}/>}
                                    {tab==='staff' && <Icons.Users size={20}/>}
                                    {tab==='reports' && <Icons.FileText size={20}/>}
                                    {isSidebarOpen && <span className="capitalize">{tab}</span>}
                                </button>
                            ))}
                        </div>
                        <div className="p-4 border-t border-slate-800">
                            <button onClick={() => setIsSettingsOpen(true)} className="flex items-center space-x-3 text-slate-400 hover:text-white w-full">
                                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">CD</div>
                                {isSidebarOpen && <span className="text-sm">Settings</span>}
                            </button>
                        </div>
                    </aside>

                    {/* Main Content */}
                    <main className="flex-1 flex flex-col min-w-0">
                        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 z-10">
                            <div className="flex items-center">
                                <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="mr-4 text-slate-500"><Icons.Menu size={24}/></button>
                                <h1 className="text-xl font-bold capitalize">{activeTab}</h1>
                            </div>
                            <div className="flex items-center space-x-4">
                                <div className="flex items-center bg-slate-100 rounded-lg px-3 py-2">
                                    <Icons.Search size={18} className="text-slate-400 mr-2"/>
                                    <input type="text" placeholder="Search system..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} className="bg-transparent border-none text-sm focus:outline-none w-48"/>
                                </div>
                                {saveStatus === 'saved' && <span className="text-green-600 text-sm font-bold animate-pulse">Saved!</span>}
                            </div>
                        </header>

                        <div className="flex-1 overflow-y-auto p-6">
                            
                            {/* DASHBOARD */}
                            {activeTab === 'dashboard' && (
                                <div className="space-y-6 animate-fade-in">
                                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                                        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm"><p className="text-xs font-bold text-slate-500 uppercase">Pending Tasks</p><h3 className="text-2xl font-bold mt-1">{stats.total - stats.done}</h3></div>
                                        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm"><p className="text-xs font-bold text-slate-500 uppercase">Completion</p><h3 className="text-2xl font-bold mt-1 text-green-600">{Math.round((stats.done / (stats.total || 1)) * 100)}%</h3></div>
                                        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm"><p className="text-xs font-bold text-slate-500 uppercase">Critical</p><h3 className="text-2xl font-bold mt-1 text-red-600">{stats.highPriority}</h3></div>
                                        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm"><p className="text-xs font-bold text-slate-500 uppercase">Occupancy</p><h3 className="text-2xl font-bold mt-1 text-indigo-600">{stats.occupancy}%</h3></div>
                                    </div>
                                </div>
                            )}

                            {/* DAILY SCHEDULER VIEW (NEW) */}
                            {activeTab === 'schedule' && (
                                <div className="space-y-4 animate-fade-in">
                                    <div className="flex items-center justify-between bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                        <div className="flex items-center space-x-2">
                                            <Icons.Calendar size={20} className="text-indigo-600" />
                                            <span className="font-bold text-slate-700">Select Date:</span>
                                            <input 
                                                type="date" 
                                                className="border rounded-lg p-2 text-sm"
                                                value={selectedDate}
                                                onChange={(e) => setSelectedDate(e.target.value)}
                                            />
                                        </div>
                                        <span className="text-xs text-slate-400">Autosave enabled</span>
                                    </div>

                                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                                        <div className="overflow-x-auto">
                                            <table className="min-w-full divide-y divide-slate-200">
                                                <thead className="bg-slate-50">
                                                    <tr>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-16">#</th>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-32">Time</th>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Task</th>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-48">Link</th>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-48">Stakeholders</th>
                                                        <th className="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider w-64">Remarks</th>
                                                    </tr>
                                                </thead>
                                                <tbody className="bg-white divide-y divide-slate-200">
                                                    {timeSlots.map((slot) => (
                                                        <tr key={slot.id} className="hover:bg-slate-50">
                                                            <td className="px-4 py-2 text-sm text-slate-500 font-mono">{slot.id}</td>
                                                            <td className="px-4 py-2 text-sm font-bold text-slate-700 whitespace-nowrap">{slot.time}</td>
                                                            <td className="px-4 py-2"><input type="text" placeholder="Enter task..." className="grid-input" value={getScheduleValue(slot.id, 'task')} onChange={(e) => handleScheduleChange(slot.id, 'task', e.target.value)} /></td>
                                                            <td className="px-4 py-2 relative group">
                                                                <div className="flex items-center">
                                                                    <input type="text" placeholder="https://..." className="grid-input" value={getScheduleValue(slot.id, 'link')} onChange={(e) => handleScheduleChange(slot.id, 'link', e.target.value)} />
                                                                    {getScheduleValue(slot.id, 'link') && (
                                                                        <a href={getScheduleValue(slot.id, 'link')} target="_blank" className="ml-1 text-indigo-600 hover:text-indigo-800"><Icons.ExternalLink size={14} /></a>
                                                                    )}
                                                                </div>
                                                            </td>
                                                            <td className="px-4 py-2"><input type="text" placeholder="Who involved?" className="grid-input" value={getScheduleValue(slot.id, 'stakeholders')} onChange={(e) => handleScheduleChange(slot.id, 'stakeholders', e.target.value)} /></td>
                                                            <td className="px-4 py-2"><input type="text" placeholder="Notes..." className="grid-input" value={getScheduleValue(slot.id, 'remarks')} onChange={(e) => handleScheduleChange(slot.id, 'remarks', e.target.value)} /></td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* OTHER VIEWS */}
                            {activeTab === 'tasks' && (
                                <div className="h-full overflow-x-auto pb-4"><div className="flex space-x-6 h-full min-w-[1000px]">{['todo','in-progress','review','done'].map(s => <KanbanColumn key={s} title={s.toUpperCase()} status={s} tasks={filteredTasks.filter(t=>t.status===s)} />)}</div></div>
                            )}

                            {activeTab === 'facilities' && (
                                <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                                    <div className="grid grid-cols-4 bg-slate-50 p-4 font-bold text-xs text-slate-500 uppercase"><div>Name</div><div>Capacity</div><div>Status</div><div>Next Free</div></div>
                                    <div className="divide-y divide-slate-100">{filteredFacilities.map(f => <div key={f.id} className="grid grid-cols-4 p-4 text-sm items-center hover:bg-slate-50"><div className="font-medium flex items-center"><Icons.Building2 size={16} className="text-slate-400 mr-2"/>{f.name}</div><div className="text-slate-500">{f.capacity}</div><div><span className={`px-2 py-1 rounded-full text-xs font-bold ${f.status==='Available'?'bg-green-100 text-green-700':f.status==='Maintenance'?'bg-yellow-100 text-yellow-700':'bg-red-100 text-red-700'}`}>{f.status}</span></div><div className="font-mono text-slate-500">{f.nextFree}</div></div>)}</div>
                                </div>
                            )}

                            {activeTab === 'staff' && (
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">{filteredStaff.map(s => <div key={s.id} className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-start space-x-4"><div className="p-3 bg-slate-100 rounded-full"><Icons.Users size={24} className="text-slate-600"/></div><div><h4 className="font-bold">{s.name}</h4><p className="text-xs uppercase text-slate-500 mb-2">{s.role}</p><span className={`text-xs px-2 py-1 rounded border ${s.status==='On Duty'?'bg-green-50 text-green-700 border-green-200':'bg-slate-50 text-slate-500'}`}>{s.status}</span></div></div>)}</div>
                            )}

                            {activeTab === 'reports' && (
                                <div className="space-y-6">
                                    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                                        <div className="flex justify-between items-center mb-6"><h2 className="font-bold text-lg">AI Executive Summary</h2><button onClick={handleGenerateReport} disabled={aiLoading} className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-indigo-700 disabled:opacity-50 flex items-center">{aiLoading ? <div className="spinner mr-2"></div> : <Icons.Sparkles size={16} className="mr-2"/>} Generate Report</button></div>
                                        {aiReport ? <div className="prose prose-sm max-w-none bg-slate-50 p-6 rounded-lg border border-slate-200" dangerouslySetInnerHTML={{ __html: marked.parse(aiReport) }}></div> : <div className="text-center py-12 text-slate-400 border-2 border-dashed border-slate-200 rounded-lg">No report generated yet. Click the button above.</div>}
                                    </div>
                                </div>
                            )}
                        </div>
                    </main>

                    {/* MODALS */}
                    {isTaskModalOpen && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                            <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 m-4">
                                <div className="flex justify-between mb-4"><h3 className="font-bold">New Action</h3><button onClick={()=>setIsTaskModalOpen(false)}><Icons.X/></button></div>
                                <div className="space-y-4">
                                    <div><label className="flex justify-between text-sm font-medium mb-1"><span>Task Note</span><button onClick={handleSmartTaskDraft} disabled={aiLoading} className="text-indigo-600 text-xs flex items-center hover:underline">{aiLoading ? "Thinking..." : "✨ AI Auto-Fill"}</button></label><input className="w-full border rounded-lg p-2" value={newTask.title} onChange={e=>setNewTask({...newTask, title:e.target.value})} placeholder="e.g. 'Fix the projector in Hall A'" /></div>
                                    <div className="grid grid-cols-2 gap-4"><div><label className="text-sm font-medium">Category</label><select className="w-full border rounded-lg p-2" value={newTask.category} onChange={e=>setNewTask({...newTask, category:e.target.value})}><option>Admin</option><option>Facilities</option><option>Compliance</option><option>Events</option></select></div><div><label className="text-sm font-medium">Priority</label><select className="w-full border rounded-lg p-2" value={newTask.priority} onChange={e=>setNewTask({...newTask, priority:e.target.value})}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></div></div>
                                    <div><label className="text-sm font-medium">Assignee</label><input className="w-full border rounded-lg p-2" value={newTask.assignee} onChange={e=>setNewTask({...newTask, assignee:e.target.value})} /></div>
                                    <button onClick={()=>{ setTasks([...tasks, {id:`t${Date.now()}`, ...newTask, status:'todo'}]); setIsTaskModalOpen(false); setNewTask({title:'',category:'Admin',priority:'medium',assignee:'Self'}); }} className="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700">Create Task</button>
                                </div>
                            </div>
                        </div>
                    )}

                    {isSettingsOpen && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                            <div className="bg-white rounded-xl shadow-xl w-full max-w-sm p-6 m-4">
                                <div className="flex justify-between mb-4"><h3 className="font-bold">Settings</h3><button onClick={()=>setIsSettingsOpen(false)}><Icons.X/></button></div>
                                <div className="space-y-4">
                                    <div><label className="block text-sm font-medium mb-1">Gemini API Key</label><input type="password" className="w-full border rounded-lg p-2" value={apiKey} onChange={e=>setApiKey(e.target.value)} placeholder="Paste API Key here" /><p className="text-xs text-slate-500 mt-1">Data saved to browser LocalStorage.</p></div>
                                    <button onClick={handleSaveSettings} className="w-full bg-slate-800 text-white font-bold py-2 rounded-lg hover:bg-slate-700">Save & Close</button>
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

components.html(react_app, height=1000, scrolling=True)
