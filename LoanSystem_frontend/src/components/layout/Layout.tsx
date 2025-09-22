import { useState } from 'react';
import Sidebar from './Sidebar';

interface LayoutProps {
	children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
	const [sidebarOpen, setSidebarOpen] = useState(false);
	const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

	const toggleSidebar = () => {
		setSidebarOpen(!sidebarOpen);
	};

	const toggleCollapse = () => {
		setSidebarCollapsed(!sidebarCollapsed);
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-primary-light/40 to-white dark:from-primary-dark/40 dark:to-gray-900 transition-colors duration-700">
			{/* Sidebar */}
			<Sidebar 
				isOpen={sidebarOpen} 
				onClose={() => setSidebarOpen(false)}
				collapsed={sidebarCollapsed}
				onToggleCollapse={toggleCollapse}
			/>

			{/* Main Content */}
			<div className={`transition-all duration-500 ease-in-out ${sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-64'} transform-gpu`}> 
				<main className="min-h-screen transition-all duration-500 ease-in-out">
					{children}
				</main>
			</div>
		</div>
	);
}
